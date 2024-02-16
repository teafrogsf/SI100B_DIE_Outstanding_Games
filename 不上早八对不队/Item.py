import pygame
from Settings import *
from Settings import BackpackSettings
class item(pygame.sprite.Sprite):
    def __init__(self, img, x, y, width = BackpackSettings.item_size, height = BackpackSettings.item_size):
        super().__init__()
        ##### Your Code Here ↓ #####
        self.image = pygame.transform.scale(img, (width, height))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.text = ''
        self.name = ''
        self.select = pygame.image.load(GamePath.select)
        self.select = pygame.transform.scale(self.select, (width,height))
        self.healing = 0
        self.attack = 0
        self.poison = 0
        self.notusable = False
        self.wand = False
        ##### Your Code Here ↑ #####
    
    def draw(self, window, is_selected : bool,dx=0, dy=0,):
        ##### Your Code Here ↓ #####

        if is_selected:
            window.blit(self.select,(self.rect.x+dx,self.rect.y+dy))
        window.blit(self.image,(self.rect.x+dx,self.rect.y+dy))
        ##### Your Code Here ↑ #####