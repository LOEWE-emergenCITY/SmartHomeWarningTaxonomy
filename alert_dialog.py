import threading
import logging
import time
import datetime as dt

import tkinter as tk
from tkinter import *
from tkinter.messagebox import *

from alerts import trigger_acoustic_alert
from alerts import trigger_optical_alert
from alerts import trigger_sms_alert

from feedback_dialog import Feedback_Dialog

from util import save_feedback
from util import load_simulation



# To make it run on pi via ssh: export DISPLAY=":0"

MAX_ALERT_RUNNING_TIME = 300

class Alert_Dialog:
    def __init__(self, simulation_file_name, feedback_file_name):
        self.logger = logging.getLogger('main')
        self.simulation_file_name = simulation_file_name
        self.feedback_file_name = feedback_file_name
        self.window = tk.Toplevel()
        self.event = {"id": 0, "categorie": "", "time": "", "alerts": [], "message": ""}
        self.alert_runs = False
        self.collects_feedback = False
        self.stop_alert = False
        self.alert_threads = []
        self.feedback_dialog = Feedback_Dialog(simulation_file_name, feedback_file_name)
        self.create_dialog()
        self.window.withdraw()

    # This method measures the time an alert is running and terminates it when it exceeds the maximum time
    def measure_alarm_time(self):
        start_time = dt.datetime.now()
        end_time = start_time + dt.timedelta(seconds=MAX_ALERT_RUNNING_TIME)
        while self.alert_runs:
            time.sleep(1)
            if (end_time < dt.datetime.now()):
                self.logger.info("Alert: Alarm forced to terminate. Start time: {}, Now: {}".format(start_time, dt.datetime.now()))
                self.event['time_acknowledge'] = None
                save_feedback(self.simulation_file_name, self.feedback_file_name, self.event, [], True, '')
                self.terminate_alert()
                break

    def dispatch_event(self, event, feedback_dialog):
        self.logger.info("Alert: Dispatch event with ID {}".format(event["id"]))
        self.alert_runs = True
        self.stop_alert = False
        self.feedback_dialog = feedback_dialog
        self.event = event
        self.event['time_triggered'] = dt.datetime.now()
        self.text_label['text'] = event['message']
        self.text_label.update()
        self.window.deiconify()
        self.switchOn_alerts(event['alerts'])
        time_thread = threading.Thread(target=self.measure_alarm_time)
        time_thread.start()

    def perception_acknowledged(self, device):
        self.event['time_acknowledge'] = dt.datetime.now()
        self.switchOff_alerts()
        self.feedback_dialog.collect_feedback(self.event, device)
        self.terminate_alert()

    def abort_alert(self):
        if askyesno("Switch off alarm", "This function is only intended for bystanders who feel disturbed by the alarm. \n Sure that the alarm should be turned off?"):
            self.logger.warning("Alert: Alarm was stopped by a third person")
            self.terminate_alert()
        
    def switchOn_alerts(self, alerts):
        for alert in alerts:
            if alert == 'acoustic':
                sound_threat = threading.Thread(target=trigger_acoustic_alert, args=(id, lambda: self.stop_alert, False))
                sound_threat.start()
                self.alert_threads.append(sound_threat)
            if alert == 'acoustic_alarm':
                sound_threat = threading.Thread(target=trigger_acoustic_alert, args=(id, lambda: self.stop_alert, True))
                sound_threat.start()
                self.alert_threads.append(sound_threat)
            if alert == 'optic_red':
                optical_threat = threading.Thread(target=trigger_optical_alert, args=(id, lambda: self.stop_alert, "red", False))
                optical_threat.start()
                self.alert_threads.append(optical_threat)
            if alert == 'optic_blue':
                optical_threat = threading.Thread(target=trigger_optical_alert, args=(id, lambda: self.stop_alert, "blue", False))
                optical_threat.start()
                self.alert_threads.append(optical_threat)
            if alert == 'optic_white':
                optical_threat = threading.Thread(target=trigger_optical_alert, args=(id, lambda: self.stop_alert, "white", False))
                optical_threat.start()
                self.alert_threads.append(optical_threat)
            if alert == 'optic_bl_red':
                optical_threat = threading.Thread(target=trigger_optical_alert, args=(id, lambda: self.stop_alert, "red", True))
                optical_threat.start()
                self.alert_threads.append(optical_threat)
            if alert == 'optic_bl_blue':
                optical_threat = threading.Thread(target=trigger_optical_alert, args=(id, lambda: self.stop_alert, "blue", True))
                optical_threat.start()
                self.alert_threads.append(optical_threat)
            if alert == 'optic_bl_white':
                optical_threat = threading.Thread(target=trigger_optical_alert, args=(id, lambda: self.stop_alert, "white", True))
                optical_threat.start()
                self.alert_threads.append(optical_threat)
            if alert == 'email':
                return
            if alert == 'sms':
                simulation = load_simulation(self.simulation_file_name)
                number = simulation['user_data']['phone']
                sms_threat = threading.Thread(target=trigger_sms_alert, args=(id, self.perception_acknowledged, self.event['message'], number))
                sms_threat.start()
                self.alert_threads.append(sms_threat)

    def switchOff_alerts(self):
        self.stop_alert = True
        for thread in self.alert_threads:
            thread.join()
        self.alert_threads = []

    def terminate_alert(self):
        self.alert_runs = False
        self.switchOff_alerts()
        self.window.withdraw()
        self.logger.info("Alert: End event with ID {}".format(self.event["id"]))
    
    def create_dialog(self):
        self.window.title('Smart Home Systems Study')

        # Make root window full screen
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.attributes('-fullscreen', True)
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.bind("<Escape>", lambda e: self.window.quit())

        center_frame = tk.Frame(self.window, width=400, height=300)
        center_frame.pack(expand=TRUE, ipady=50)

        self.text_label = Label(center_frame, text=self.event["message"], font=("Calibri", 25))
        self.text_label.pack(pady=20)

        button_frame = tk.Frame(center_frame, width=300)
        button_frame.pack(ipady=20)

        acknowledge_button = Button(button_frame, command=lambda : self.perception_acknowledged('display'), text="Alarm perceived", background="green", foreground="white", font=("Calibri", 25))   
        acknowledge_button.pack(side=LEFT, padx=20)

        abort_button = Button(button_frame, command=lambda : self.abort_alert(), text="Abort", background="red", foreground="white", font=("Calibri", 25))   
        abort_button.pack(side=LEFT, padx=20)
