import pygame
from Settings import *

class BgmPlayer:
    def __init__(self):
        pass
     
    def play(self,index):
        pygame.mixer.init()
        pygame.mixer.music.load(GamePath.music[index])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)

    def stop(self):
        pygame.mixer.quit()




    
