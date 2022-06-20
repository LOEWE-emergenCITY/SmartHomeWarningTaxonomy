
from tkinter import *
from tkinter.ttk import Progressbar
from util import save_feedback
import json
import time
import logging

QUESTIONS_FILE_NAME = "questions.json"

class Feedback_Dialog():
    def __init__(self):
        self.logger = logging.getLogger('main')
        self.runs = False
        self.questions = self.load_questions()
        self.event = {"id": 0, "categorie": "", "time": "", "alerts": [], "message": ""}
        self.step = 1
        self.total_steps = len(self.questions)
        self.progress_value = 1/self.total_steps * 100
        self.feedback = []

        # Create GUI
        self.feedback_dialog = Toplevel()
        self.center_frame = Frame(self.feedback_dialog, width=400, height=300)
        self.rating_frame = Frame(self.center_frame, width=400, height=100)
        self.question_label = Label(self.rating_frame, text=self.questions[0]['question'], font=("Calibri bold", 16))
        self.progress_frame = Frame(self.center_frame)
        self.progress_bar = Progressbar(self.progress_frame, orient='horizontal', length=300, mode='determinate')
        self.progress_label = Label(self.progress_frame, text="Frage {} von {} ".format(self.step, self.total_steps))

        self.create_dialog()
        self.feedback_dialog.withdraw()
        
    def collect_feedback(self, event):
        self.logger.info("Feedback: Start collecting feedback for event with ID {}".format(event["id"]))
        self.event = event
        self.runs = True
        self.feedback_dialog.deiconify()
        
    def store_rating(self, answer):
        if self.step != self.total_steps:
            self.feedback.append(answer)
            self.question_label['text'] = self.questions[self.step]['question']
            self.step = self.step + 1
            self.progress_value = self.step/self.total_steps * 100
            self.progress_bar['value'] = self.progress_value
            self.progress_label['text'] = "Frage {} von {} ".format(self.step, self.total_steps)
            self.feedback_dialog.update()
        else:
            # Collect and store feedback
            self.feedback.append(answer)
            save_feedback(self.event['id'], self.feedback)

            # Adapt GUI
            self.question_label['text'] = self.questions[0]['question']
            self.step = 1
            self.progress_value = self.step/self.total_steps * 100
            self.progress_bar['value'] = self.progress_value
            self.progress_label['text'] = "Frage {} von {} ".format(self.step, self.total_steps)

            # Set flag and hide dialog
            self.runs = False
            self.feedback_dialog.withdraw()
            self.logger.info("Feedback: Finish collecting feedback for event with ID {}".format(self.event["id"]))

    def load_questions(self):
        with open(QUESTIONS_FILE_NAME, encoding='utf-8') as questions_json:
            questions = json.load(questions_json)
            return questions['questions']

    def create_dialog(self):
        self.feedback_dialog.title("Feedback")
        w, h = self.feedback_dialog.winfo_screenwidth(), self.feedback_dialog.winfo_screenheight()
        #window.attributes('-fullscreen', True)
        self.feedback_dialog.geometry("%dx%d+0+0" % (w, h))

        self.center_frame.pack(expand=TRUE, ipady=50)

        # Rating Scale
        self.rating_frame.pack(ipady=20)

        self.question_label.pack(side=TOP, ipady=10)

        label2 = Label(self.rating_frame, text="1 = völlig ungeeignet, 5 = absolut passend", font=("Calibri", 14))
        label2.pack(side=TOP)

        button1 = Button(self.rating_frame, text='1', command=lambda : self.store_rating(1), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button1.pack(side=LEFT, padx=20)
        button2 = Button(self.rating_frame, text='2', command=lambda : self.store_rating(2), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button2.pack(side=LEFT, padx=20)
        button3 = Button(self.rating_frame, text='3', command=lambda : self.store_rating(3), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button3.pack(side=LEFT, padx=20)
        button4 = Button(self.rating_frame, text='4', command=lambda : self.store_rating(4), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button4.pack(side=LEFT, padx=20)
        button5 = Button(self.rating_frame, text='5', command=lambda : self.store_rating(5), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button5.pack(side=LEFT, padx=20)

        # Progress Label
        self.progress_frame.pack(pady=30)

        self.progress_bar['value'] += self.progress_value
        self.progress_bar.pack()

        self.progress_label.pack()

#question = "Wie finden sie das das so und so läuft?"
#dialog = Feedback_Dialog()
#time.sleep(2)
#dialog.collect_feedback()
#time.sleep(5)