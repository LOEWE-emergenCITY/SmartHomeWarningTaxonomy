import logging
import time
import serial

from util import *
from PyP100 import PyL530
from playsound import playsound
from gsmHat import GSMHat

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

def trigger_sms_alert(id, message):
    try:
        logger.info("Trigger optical alert")
        simulation = load_simulation()
        number = simulation['user_data']['phone']

        gsm = GSMHat('/dev/ttyS0', 115200)

        messageString = 'AT+CMGS="' + number  + '"\n' + message + '\x1A'

        ser = serial.Serial('/dev/ttyS0', 115200)
        ser.flushInput()

        string = messageString + '\n'

        ser.write(string.encode('iso-8859-1'))
        ser.close()
    except Exception as e:
        logger.error("SMS_Alert: Error while triggering SMS alert. Error: {}".format(e))


