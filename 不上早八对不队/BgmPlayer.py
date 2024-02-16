import pygame
from Settings import *

class BgmPlayer():
    def __init__(self):
        ##### Your Code Here ↓ #####
        pygame.mixer.music.load(GamePath.bgm)
        ##### Your Code Here ↑ #####


    def play(self, loop=-1):
        ##### Your Code Here ↓ #####
        pygame.mixer.music.play(loop)
        ##### Your Code Here ↑ #####

    def stop(self):
        ##### Your Code Here ↓ #####
        pygame.mixer.music.stop()
        ##### Your Code Here ↑ #####

    def update(self, GOTO):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####


    
