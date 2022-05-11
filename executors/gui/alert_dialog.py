import tkinter as tk
from tkinter import *

# To make it run on pi via ssh: export DISPLAY=":0"

class Alert_Dialog:
    def __init__(self, event):
        self.event = event
        self.stop_alert = False

    def store_rating(self, root):
        # TODO: Store rating
        self.stop_alert = True
        root.destroy()

    def switchOff_alert(self, root):
        self.stop_alert = True
        root.destroy()
    
    def create_dialog(self):
        root = tk.Tk()
        root.title('Smart Home Systems Study')

        # Make root window full screen
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.attributes('-fullscreen', True)
        root.geometry("%dx%d+0+0" % (w, h))
        root.bind("<Escape>", lambda e: root.quit())

        abort_button = Button(root, command=lambda : self.switchOff_alert(root), text="Alarm ausschalten", background="#000000", foreground="white")   
        abort_button.place(x=1200, y=310, width=120, height=50, anchor='ne')

        center_frame = tk.Frame(width=400, height=300)
        center_frame.pack(expand=TRUE, ipady=50)
        abort_button.tkraise()

        label = Label(center_frame, text=self.event, font=("Calibri", 44))
        label.pack()

        rating_frame = tk.Frame(center_frame, width=400, height=100)
        rating_frame.pack(ipady=50)

        # Rating Scale
        label1 = Label(rating_frame, text="Bitte bewerte, ob du den Warnkanal für das Ereignis als angemessen empfindest.", font=("Calibri", 14))
        label1.pack(side=TOP)

        label2 = Label(rating_frame, text="1 = völlig ungeeignet, 5 = absolut passend", font=("Calibri", 14))
        label2.pack(side=TOP)

        button1 = Button(rating_frame, text='1', command=lambda : self.store_rating(root), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button1.pack(side=LEFT, padx=20)
        button2 = Button(rating_frame, text='2', command=lambda : self.store_rating(root), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button2.pack(side=LEFT, padx=20)
        button3 = Button(rating_frame, text='3', command=lambda : self.store_rating(root), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button3.pack(side=LEFT, padx=20)
        button4 = Button(rating_frame, text='4', command=lambda : self.store_rating(root), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button4.pack(side=LEFT, padx=20)
        button5 = Button(rating_frame, text='5', command=lambda : self.store_rating(root), width=4, height=3, background="#A53C3C", font=("Calibri", 25))
        button5.pack(side=LEFT, padx=20)

        root.mainloop()

dialog = Alert_Dialog('test')
dialog.create_dialog()