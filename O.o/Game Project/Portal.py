# -*- coding:utf-8 -*-

from Settings import *

import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, GOTO:SceneType):
        super().__init__()
        
        ##### Your Code Here ↓ #####
        self.image = pygame.image.load(GamePath.portal)
        self.image = pygame.transform.scale(self.image, (PortalSettings.width, PortalSettings.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.sceneType = GOTO
        ##### Your Code Here ↑ #####
    
    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        self.rect = self.rect.move(dx, dy)
        window.blit(self.image, self.rect)
        ##### Your Code Here ↑ #####

