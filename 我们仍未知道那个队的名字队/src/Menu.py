import pygame
from Event import GameEvent
from Setting import WindowSettings, GamePath
class Menu:
    def __init__(self) -> None:
        self.BGM = GamePath.bgmMainMenu
        self.image = pygame.image.load(GamePath.MainMenu)
        self.image = pygame.transform.scale(self.image, (WindowSettings.width, WindowSettings.height))
        self.displaySurface = pygame.display.get_surface()

    def update(self, keyDown):
        if keyDown == pygame.K_RETURN:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH, target = 'Home'))

    def render(self):
        self.displaySurface.blit(self.image, (0, 0))