import pygame
import tkinter
from tkinter.messagebox import askyesno
from threading import Thread


def play_sound(id, stop):
    while True:
        pygame.mixer.init()
        pygame.mixer.music.load("mixkit-classic-alarm-995.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        if stop():
            break

def execute_acoustic_warning(text):
    stop_sound = False
    for id in range(0,1):
        sound = Thread(target=play_sound, args=(id, lambda: stop_sound))
        sound.start()

    parent = tkinter.Tk()  # Create the object
    # Avoid it appearing and then disappearing quickly
    parent.overrideredirect(1)
    parent.withdraw()  # Hide the window as we do not want to see this one
    answer = askyesno("test", "test 123", parent=parent)

    if answer:
        stop_sound = True

execute_acoustic_warning('test')
