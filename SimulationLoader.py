import json
import logging
import threading
from time import sleep
import tkinter as tk
from tkinter import *

from apscheduler.schedulers.background import BackgroundScheduler
from executors.optical_warning_executor import execute_optical_warning
from executors.acoustic_warning_executor import execute_acoustic_warning
from executors.email_warning_executor import execute_email_warning
from executors.sms_warning_executor import execute_sms_warning
from executors.gui.base_dialog import Base_Dialog
from executors.gui.alert_dialog import Alert_Dialog

class SimulationLoader():

    def __init__(self):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        self.block_execution = False

        # Start Base Dialog
        root = tk.Tk()
        root.withdraw()
        logging.info("Main    : Successfully started base dialog")

        simulation = self.loadFile('TestSimulation.json')
        #alert_dialog = Alert_Dialog({"id": 1, "categorie": "highest", "time": "17:02:20", "alerts": ["acoustic"], "message": "Die Sicherung der Kaffeemaschine ist durchgebrannt!"})
        self.base_dialog = Base_Dialog()
        self.run_simulation(simulation)
        self.base_dialog.trigger_mainloop()
        #execute_acoustic_warning("test")
        #execute_email_warning('test')

    def loadFile(self, file_name):
        logging.info("Main    : Start loading simulation file...")
        test_simulation_json = open(file_name)
        simulation = json.load(test_simulation_json)
        logging.info("Main    : Successfully loaded simulation file")
        return simulation

    def run_simulation(self, simulation):
        date = simulation['config']['date']
        events = simulation['events']
        scheduler = BackgroundScheduler(timezone="Europe/Berlin")

        for event in events:
            execution_time = date + " " + event['time']
            scheduler.add_job(self.dispatch_alarm, 'date', run_date=execution_time, args=(event, self.base_dialog))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            print("Shutdown")
            pass

    def dispatch_alarm(self, event, base_dialog):
        if (self.block_execution):
            logging.info("Main    : Event with ID {} was missed because the execution was blocked".format(event["id"]))
        else:
            logging.info("Main    : Dispatch event with ID {}".format(event["id"]))
            #Alert_Dialog(event)
            base_dialog.dispatch_alert_dialog(event)

simulation = SimulationLoader()
