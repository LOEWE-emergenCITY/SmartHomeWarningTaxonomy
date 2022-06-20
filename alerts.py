import logging
from PyP100 import PyL530
from threading import Thread
import time
from playsound import playsound


ip = "192.168.178.73"
username = "marcwendelborn@web.de"
password = "Pinguin1"

logger = logging.getLogger('main')

def trigger_acoustic_alert(id, stop):
    try:
        logger.info("Trigger acoustic alert")
        while True:
            playsound('mixkit-classic-alarm-995.wav')
            if stop():
                logger.info("Stop acoustic alert")
                break
    except Exception as e:
        logger.error("Acoustic_Alert: Error while triggering acoustic alert. Error: {}".format(e))
        return

def trigger_optical_alert(id, flash):
    logger.info("Trigger optical alert")
    l530 = PyL530.L530(ip, username, password) 
    try:
        l530.handshake() 
        l530.login()
    except Exception as e:
        logger.error("Optical_Alert: Error while initialising connection to smart light. Error: {}".format(e))
        return

    while True:
        try:
            l530.turnOn()
            time.sleep(1)
            l530.turnOff()
            time.sleep(1)
            if flash():
                logger.info("Stop optical alert")
                break
        except Exception as e:
            logger.error("Optical_Alert: Error while triggering optical alert. Error: {}".format(e))
            return

