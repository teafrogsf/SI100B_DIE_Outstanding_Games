# -*- coding:utf-8 -*-

import pygame

from Settings import *
import random 
from random import randint
from NPCs import *


class Block(pygame.sprite.Sprite):

    def __init__(self,n, x, y):
        super().__init__()
        self.n=n
        self.image = pygame.transform.scale(pygame.image.load(GamePath.tree) , (SceneSettings.tileWidth, SceneSettings.tileHeight))
        self.rect=self.image.get_rect()
        self.originrect_x=x
        self.originrect_y=y
        self.rect.x=x
        self.rect.y=y
        
    def draw(self, window, dx=0, dy=0):
        self.rect.x=self.originrect_x-dx
        self.rect.y=self.originrect_y-dy
        window.blit(self.image, (self.rect))
        self.lastdx=dx
        self.lastdy=dy

class Decorate(pygame.sprite.Sprite):
    def __init__(self,n, x, y):
        super().__init__()
        self.n=n
        self.frame=random.randint(0,6)
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (SceneSettings.tileWidth, SceneSettings.tileHeight*2)) for img in GamePath.fire]
        self.image=self.images[0]
        self.rect = self.image.get_rect()
        self.originrect_x=x
        self.originrect_y=y-40
        self.rect.x=x
        self.rect.y=y-40

    def update(self):

        if self.frame<18:
            self.image=self.images[(self.frame//3)]
            self.frame+=1
        else:
            self.frame=0

    def draw(self, window, dx=0, dy=0):
        self.rect.x=self.originrect_x-dx
        self.rect.y=self.originrect_y-dy
        window.blit(self.image, self.rect)

class CanBreak(pygame.sprite.Sprite):

    def __init__(self,n, x, y):
        super().__init__()
        self.n=n
        self.image =pygame.transform.scale(pygame.image.load(GamePath.vase), 
                            (SceneSettings.tileWidth, SceneSettings.tileHeight))

        self.rect = self.image.get_rect()
        self.originrect_x=x
        self.originrect_y=y
        self.rect.x=x
        self.rect.y=y

    def draw(self, window, dx=0, dy=0):
        self.rect.x=self.originrect_x-dx
        self.rect.y=self.originrect_y-dy
        window.blit(self.image, (self.rect))

class Portal(pygame.sprite.Sprite):
    def __init__(self,n,x,y):
        super().__init__()
        self.n=n
        self.frame=0
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (SceneSettings.tileWidth*2, SceneSettings.tileHeight*3)) for img in GamePath.portal]
        self.image=self.images[0]
        self.rect = self.image.get_rect()
        self.originrect_x=x
        self.originrect_y=y-60
        self.rect.x=x
        self.rect.y=y-60
        

    def update(self):
        if self.frame<21:
            self.image=self.images[self.frame//3]
            self.frame+=1
        else:
            self.frame=0


    def draw(self, window, dx=0, dy=0):
        self.rect.x=self.originrect_x-dx
        self.rect.y=self.originrect_y-dy
        window.blit(self.image, (self.rect))      

class Hint(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(GamePath.hint) , (SceneSettings.tileWidth, SceneSettings.tileHeight))
        self.x=x
        self.y=y
        

def gen_wild_map():
    images = [pygame.image.load(tile) for tile in GamePath.groundTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)
    
    return mapObj

def gen_home_map():
    images = [pygame.image.load(tile) for tile in GamePath.cityTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)
    
    return mapObj


def gen_home_obstacle():
    homematrix=HomeSettings.matrix

    decorates=pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    breakobj=pygame.sprite.Group()
    portals=pygame.sprite.Group()
    wildanimals=pygame.sprite.Group()
    hint=pygame.sprite.Group()
    for i in range(108):  
        for j in range(54): 
            if homematrix[j][i]==1:
                obstacles.add(Block(homematrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            if homematrix[j][i]==2:
                decorates.add(Decorate(homematrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            if homematrix[j][i]==3:
                breakobj.add(CanBreak(homematrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            if homematrix[j][i]==4:
                portals.add(Portal(homematrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            if homematrix[j][i]==8:
                b=random.randint(0,8)
                wildanimals.add(Animal(b,i*SceneSettings.tileWidth,j*SceneSettings.tileHeight))
            if homematrix[j][i]==6: 
                hint.add(Hint(i*SceneSettings.tileWidth,j*SceneSettings.tileHeight))
    return obstacles,decorates,breakobj,portals,wildanimals,hint

def gen_wild_obstacle():
    decorates=pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    breakobj=pygame.sprite.Group()
    portal=pygame.sprite.Group()
    wildmatrix=WildSettings.matrix

    for i in range(108):  #SceneSettings.tileXnum
        for j in range(54): #SceneSettings.tileYnum
            if wildmatrix[j][i]==1:
                obstacles.add(Block(wildmatrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            if wildmatrix[j][i]==2:
                decorates.add(Decorate(wildmatrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            if wildmatrix[j][i]==3:
                breakobj.add(CanBreak(wildmatrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            if wildmatrix[j][i]==4:
                portal.add(Portal(wildmatrix[j][i], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles,decorates,breakobj,portal 

