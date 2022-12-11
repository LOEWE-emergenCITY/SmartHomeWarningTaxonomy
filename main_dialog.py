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

    state = "Study is running"

    def __init__(self):
        self.block_execution = False

        # Logger
        self.logger = setup_logger()
        self.logger.info("Main: Start program at {}".format(dt.datetime.now()))

        # GUI components
        self.window = tk.Toplevel()
        self.center_frame = tk.Frame(self.window, width=400, height=300)
        self.text_frame = tk.Frame(self.center_frame)
        self.label1 = Label(self.text_frame, text="Status: ", font=("Calibri", 20))
        self.label2 = Label(self.text_frame, text="Study is running", fg="green", font=("Calibri", 20))
        self.checkout_button = Button(self.center_frame, command=lambda: self.change_study_status(), text="Check-Out", height=2, background="#000000", foreground="white", font=("Calibri", 25))
        self.img = PhotoImage(file='/home/pi/shws/logo.png')
        self.start_button = Button(self.center_frame, command=lambda: self.run_simulation_threat(), text="Start the study", height=2, background="#000000", foreground="white", font=("Calibri", 25))
        self.img_label = Label(self.center_frame, image=self.img)
        self.error_label = Label(self.center_frame)
        self.finish_label = Label(self.center_frame, text="The study is completed. Thank you for your participation! \n The box can now be disconnected from the power supply.", font=("Calibri", 17))

         # Load Simulation
        self.simulation_file_name = self.get_file_name()
        self.simulation = load_simulation(self.simulation_file_name)
        self.missed_events = []

        # Setup files
        self.feedback_file_name = init_feedback_file(self.simulation_file_name)

        # For demonstration
        event = {"id": 1, "categorie": "highest", "time": "14:03:10", "alerts": ['optic_bl_white', 'acoustic', 'sms'], "message": "The fuse of the coffee machine \n is blown!"}
        self.trigger_button = Button(self.center_frame, command=lambda: self.test_warning(), text="Test warning", height=2, background="#000000", foreground="white", font=("Calibri", 25))

        self.alert_dialog = Alert_Dialog(self.simulation_file_name, self.feedback_file_name)
        self.feedback_dialog = Feedback_Dialog(self.simulation_file_name, self.feedback_file_name)
        self.create_dialog()

        # Connect to GSM hat
        connect_to_gsm_hat()

        self.window.mainloop()

    def get_file_name(self):
        today_date = datetime.datetime.today().strftime('%Y%m%d')
        simulations = [f for f in listdir('/home/pi/shws/resources/simulations')]
        for simulation in simulations:
            if today_date in str(simulation):
                self.logger.info("Load simulation file: {}".format(simulation_file_path + 'simulation_' + today_date + '.json'))
                return simulation_file_path + 'simulation_' + today_date + '.json'
        logger.info("Load simulation file: {}".format(simulation_file_path + 'TestSimulation.json'))
        return simulation_file_path + 'TestSimulation.json'

    def dispatch_alarm(self, match, schedule, is_test):
        event = match[1]
        if is_test:
            self.alert_dialog.dispatch_event(event, self.feedback_dialog)
            return
        # Check if other alarm is running
        if (self.alert_dialog.alert_runs):
            self.missed_events.append(match)
            logger.info("Main: Event with ID {} was missed because another alarm was still running".format(event["id"]))
            return
        # Check if feedback dialog is still open
        if (self.feedback_dialog.runs):
            self.missed_events.append(match)
            logger.info("Main: Event with ID {} was missed because feedback collection from previous alarm was still running".format(event["id"]))
            return
        # Check if study is paused
        if (self.block_execution):
            self.missed_events.append(match)
            logger.info("Main: Event with ID {} was missed because the study was paused".format(event["id"]))
            return
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
            timedelta = dt.timedelta(hours=int(time_array[0]), minutes=int(time_array[1]), seconds=int(time_array[2]))
            schedule.once(timedelta, self.dispatch_alarm, args=(match, schedule, False))

        print(schedule)
        return schedule

    def run_simulation(self):
        simulation_runs = True
        schedule = Scheduler()
        schedule = self.setup_scheduler()
        while simulation_runs:
            if len(self.missed_events) != 0:
                for match in self.missed_events:
                    minutes = random.randint(20, 180)
                    new_timedelta = dt.timedelta(minutes=minutes)
                    schedule.once(new_timedelta, self.dispatch_alarm, args=(match, schedule, False))
                    logger.info("Main: Event with ID {} was rescheduled for {} minutes".format(match[1]['id'], minutes))
                    self.missed_events.remove(match)
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
        event = {"id": 0, "alerts": ['optic_red', 'acoustic', 'sms'], "message": "This is a test event. \n Below you can familiarize yourself with the \n feedback questions."}
        match = [{}, event]
        self.dispatch_alarm(match, {}, True)

        # Change GUI
        self.trigger_button.pack_forget()
        self.start_button.pack(pady=10)

    def change_study_status(self):
        if (not self.block_execution):
            self.logger.info("Main: Study paused at {}".format(dt.datetime.now()))
            self.block_execution = True
            self.label2["text"] = "Study paused"
            self.checkout_button["text"] = "Check In"
            self.label2.config(fg="red")
        else:
            self.logger.info("Main: Study continued at {}".format(dt.datetime.now()))
            self.block_execution = False
            self.label2["text"] = "Study is running"
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

        self.trigger_button.pack(side=LEFT, padx=10)



root = tk.Tk()
root.withdraw()
dialog = Main_Dialog()
