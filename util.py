import logging
import json
import datetime
import csv
import RPi.GPIO as GPIO
import time
from random import shuffle

logger = logging.getLogger('main')
simulation_file_path = '/home/pi/masterthesis/resources/simulations/'
#file_name = 'resources/simulations/TestSimulation.json'

def load_simulation(simulation_file_name):
    simulation_json = open(simulation_file_name)
    simulation = json.load(simulation_json)
    return simulation

def setup_logger():
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger('main')
    rootLogger.setLevel(logging.INFO)

    #fileHandler = logging.FileHandler("{0}/{1}.log".format('resources', 'log'))
    fileHandler = logging.FileHandler("{0}/{1}.log".format('/home/pi/masterthesis/resources', 'log'))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    return rootLogger

def match_times_with_events(times, events):
    shuffle(times)
    merged_list = zip(times, events)
    return tuple(merged_list)

def init_feedback_file(simulation_file_name):
    logger = logging.getLogger('main')
    logger.info("Init feedback file")
    #print("Feedback    : Init feedback file")
    simulation = load_simulation(simulation_file_name)
    user_id = simulation['user_data']['id']
    headers = ['user_id', 'event_id', 'answer', 'time_triggerd', 'time_acknowledge', 'missed', 'ack_medium']
    
    file = open('/home/pi/masterthesis/resources/feedback_{}.csv'.format(user_id), 'w')
    writer = csv.writer(file)
    writer.writerow(headers)
    file.close()

def save_feedback(simulation_file_name, event, answer, missed, media):
    logger = logging.getLogger('main')
    logger.info("Store feedback for event {}".format(event['id']))
    simulation = load_simulation(simulation_file_name)
    user_id = simulation['user_data']['id']
    # TODO Calculate and store time user needed for perception
    feedback = [user_id, event['id'], answer, event['time_triggered'], event['time_acknowledge'], missed, media]

    #print("Feedback    : Store feedback for question {}".format(question_id))
    file = open('/home/pi/masterthesis/resources/feedback_{}.csv'.format(user_id), 'a+', newline='')
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
    