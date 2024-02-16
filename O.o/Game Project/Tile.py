# -*- coding:utf-8 -*-

import pygame

from Settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, width=SceneSettings.tileWidth, height=SceneSettings.tileHeight):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, window, dx=0, dy=0):
        self.rect = self.rect.move(dx, dy)
        window.blit(self.image, self.rect)

class Tree(pygame.sprite.Sprite):  # 树木tile用于制造动画树木
    def __init__(self, images:list, x=0, y=0, width=SceneSettings.tileWidth, height=SceneSettings.tileHeight):
        super().__init__()
        self.images = [pygame.transform.scale(image, (width, height)) for image in images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, window, dx=0, dy=0):
        self.update()
        self.rect = self.rect.move(dx, dy)
        window.blit(self.image, self.rect)

    def update(self):   # 树木tile动画
        self.index = (self.index + 1 / 3) % len(self.images)
        self.image = self.images[int(self.index)]

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(GamePath.mouse), (30, 30))
        self.rect = self.image.get_rect()

    def update(self, window):
        self.rect = pygame.mouse.get_pos()
        if (ShopSettings.boxStartX < self.rect[0] < ShopSettings.boxStartX + ShopSettings.boxWidth and
                ShopSettings.boxStartY < self.rect[1] < ShopSettings.boxStartY + ShopSettings.boxHeight):
            pygame.mouse.set_visible(0)
            window.blit(self.image, self.rect)
        else:
            pygame.mouse.set_visible(1)

class Item(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (ShopSettings.itemWidth,
                                                                       ShopSettings.itemHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.ID = 0

class ShopAttack(Item):
    def __init__(self):
        super().__init__(GamePath.shopItem[1], ShopSettings.itemStartX, ShopSettings.itemStartY)
        self.ID = 1
class ShopDefence(Item):
    def __init__(self):
        super().__init__(GamePath.shopItem[2], ShopSettings.itemStartX + ShopSettings.itemGap,
                         ShopSettings.itemStartY)
        self.ID = 2
class ShopHP(Item):
    def __init__(self):
        super().__init__(GamePath.shopItem[0], ShopSettings.itemStartX + ShopSettings.itemGap * 2,
                         ShopSettings.itemStartY)
        self.ID = 3
class ShopLevel(Item):
    def __init__(self):
        super().__init__(GamePath.shopItem[3], ShopSettings.itemStartX + ShopSettings.itemGap * 3,
                         ShopSettings.itemStartY)
        self.ID = 4
class ShopExit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(GamePath.shopExit), (80, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (ShopSettings.boxStartX + 360, ShopSettings.boxStartY + 190)
        self.ID = 5
