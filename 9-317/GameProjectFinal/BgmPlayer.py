import pygame
from Settings import *

# BGM settings
class BgmPlayer():
    def __init__(self):
        self.bgm_CITY = GamePath.bgm[0]
        self.bgm_WILD = GamePath.bgm[1]
        self.bgm_BOSS = GamePath.bgm[2]
        self.bgm_SHOP = GamePath.bgm[3]
        self.bgm_HOSPITAL = GamePath.bgm[4]
        self.bgm_GYM = GamePath.bgm[5]
        self.bgm_END = GamePath.bgm[6]

    def play(self, name:GameState, loop=-1):
        if name == GameState.GAME_PLAY_CITY:
            pygame.mixer_music.load(self.bgm_CITY)
            pygame.mixer_music.play(loop)
        elif name == GameState.GAME_PLAY_WILD:
            pygame.mixer_music.load(self.bgm_WILD)
            pygame.mixer_music.play(loop)
        elif name == GameState.GAME_PLAY_BOSS:
            pygame.mixer_music.load(self.bgm_BOSS)
            pygame.mixer_music.play(loop)
        elif name == GameState.GAME_PLAY_SHOP:
            pygame.mixer_music.load(self.bgm_SHOP)
            pygame.mixer_music.play(loop)
        elif name == GameState.GAME_PLAY_HOSPITAL:
            pygame.mixer_music.load(self.bgm_HOSPITAL)
            pygame.mixer_music.play(loop)
        elif name == GameState.GAME_PLAY_GYM:
            pygame.mixer_music.load(self.bgm_GYM)
            pygame.mixer_music.play(loop)
        elif name == GameState.END_GAME:
            pygame.mixer_music.load(self.bgm_END)
            pygame.mixer_music.play(loop)
        
    def stop(self):
        pygame.mixer.music.stop

    def update(self, GOTO:GameState):
        #UPDATE CURRENT STATUS AND PLAY NEW BGM
        self.stop()
        self.play(GOTO)