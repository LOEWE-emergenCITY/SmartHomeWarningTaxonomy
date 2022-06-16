from PyP100 import PyL530
from threading import Thread
import time
from playsound import playsound


ip = "192.168.178.73"
username = "marcwendelborn@web.de"
password = "Pinguin1"

def trigger_acoustic_alert(id, stop):
    while True:
        playsound('mixkit-classic-alarm-995.wav')
        if stop():
            break

def trigger_optical_alert(id, flash):
    l530 = PyL530.L530(ip, username, password) 
    l530.handshake() 
    l530.login()

    while True:
        try:
            l530.turnOn()
            time.sleep(1)
            l530.turnOff()
            time.sleep(1)
            if flash():
                break
        except KeyError as e:
            print("Optical_Alert    : Error while triggering optical alert. Error: {}".format(e))
