import pygame
from gui.alert_dialog import Alert_Dialog
from threading import Thread

# To make it run on pi via ssh: export DISPLAY=":0"

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
    print('start')
    stop_sound = False
    for id in range(0,1):
        sound = Thread(target=play_sound, args=(id, lambda: stop_sound))
        sound.start()

    dialog = Alert_Dialog("Das ist ein Test")
    dialog.create_dialog()

    #parent = tkinter.Tk()  # Create the object
    #parent.overrideredirect(1)
    #parent.withdraw()  # Hide the window as we do not want to see this one
    #answer = askyesno("test", "test 123", parent=parent)

    if dialog.stop_alert:
        stop_sound = True

execute_acoustic_warning('test')
