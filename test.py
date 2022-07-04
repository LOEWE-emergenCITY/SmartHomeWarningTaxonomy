from textwrap import fill
import tkinter as tk
from tkinter import *

def abort_alert():
    return

root = tk.Tk()
root.withdraw()

window = tk.Toplevel()
window.title('Smart Home Systems Study')
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
#window.attributes('-fullscreen', True)
window.geometry("%dx%d+0+0" % (w, h))
window.bind("<Escape>", lambda e: window.quit())

center_frame = tk.Frame(window, width=300, height=300)
center_frame.pack(expand=TRUE, ipady=50)

text_label = Label(center_frame, width=100, text="Die Sicherung der Kaffeemaschine ist \n durchgebrant Die Sicherung ist durchgebrannt!", font=("Calibri", 30))
text_label.pack()

button_frame = tk.Frame(center_frame, width=300)
button_frame.pack(ipady=20)

acknowledge_button = Button(button_frame, command=lambda : abort_alert(), text="Alarm wahrgenommen", background="green", foreground="white", font=("Calibri", 25))   
acknowledge_button.pack(side=LEFT, padx=20)

abort_button = Button(button_frame, command=lambda : abort_alert(), text="Abbruch", background="red", foreground="white", font=("Calibri", 25))   
abort_button.pack(side=LEFT, padx=20)

window.mainloop()