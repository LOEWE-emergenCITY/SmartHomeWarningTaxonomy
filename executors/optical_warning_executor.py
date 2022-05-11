from PyP100 import PyL530
from gui.alert_dialog import Alert_Dialog
import time
from threading import Thread

ip = "192.168.178.73"
username = "marcwendelborn@web.de"
password = "Pinguin1"

def flash_light(id, l530, flash):
    while True:
        l530.turnOn()
        time.sleep(1)
        l530.turnOff()
        time.sleep(1)
        if flash():
            break

def execute_optical_warning(text):
    l530 = PyL530.L530(ip, username, password) 
    l530.handshake() 
    l530.login()

    flash = False
    for id in range(0,1):
        sound = Thread(target=flash_light, args=(id, l530, lambda: flash))
        sound.start()

    dialog = Alert_Dialog(text)
    dialog.create_dialog()

    if dialog.stop_alert:
        flash = True

execute_optical_warning('test')