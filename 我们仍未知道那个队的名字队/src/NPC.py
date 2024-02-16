import pygame
from Setting import *
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, image) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

class KFC_NPC(NPC):
    def __init__(self, pos, image) -> None:
        super().__init__(pos, image)
        self.shopType = 'Shop_KFCBox'

class Guide_NPC(NPC):
    def __init__(self, pos, image):
        super().__init__(pos, image)
        self.dialogType = 'Dialog_GuideBox'

class Shop_NPC(NPC):
    def __init__(self, pos, image):
        super().__init__(pos, image)
        self.shopType = 'Shop_HomeBox'

class Treasure_NPC(NPC):
    def __init__(self, pos, image):
        super().__init__(pos, image)
        self.HPChange = random.choice([0.5, 0, 0.25, 0.75, 1])