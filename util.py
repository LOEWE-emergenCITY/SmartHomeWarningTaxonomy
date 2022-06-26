import logging
import json
import datetime
import csv
import RPi.GPIO as GPIO
import time

logger = logging.getLogger('main')
file_name = '/home/pi/masterthesis/TestSimulation.json'
#file_name = 'TestSimulation.json'

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
    headers = ['user_id', 'event_id', 'answer', 'time_triggerd', 'time_acknowledge', 'missed', 'ack_medium']
    
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

def save_feedback(event, answer, missed):
    logger = logging.getLogger('main')
    logger.info("Store feedback for event {}".format(event['id']))
    simulation = load_simulation()
    time = datetime.datetime.now()
    user_id = simulation['user_data']['id']
    # TODO Calculate and store time user needed for perception
    feedback = [user_id, event['id'], answer, event['time_triggered'], event['time_acknowledge'], missed, 'display']

    #print("Feedback    : Store feedback for question {}".format(question_id))
    file = open('resources/feedback_{}.csv'.format(user_id), 'a+', newline='')
    writer = csv.writer(file)
    writer.writerow(feedback)
    file.close()

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    begin_time = datetime.time(int(begin_time.split(':')[0]), int(begin_time.split(':')[1]))
    end_time = datetime.time(int(end_time.split(':')[0]), int(end_time.split(':')[1]))
    check_time = check_time or datetime.datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def connect_to_gsm_hat():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    while True:
        GPIO.output(7, GPIO.LOW)
        time.sleep(4)
        GPIO.output(7, GPIO.HIGH)
        break
    GPIO.cleanup()