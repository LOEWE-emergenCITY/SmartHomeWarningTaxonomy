import tkinter
from tkinter import messagebox

parent = tkinter.Tk() # Create the object
parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
parent.withdraw() # Hide the window as we do not want to see this one

yesno = messagebox.askyesno('Question Title', 'Are you sure you want to undo?', parent=parent) # Yes / No