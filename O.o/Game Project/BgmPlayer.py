import pygame
from Settings import *

class BgmPlayer():
    def __init__(self):
        ##### Your Code Here ↓ #####
        pygame.mixer.init()
        ##### Your Code Here ↑ #####


    def play(self, loop=-1):
        ##### Your Code Here ↓ #####
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loop)
        ##### Your Code Here ↑ #####

    def stop(self):
        ##### Your Code Here ↓ #####
        pygame.mixer.music.stop()
        ##### Your Code Here ↑ #####

    def update(self, GOTO = GameState.MAIN_MENU):
        ##### Your Code Here ↓ #####
        self.stop()
        if GOTO == SceneType.CITY:
            pygame.mixer.music.load(GamePath.bgm[0])
        elif GOTO == SceneType.WILD:
            pygame.mixer.music.load(GamePath.bgm[1])
        elif GOTO == SceneType.BOSS:
            pygame.mixer.music.load(GamePath.bgm[2])
        elif GOTO == SceneType.VICTORY:
            pygame.mixer.music.load(GamePath.bgm[4])
        elif GOTO == SceneType.DEFEAT:
            pygame.mixer.music.load(GamePath.bgm[5])
        else:
            pygame.mixer.music.load(GamePath.bgm[3])
        self.play()
        ##### Your Code Here ↑ #####


    
