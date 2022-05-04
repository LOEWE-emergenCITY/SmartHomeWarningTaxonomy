import pygame

def execute_acoustic_warning(text):

    flag = True
    while flag:
        pygame.mixer.init()
        pygame.mixer.music.load("mixkit-classic-alarm-995.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue