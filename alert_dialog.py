from os import abort
import tkinter as tk
from tkinter import *
import threading
import json
import time
import datetime as dt
from alerts import trigger_acoustic_alert
from alerts import trigger_optical_alert

# To make it run on pi via ssh: export DISPLAY=":0"

QUESTIONS_FILE_NAME = "executors/gui/questions.json"
MAX_ALERT_RUNNING_TIME = 50

class Alert_Dialog:
    def __init__(self):
        self.window = tk.Toplevel()
        self.event = {"id": 0, "categorie": "", "time": "", "alerts": [], "message": ""}
        self.alert_runs = False
        self.stop_alert = False
        self.alert_threads = []
        self.questions = self.load_questions()
        self.create_dialog()
        self.window.withdraw()

    # This method measures the time an alert is running and terminates it when it exceeds the maximum time
    def measure_alarm_time(self):
        start_time = dt.datetime.now()
        end_time = start_time + dt.timedelta(seconds=MAX_ALERT_RUNNING_TIME)
        while self.alert_runs:
            time.sleep(1)
            if (end_time < dt.datetime.now()):
                print("Alert    : Alarm forced to terminate. Endtime: {}, Now: {}".format(end_time, dt.datetime.now()))
                self.terminate_alert()
                break

    def dispatch_event(self, event):
        print("Alert    : Dispatch event with ID {}".format(event["id"]))
        self.alert_runs = True
        self.stop_alert = False
        self.event = event
        self.text_label['text'] = event['message']
        self.text_label.update()
        self.window.deiconify()
        self.switchOn_alerts(event['alerts'])
        time_thread = threading.Thread(target=self.measure_alarm_time)
        time_thread.start()

    def load_questions(self):
        questions_json = open(QUESTIONS_FILE_NAME)
        questions = json.load(questions_json)
        return questions['questions']

    def store_rating(self):
        # TODO: Store rating
        self.terminate_alert()

    def switchOn_alerts(self, alerts):
        for alert in alerts:
            if alert == 'acoustic':
                sound_threat = threading.Thread(target=trigger_acoustic_alert, args=(id, lambda: self.stop_alert))
                sound_threat.start()
                self.alert_threads.append(sound_threat)
            if alert == 'optic':
                optical_threat = threading.Thread(target=trigger_optical_alert, args=(id, lambda: self.stop_alert))
                optical_threat.start()
                self.alert_threads.append(optical_threat)
            if alert == 'email':
                return
            if alert == 'sms':
                return

    def switchOff_alerts(self):
        self.stop_alert = True
        for thread in self.alert_threads:
            thread.join()
        self.alert_threads = []

    def terminate_alert(self):
        self.alert_runs = False
        self.switchOff_alerts()
        self.window.withdraw()
        print("Alert    : End event with ID {}".format(self.event["id"]))
    
    def create_dialog(self):
        self.window.title('Smart Home Systems Study')

        # Make root window full screen
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        #window.attributes('-fullscreen', True)
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.bind("<Escape>", lambda e: self.window.quit())

        center_frame = tk.Frame(self.window, width=400, height=300)
        center_frame.pack(expand=TRUE, ipady=50)

        self.text_label = Label(center_frame, text=self.event["message"], font=("Calibri", 44))
        self.text_label.pack(pady=20)

        #rating_frame = tk.Frame(center_frame, width=400, height=100)
        #rating_frame.pack(ipady=50)

        # Rating Scale
        #label1 = Label(rating_frame, text="Bitte bewerte, ob du den Warnkanal für das Ereignis als angemessen empfindest.", font=("Calibri", 14))
        #label1.pack(side=TOP)

        #label2 = Label(rating_frame, text="1 = völlig ungeeignet, 5 = absolut passend", font=("Calibri", 14))
        #label2.pack(side=TOP)

        #button1 = Button(rating_frame, text='1', command=lambda : self.store_rating(), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        #button1.pack(side=LEFT, padx=20)
        #button2 = Button(rating_frame, text='2', command=lambda : self.store_rating(), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        #button2.pack(side=LEFT, padx=20)
        #button3 = Button(rating_frame, text='3', command=lambda : self.store_rating(), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        #button3.pack(side=LEFT, padx=20)
        #button4 = Button(rating_frame, text='4', command=lambda : self.store_rating(), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        #button4.pack(side=LEFT, padx=20)
        #button5 = Button(rating_frame, text='5', command=lambda : self.store_rating(), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        #button5.pack(side=LEFT, padx=20)

        acknowledge_button = Button(center_frame, command=lambda : self.store_rating(), text="Alarm wurde wahrgenommen", background="#000000", foreground="white", font=("Calibri", 25))   
        acknowledge_button.pack(pady=50)

        abort_button = Button(center_frame, command=lambda : self.switchOff_alert(self.window), text="Alarm ausschalten \n (Achtung! Nicht für Studienteilnehmer)", background="#7F7A7A", foreground="white", font=("Calibri", 25))   
        abort_button.pack()
        #checkout_button = Button(center_frame, command=lambda : self.switchOff_alert(root), text="Check-Out", background="#000000", foreground="white", font=("Calibri", 25))   
        #checkout_button.pack(side=RIGHT)

        #self.window.mainloop()

#root = tk.Tk()
#root.withdraw()
#event = {"id": 1, "categorie": "highest", "time": "17:02:20", "alerts": ["acoustic"], "message": "Die Sicherung der Kaffeemaschine ist durchgebrannt!"}
#dialog = Alert_Dialog()
#dialog.dispatch_event(event)