# -*- coding:utf-8 -*-

from Settings import *
import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, globalX, globalY):
        super().__init__()
        self.image = pygame.image.load(PortalImagePath.portal)
        self.image = pygame.transform.scale(self.image,
                            (PortalSettings.portalWidth, 
                             PortalSettings.portalHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (globalX, globalY)
        self.globalX=globalX
        self.globalY=globalY