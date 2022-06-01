import tkinter as tk
from tkinter import *
import threading
import pygame
import json

# To make it run on pi via ssh: export DISPLAY=":0"

QUESTIONS_FILE_NAME = "executors/gui/questions.json"

class Alert_Dialog:
    def __init__(self, event):
        self.event = event
        self.stop_alert = False
        self.alert_threads = []
        self.questions = self.load_questions()
        print(self.questions)
        self.switchOn_alerts(event["alerts"])
        self.create_dialog()

    def load_questions(self):
        questions_json = open(QUESTIONS_FILE_NAME)
        questions = json.load(questions_json)
        return questions['questions']

    def store_rating(self, window):
        # TODO: Store rating
        #self.stop_alert = True
        self.switchOff_alerts()
        window.withdraw()
        #root.destroy()

    def switchOn_alerts(self, alerts):
        for alert in alerts:
            if alert == 'acoustic':
                sound_threat = threading.Thread(target=self.play_sound, args=(id, lambda: self.stop_alert))
                sound_threat.start()
                self.alert_threads.append(sound_threat)
            if alert == 'optic':
                return
            if alert == 'email':
                return
            if alert == 'sms':
                return

    def switchOff_alerts(self):
        self.stop_alert = True
        for thread in self.alert_threads:
            thread.join()

    def play_sound(id, self, stop):
        while True:
            pygame.mixer.init()
            pygame.mixer.music.load("mixkit-classic-alarm-995.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            if stop():
                break
    
    def create_dialog(self):
        window = tk.Toplevel()
        window.title('Smart Home Systems Study')

        # Make root window full screen
        w, h = window.winfo_screenwidth(), window.winfo_screenheight()
        #window.attributes('-fullscreen', True)
        window.geometry("%dx%d+0+0" % (w, h))
        window.bind("<Escape>", lambda e: window.quit())

        center_frame = tk.Frame(window, width=400, height=300)
        center_frame.pack(expand=TRUE, ipady=50)

        label = Label(center_frame, text=self.event["message"], font=("Calibri", 44))
        label.pack(pady=20)

        rating_frame = tk.Frame(center_frame, width=400, height=100)
        rating_frame.pack(ipady=50)

        # Rating Scale
        label1 = Label(rating_frame, text="Bitte bewerte, ob du den Warnkanal für das Ereignis als angemessen empfindest.", font=("Calibri", 14))
        label1.pack(side=TOP)

        label2 = Label(rating_frame, text="1 = völlig ungeeignet, 5 = absolut passend", font=("Calibri", 14))
        label2.pack(side=TOP)

        button1 = Button(rating_frame, text='1', command=lambda : self.store_rating(window), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button1.pack(side=LEFT, padx=20)
        button2 = Button(rating_frame, text='2', command=lambda : self.store_rating(window), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button2.pack(side=LEFT, padx=20)
        button3 = Button(rating_frame, text='3', command=lambda : self.store_rating(window), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button3.pack(side=LEFT, padx=20)
        button4 = Button(rating_frame, text='4', command=lambda : self.store_rating(window), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button4.pack(side=LEFT, padx=20)
        button5 = Button(rating_frame, text='5', command=lambda : self.store_rating(window), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button5.pack(side=LEFT, padx=20)

        abort_button = Button(center_frame, command=lambda : self.switchOff_alert(window), text="Alarm ausschalten", background="#000000", foreground="white", font=("Calibri", 25))   
        abort_button.pack()
        #checkout_button = Button(center_frame, command=lambda : self.switchOff_alert(root), text="Check-Out", background="#000000", foreground="white", font=("Calibri", 25))   
        #checkout_button.pack(side=RIGHT)

        window.mainloop()

#root = tk.Tk()
#root.withdraw()
event = {"id": 1, "categorie": "highest", "time": "17:02:20", "alerts": ["acoustic"], "message": "Die Sicherung der Kaffeemaschine ist durchgebrannt!"}
#dialog = Alert_Dialog(event)
#dialog.create_dialog()