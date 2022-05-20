import tkinter as tk
from tkinter import *

# To make it run on pi via ssh: export DISPLAY=":0"

class Base_Dialog:
    def __init__(self, event):
        self.event = event
        self.stop_alert = False

    def check_out(self, root):
        root.destroy()
    
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

        img = PhotoImage(file='executors\gui\peasec_logo.png')

        label = Label(center_frame, image=img)
        label.pack(pady=20)

        checkout_button = Button(center_frame, command=lambda : self.check_out(root), text="Check-Out", background="#000000", foreground="white", font=("Calibri", 25))   
        checkout_button.pack(pady=50)

        root.mainloop()

dialog = Base_Dialog('test')
dialog.create_dialog()