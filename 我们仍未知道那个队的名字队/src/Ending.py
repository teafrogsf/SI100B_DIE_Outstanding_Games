import pygame
from Event import GameEvent
from Setting import WindowSettings, GamePath

class GameOverScene:
    def __init__ (self, window):
        self.window = window
        self.BGM = GamePath.bgmGameOver
        self.image = pygame.image.load(GamePath.GameOver)
        self.image = pygame.transform.scale(self.image, (WindowSettings.width, WindowSettings.height))
    
    def update(self, keyDown):
        if keyDown == pygame.K_RETURN:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_RESTART))
    
    def render(self):
        self.window.blit(self.image, (0, 0))

class GameWinScene:
    def __init__ (self, window):
        self.window = window
        self.BGM = GamePath.bgmGameWin
        self.image = pygame.image.load(GamePath.GameWin)
        self.image = pygame.transform.scale(self.image, (WindowSettings.width, WindowSettings.height))
    
    def update(self, keyDown):
        if keyDown == pygame.K_RETURN:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_RESTART))
    
    def render(self):
        self.window.blit(self.image, (0, 0))
