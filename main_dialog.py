import tkinter as tk
import time
import logging
import threading
import datetime as dt
from os import listdir
from tkinter import *
from alert_dialog import Alert_Dialog
from feedback_dialog import Feedback_Dialog
from util import *
from scheduler import Scheduler
import random

# To make it run on pi via ssh: export DISPLAY=":0"

class Main_Dialog:

    state = "Studie läuft"

    def __init__(self):
        #print("Main    : Start program at {}".format(dt.datetime.now()))
        self.block_execution = False

        # Logger
        self.logger = setup_logger()
        self.logger.info("Main: Start program at {}".format(dt.datetime.now()))

        # GUI components
        self.window = tk.Toplevel()
        self.center_frame = tk.Frame(self.window, width=400, height=300)
        self.text_frame = tk.Frame(self.center_frame)
        self.label1 = Label(self.text_frame, text="Status: ", font=("Calibri", 20))
        self.label2 = Label(self.text_frame, text="Studie läuft", fg="green", font=("Calibri", 20))
        self.checkout_button = Button(self.center_frame, command=lambda: self.change_study_status(), text="Check-Out", height=2, background="#000000", foreground="white", font=("Calibri", 25))
        self.img = PhotoImage(file='/home/pi/masterthesis/executors/gui/peasec_logo.png')
        #self.img = PhotoImage(file='executors\gui\peasec_logo.png')
        self.start_button = Button(self.center_frame, command=lambda: self.run_simulation_threat(), text="Studie starten", height=2, background="#000000", foreground="white", font=("Calibri", 25))
        self.img_label = Label(self.center_frame, image=self.img)
        self.error_label = Label(self.center_frame)
        self.finish_label = Label(self.center_frame, text="Die Studie ist abgeschlossen. Vielen Dank für Ihre Teilnahme! \n Die Box kann nun von der Stromversorgung getrennt werden.", font=("Calibri", 17))

         # Load Simulation
        self.simulation_file_name = self.get_file_name()
        self.simulation = load_simulation(self.simulation_file_name)

        # Setup files
        self.feedback_file_name = init_feedback_file(self.simulation_file_name)

        # For demonstration
        event = {"id": 1, "categorie": "highest", "time": "14:03:10", "alerts": ['optic_bl_white', 'acoustic', 'sms'], "message": "Die Sicherung der Kaffeemaschine \n ist durchgebrannt!"}
        self.trigger_button = Button(self.center_frame, command=lambda: self.test_warning(), text="Warnung testen", height=2, background="#000000", foreground="white", font=("Calibri", 25))

        self.alert_dialog = Alert_Dialog(self.simulation_file_name, self.feedback_file_name)
        self.feedback_dialog = Feedback_Dialog(self.simulation_file_name, self.feedback_file_name)
        self.create_dialog()

        # Connect to GSM hat
        connect_to_gsm_hat()

        self.window.mainloop()

    def get_file_name(self):
        today_date = datetime.datetime.today().strftime('%Y%m%d')
        simulations = [f for f in listdir('/home/pi/masterthesis/resources/simulations')]
        for simulation in simulations:
            if today_date in str(simulation):
                self.logger.info("Load simulation file: {}".format(simulation_file_path + 'simulation_' + today_date + '.json'))
                return simulation_file_path + 'simulation_' + today_date + '.json'
        logger.info("Load simulation file: {}".format(simulation_file_path + 'TestSimulation.json'))
        return simulation_file_path + 'TestSimulation.json'

    def dispatch_alarm(self, match, schedule):
        event = match[1]
        # Check if other alarm is running
        if (self.alert_dialog.alert_runs):
            logger.info("Main: Event with ID {} was missed because another alarm was still running".format(event["id"]))
            return
        # Check if feedback dialog is still open
        if (self.feedback_dialog.runs):
            logger.info("Main: Event with ID {} was missed because feedback collection from previous alarm was still running".format(event["id"]))
            return
        # Check if execution time is in the past
        #if ((execution_date + dt.timedelta(seconds=2)) < dt.datetime.now()):
        #    logger.info("Main: Event with ID {} was missed because the execution time is in the past".format(event["id"]))
        #    return
        # Check if study is paused
        if (self.block_execution):
            minutes = random.randint(20, 600)
            new_timedelta = dt.timedelta(minutes=minutes)
            schedule.once(new_timedelta, self.dispatch_alarm, args=(match, schedule))
            logger.info("Main: Event with ID {} was missed because the study was paused".format(event["id"]))
            logger.info("Main: Event with ID {} was rescheduled for {} minutes".format(event["id"], minutes))
            return
        # Check if alarm is during rest time
        if (is_time_between(self.simulation['user_data']['rest_time_start'], self.simulation['user_data']['rest_time_end'])):
            minutes = random.randint(20, 600)
            new_timedelta = dt.timedelta(minutes=minutes)
            schedule.once(new_timedelta, self.dispatch_alarm, args=(match, schedule))
            logger.info("Main: Event with ID {} was missed because the alarm was during the rest time".format(event["id"]))
            logger.info("Main: Event with ID {} was rescheduled for {} minutes".format(event["id"], minutes))
        else:
            self.alert_dialog.dispatch_event(event, self.feedback_dialog)

    def setup_scheduler(self):
        schedule = Scheduler()

        # Match times with events
        dates = self.simulation['dates']
        events = self.simulation['events']
        matches = match_times_with_events(dates, events)

        for match in matches:
            time_array = match[0]['timedelta'].split(':')
            #date_array = match[0]['date'].split('-')
            #execution_date = dt.datetime(year=int(date_array[0]), month=int(date_array[1]), day=int(date_array[2]),
            #              hour=int(time_array[0]), minute=int(time_array[1]), second=int(time_array[2]))
            timedelta = dt.timedelta(hours=int(time_array[0]), minutes=int(time_array[1]), seconds=int(time_array[2]))
            schedule.once(timedelta, self.dispatch_alarm, args=(match, schedule))

        print(schedule)
        return schedule

    def run_simulation(self):
        simulation_runs = True
        schedule = Scheduler()
        schedule = self.setup_scheduler()
        while simulation_runs:
            schedule.exec_jobs()
            if (len(schedule.get_jobs()) == 0):
                simulation_runs = False
            time.sleep(1)
        self.finish_simulation()

    def finish_simulation(self):
        # Change GUI
        self.text_frame.pack_forget()
        self.checkout_button.pack_forget()
        self.trigger_button.pack_forget()
        self.finish_label.pack(ipady=30)

        self.logger.info("Main: End program at {}".format(dt.datetime.now()))

    def run_simulation_threat(self):
        self.logger.info("Main: Simulation started at {}".format(dt.datetime.now()))

        # Change GUI
        self.text_frame.pack()
        self.label1.pack(pady=20, side=LEFT)
        self.label2.pack(pady=20, side=LEFT)
        self.start_button.pack_forget()
        self.checkout_button.pack()

        # Init and start thread
        simulation_thread = threading.Thread(target=self.run_simulation)
        simulation_thread.start()

    def test_warning(self):
        # Trigger test event
        event = {"id": 0, "alerts": ['optic_red', 'acoustic', 'sms'], "message": "Das ist ein Test Event. \n Im folgenden können Sie sich mit den \n Feedback Fragen vertraut machen."}
        self.dispatch_alarm(event, dt.datetime.now())

        # Change GUI
        self.trigger_button.pack_forget()
        self.start_button.pack(pady=10)

    def change_study_status(self):
        if (not self.block_execution):
            self.logger.info("Main: Study paused at {}".format(dt.datetime.now()))
            self.block_execution = True
            self.label2["text"] = "Studie unterbrochen"
            self.checkout_button["text"] = "Check In"
            self.label2.config(fg="red")
        else:
            self.logger.info("Main: Study continued at {}".format(dt.datetime.now()))
            self.block_execution = False
            self.label2["text"] = "Studie läuft"
            self.label2.config(fg="green")
            self.checkout_button["text"] = "Check Out"
        self.window.update()

    def create_dialog(self):
        self.window.title('Smart Home Systems Study')

        # Make root window full screen
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.attributes('-fullscreen', True)
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.bind("<Escape>", lambda e: self.window.destroy())

        self.center_frame.pack(expand=TRUE, ipady=50)

        self.img_label.pack(pady=10)

        #self.start_button.pack(side=LEFT, pady=10, padx=10)
        self.trigger_button.pack(side=LEFT, padx=10)



root = tk.Tk()
root.withdraw()
dialog = Main_Dialog()
