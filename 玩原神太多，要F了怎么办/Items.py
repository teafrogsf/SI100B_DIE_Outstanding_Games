# -*- coding:utf-8 -*-

import pygame

from Settings import *

class Items(pygame.sprite.Sprite):
    def __init__(self, image, x, y) -> None:
        super().__init__()
        self.layer = 0                      # 三层图层，0是最底层 
        self.image = image
        self.isObstacle = False
        self.canInteract = False
        self.interactType = 0               # 0: 对话框, 1: 战斗 
        self.catergory = None
        self.ID = ""
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def topleft(self):
        return self.rect.topleft

class Grounds(Items):
    def __init__(self, image, x, y) -> None:
        super().__init__(image, x, y)
        self.catergory = "Ground"

class Trees(Items):
    def __init__(self, image, x, y) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.isObstacle = True
        self.catergory = "Tree"
        self.rect = pygame.Rect(x,y + MapSettings.treeDeltaY + MapSettings.treeDeltaRect,
                                MapSettings.treeWidth,
                                MapSettings.treeHeight - MapSettings.treeDeltaY - MapSettings.treeDeltaRect)

    def topleft(self):
        return (self.rect.x, self.rect.y - MapSettings.treeDeltaY - MapSettings.treeDeltaRect)

class Bushes(Items):
    def __init__(self, image, x, y) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.isObstacle = True
        self.catergory = "Bush"

class Flowers(Items):
    def __init__(self, image, x, y) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.isObstacle = False
        self.catergory = "Flower"

class Grasses(Items):
    def __init__(self, image, x, y) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.catergory = "Grass"

class Boards(Items):
    def __init__(self, image, x, y, ID) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.catergory = "Board"
        self.canInteract = True
        self.ID = ID

class Bells(Items):
    def __init__(self, image, x, y, ID) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.catergory = "Bell"
        self.canInteract = True
        self.isObstacle = True
        scale = BellSettings.scale
        self.rect = pygame.Rect(x,y + BellSettings.safeZone,
                                BellSettings.scale[0],
                                BellSettings.scale[1] - BellSettings.safeZone)
        self.ID = ID
    
    def topleft(self):
        return (self.rect.x, self.rect.y - BellSettings.safeZone)
    
class Specials(Items):
    def __init__(self, image, x, y, width, height, rect_width, rect_height) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.isObstacle = True
        self.width = width
        self.height = height
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.catergory = "Special"
        self.rect = pygame.Rect(x + (width - rect_width) // 2,y + height - rect_height,
                                rect_width, rect_height)

    def topleft(self):
        return (self.rect.x - (self.width - self.rect_width) // 2, self.rect.y - (self.height - self.rect_height))
    
class Shops(Items):
    def __init__(self, image, x, y, ID) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.canInteract = True
        self.isObstacle = True
        self.catergory = "Shop"
        self.ID = ID
        self.rect = pygame.Rect(x + (FigureSettings.width - FigureSettings.rect_width) // 2,
                                y + FigureSettings.height - FigureSettings.rect_height,
                                FigureSettings.rect_width, FigureSettings.rect_height)

    def topleft(self):
        return (self.rect.x - (FigureSettings.width - FigureSettings.rect_width) // 2,
                self.rect.y - (FigureSettings.height - FigureSettings.rect_height))
    
class Enemies(Items):
    def __init__(self, image, x, y, ID) -> None:
        super().__init__(image, x, y)
        self.layer = 1
        self.canInteract = True
        self.isObstacle = True
        self.catergory = "Enemy"
        self.ID = ID
        self.rect = pygame.Rect(x + (FigureSettings.width - FigureSettings.rect_width) // 2,
                                y + FigureSettings.height - FigureSettings.rect_height,
                                FigureSettings.rect_width, FigureSettings.rect_height)

    def topleft(self):
        return (self.rect.x - (FigureSettings.width - FigureSettings.rect_width) // 2,
                self.rect.y - (FigureSettings.height - FigureSettings.rect_height))