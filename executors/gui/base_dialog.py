import tkinter as tk
from tkinter import *

# To make it run on pi via ssh: export DISPLAY=":0"

class Base_Dialog:

    state = "Studie läuft"
    
    def __init__(self, event):
        self.study_runs = True
        self.stop_alert = False

    def change_study_status(self, label2, checkout_button):
        if (self.study_runs):
            self.study_runs = False
            label2["text"] = "Studie unterbrochen"
            checkout_button["text"] = "Check In"
            label2.config(fg="red")
        else:
            self.study_runs = True
            label2["text"] = "Studie läuft"
            label2.config(fg="green")
            checkout_button["text"] = "Check Out"
        #self.study_status = "Studie unterbrochen"
        #root.destroy()

    def load_font_color(self):
        if (self.study_status == "Studie läuft"):
            return 'green'
        return "red"
    
    def create_dialog(self):
        root = tk.Tk()
        root.title('Smart Home Systems Study')

        # Make root window full screen
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.attributes('-fullscreen', True)
        root.geometry("%dx%d+0+0" % (w, h))
        root.bind("<Escape>", lambda e: root.quit())

        center_frame = tk.Frame(width=400, height=300)
        center_frame.pack(expand=TRUE, ipady=50)

        img = PhotoImage(file='/home/pi/masterthesis/executors/gui/peasec_logo.png')
        #img = PhotoImage(file='executors\gui\peasec_logo.png')
        label = Label(center_frame, image=img)
        label.pack()

        text_frame = tk.Frame(center_frame)
        text_frame.pack()

        label1 = Label(text_frame, text="Status: ", font=("Calibri", 20))
        label1.pack(pady=20, side=LEFT)
        label2 = Label(text_frame, text="Studie läuft", fg="green", font=("Calibri", 20))
        label2.pack(pady=20, side=LEFT)

        checkout_button = Button(center_frame, command=lambda : self.change_study_status(label2, checkout_button), text="Check-Out", background="#000000", foreground="white", font=("Calibri", 25))   
        checkout_button.pack(pady=20)

        root.mainloop()

dialog = Base_Dialog('test')
dialog.create_dialog()