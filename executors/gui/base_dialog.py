import tkinter as tk
from tkinter import *
from executors.gui.alert_dialog import Alert_Dialog

# To make it run on pi via ssh: export DISPLAY=":0"

class Base_Dialog:

    state = "Studie läuft"
    
    def __init__(self):
        self.study_runs = True
        self.block_execution = False

        # GUI components
        self.window = tk.Toplevel()
        self.center_frame = tk.Frame(self.window, width=400, height=300)
        #self.img = PhotoImage(file='/home/pi/masterthesis/executors/gui/peasec_logo.png')
        self.img = PhotoImage(file='executors\gui\peasec_logo.png')
        self.img_label = Label(self.center_frame, image=self.img)

        self.create_dialog()

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
        self.window.update()
        #self.study_status = "Studie unterbrochen"
        #root.destroy()

    def trigger_mainloop(self):
        self.window.mainloop()

    def get_window(self):
        return self.window

    def dispatch_alert_dialog(self, event):
        Alert_Dialog(event)

    def set_block_execution(self):
        self.block_execution = True

    def set_unblock_execution(self):
        self.block_execution = False
    
    def create_dialog(self):
        self.window.title('Smart Home Systems Study')

        # Make root window full screen
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        #self.window.attributes('-fullscreen', True)
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.bind("<Escape>", lambda e: self.window.quit())

        self.center_frame.pack(expand=TRUE, ipady=50)

        self.img_label.pack(pady=10)

        text_frame = tk.Frame(self.center_frame)
        text_frame.pack()

        label1 = Label(text_frame, text="Status: ", font=("Calibri", 20))
        label1.pack(pady=20, side=LEFT)
        label2 = Label(text_frame, text="Studie läuft", fg="green", font=("Calibri", 20))
        label2.pack(pady=20, side=LEFT)

        checkout_button = Button(self.center_frame, command=lambda : self.change_study_status(label2, checkout_button), text="Check-Out", height=2, background="#000000", foreground="white", font=("Calibri", 25))   
        checkout_button.pack(pady=20)

        #self.window.mainloop()

#root = tk.Tk()
#root.withdraw()
#dialog = Base_Dialog()
#dialog.create_dialog()