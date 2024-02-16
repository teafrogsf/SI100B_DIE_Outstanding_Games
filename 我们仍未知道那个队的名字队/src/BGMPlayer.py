import pygame
from Setting import GamePath
class BGMPlayer:
    def __init__(self,file:str):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(0.5)
    def play(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
