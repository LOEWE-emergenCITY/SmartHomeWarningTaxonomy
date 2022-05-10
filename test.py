from cmath import exp
import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title('Smart Home Systems Study')

# Make root window full screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.attributes('-fullscreen', True)
root.geometry("%dx%d+0+0" % (w, h))
root.bind("<Escape>", lambda e: root.quit())

center_frame = tk.Frame(width=400, height=300)
center_frame.pack(expand=TRUE, ipady=100)

label = Label(center_frame, text="Das ist ein Beispiel Alarm", font=("Calibri", 44))
label.pack()

rating_frame = tk.Frame(center_frame, width=400, height=100)
rating_frame.pack(ipady=50)

# Rating Scale
left_label = Label(rating_frame, text="Völlig ungeeignet", font=("Calibri", 24))
left_label.pack(side=LEFT)

selected = tk.StringVar()
r1 = Radiobutton(rating_frame, text='', value='Value 1', variable=selected)
r1.pack(side=LEFT, expand=TRUE)
r2 = Radiobutton(rating_frame, text='', value='Value 2', variable=selected)
r2.pack(side=LEFT)
r3 = Radiobutton(rating_frame, text='', value='value 3', variable=selected)
r3.pack(side=LEFT)

right_label = Label(rating_frame, text="Absolut passend", font=("Calibri", 24))
right_label.pack(side=LEFT)


root.mainloop()
