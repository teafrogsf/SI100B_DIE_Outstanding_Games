# -*- coding:utf-8 -*-

from Settings import *

import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, img, x, y, FROM: SceneType,TO:SceneType):
        super().__init__()
        ##### Your Code Here ↓ #####
        self.image = img
        self.rect = self.image.get_rect(topleft = (x,y))
        ##### Your Code Here ↑ #####
    
    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        window.blit(self.image,self.rect)
        ##### Your Code Here ↑ #####
