import logging
import json
import datetime
import csv

logger = logging.getLogger('main')
file_name = 'TestSimulation.json'

def load_simulation():
    test_simulation_json = open(file_name)
    simulation = json.load(test_simulation_json)
    return simulation

def setup_logger():
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger('main')
    rootLogger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler("{0}/{1}.log".format('resources', 'log'))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    return rootLogger

def init_feedback_file():
    logger = logging.getLogger('main')
    logger.info("Init feedback file")
    #print("Feedback    : Init feedback file")
    simulation = load_simulation()
    user_id = simulation['user_data']['id']
    headers = ['user_id', 'event_id', 'answer', 'time']
    
    file = open('resources/feedback_{}.csv'.format(user_id), 'w')
    writer = csv.writer(file)
    writer.writerow(headers)
    file.close()

def init_response_time_file():
    logger = logging.getLogger('main')
    logger.info("Init response_time file")
    #print("Feedback    : Init response_time file")
    simulation = load_simulation()
    user_id = simulation['user_data']['id']
    headers = ['user_id', 'alarm_id', 'start_time', 'response_time', 'missed', 'ack_medium']

    file = open('resources/response_time_{}.csv'.format(user_id), 'w')
    writer = csv.writer(file)
    writer.writerow(headers)
    file.close()

def save_feedback(event_id, answer):
    logger = logging.getLogger('main')
    logger.info("Store feedback for event {}".format(event_id))
    simulation = load_simulation()
    time = datetime.datetime.now()
    user_id = simulation['user_data']['id']
    # TODO Calculate and store time user needed for perception
    feedback = [user_id, event_id, answer, time]

    #print("Feedback    : Store feedback for question {}".format(question_id))
    file = open('resources/feedback_{}.csv'.format(user_id), 'a+', newline='')
    writer = csv.writer(file)
    writer.writerow(feedback)
    file.close()