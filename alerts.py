import logging
import time
import serial
import threading

from util import *
from pydub import AudioSegment
from pydub.playback import play
from gsmHat import GSMHat
from requests import post

ip = "192.168.178.73"
username = "adress@server"
password = "Pinguin1"

HOME_ASSISTANT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJkZTIxODNjMzk0NDE0NjM1OTg0NmNmZDhiOWNlMTU2NCIsImlhdCI6MTY1NzE4MTE2MiwiZXhwIjoxOTcyNTQxMTYyfQ.I2jlxAbumbuLndSRmMLlxC6ek0YfPVRo2k82uhGOExc'
HOME_ASSISTANT_ENTITY_ID = 'light.light01_level_light_color_on_off'

logger = logging.getLogger('main')

def trigger_acoustic_alert(id, stop, is_alarm):
    try:
        logger.info("Trigger acoustic alert")
        if is_alarm:
            song = AudioSegment.from_wav("/home/pi/shws/sound_alarm.wav")
        else:
            song = AudioSegment.from_wav("/home/pi/shws/sound_normal.wav")
        while True:
            play(song)
            if stop():
                logger.info("Stop acoustic alert")
                break
    except Exception as e:
        logger.error("Acoustic_Alert: Error while triggering acoustic alert. Error: {}".format(e))
        return

def trigger_optical_alert(id, flash, color, blinking):
    rgb_color = [255, 0, 0]
    if color == "blue":
        rgb_color = [52, 70, 235]
    if color == "white":
        rgb_color = [255,255,255]

    logger.info("Trigger optical alert")
    try:
        url_on = "http://localhost:8123/api/services/light/turn_on"
        url_off = "http://localhost:8123/api/services/light/turn_off"
        headers = {"Authorization": "Bearer {}".format(HOME_ASSISTANT_TOKEN)}
        data_on = {"entity_id": HOME_ASSISTANT_ENTITY_ID, "rgb_color": rgb_color}
        data_off = {"entity_id": HOME_ASSISTANT_ENTITY_ID}
        while True:
            post(url_on, headers=headers, json=data_on)
            time.sleep(1)
            if blinking:
                post(url_off, headers=headers, json=data_off)
            if flash():
                logger.info("Stop optical alert")
                if not blinking:
                    post(url_off, headers=headers, json=data_off)
                break
            time.sleep(1)
    except Exception as e:
        logger.error("Optical_Alert: Error while initialising connection to smart light. Error: {}".format(e))
        return

def trigger_sms_alert(id, ack_function, message, number):
    try:
        logger.info("Trigger SMS alert")

        #gsm = GSMHat('/dev/ttyS0', 115200)

        message = '[Smart Home Studie] ' + message

        messageString = 'AT+CMGS="' + number  + '"\n' + message + '\x1A'

        ser = serial.Serial('/dev/ttyS0', 115200)
        ser.flushInput()

        string = messageString + '\n'

        ser.write(string.encode('iso-8859-1'))

        ser.close()
        time.sleep(1)

        feedback_thread = threading.Thread(target=check_for_sms, args=(ack_function, id))
        feedback_thread.start()

    except Exception as e:
        logger.error("SMS_Alert: Error while triggering SMS alert. Error: {}".format(e))

def check_for_sms(ack_function, id):
    logger.info('SMS_Alert: Start thread waiting for feedback...')
    try:
        gsm = GSMHat('/dev/ttyS0', 115200)
        # Check, if new SMS is available
        received_SMS = False
        while not received_SMS:
            if gsm.SMS_available() > 0:
                newSMS = gsm.SMS_read()
                if (newSMS.Sender != 'ALDI TALK'):
                    logger.info('SMS_Alert: Received SMS from {} at {} with message {}'.format(newSMS.Sender, newSMS.Date, newSMS.Message))
                    received_SMS = True
        ack_function('phone')
        gsm.close()
    except Exception as e:
        logger.error("SMS_Alert: Error while waiting for an SMS response. Error: {}".format(e))
