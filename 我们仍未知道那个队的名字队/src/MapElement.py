import pygame

from Setting import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos = (0, 0), width=TileSettings.tileLength, height=TileSettings.tileLength):
        super().__init__()
        #self.image = pygame.image.load(image)
        #self.image = pygame.transform.scale(image, (width, height))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Portal(pygame.sprite.Sprite):
    def __init__(self, image, pos = (0, 0), width=TileSettings.tileLength, height=TileSettings.tileLength, target = None):
        super().__init__()
        #self.image = pygame.image.load(image)
        #self.image = pygame.transform.scale(image, (width, height))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.portalTarget = target