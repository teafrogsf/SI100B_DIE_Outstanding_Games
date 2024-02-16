# -*- coding:utf-8 -*-

from Settings import *
import pygame
import os
import typing
import Scene
from math import ceil
from Monsters import Monster
from Functions import *

# 设置角色动画
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, spawnX, spawnY):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img),(PlayerSettings.playerWidth, PlayerSettings.playerHeight)) 
                       for img in PlayerImagePaths.PLAYER]
        self.index = 0
        self.movementDelay = 0
        self.isFaceLeft=False
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.renderRect = self.image.get_rect()
        self._globalX = spawnX * SceneSettings.tileWidth
        self._globalY = spawnY * SceneSettings.tileHeight
        self.rect.topleft = (self._globalX, self._globalY)
        self.renderRect.topleft = (x, y)
        self.speed = PlayerSettings.playerSpeed
        self.talking = False
        self.hp=PlayerSettings.playerHP
        self.mp=PlayerSettings.playerMP

        #self.money = PlayerSettings.playerPocketMoney

        # weapons on ui
        self.weapon_index = 4
        self.weaponListIndex=0
        self.weapons = [4]
        self.can_switch_weapon = True
        self.weapon_switch_time = 0

        self.attackCD=0
        self.weaponLevel=0

    def GetGlobalCoor(self) -> (int, int):
        return (self._globalX, self._globalY)
    
    def SetGlobalCoor(self, globalX, globalY):
        self._globalX=globalX
        self._globalY=globalY
        self.rect.topleft=(self._globalX, self._globalY)

    def MoveUpdate(self, keys):
        if self.talking:
            self.index = 0
            self.image = self.images[self.index]
        else:
            # Update Player Position
            self.dx = 0
            self.dy = 0
            speed = ceil(self.speed * SceneSettings.tileHeight)
            self.isMoving=False
            if (keys[pygame.K_w]):
                self.dy -= speed
                self.isMoving=True
            if (keys[pygame.K_s]):
                self.dy += speed
                self.isMoving=True
            if (keys[pygame.K_a]):
                self.dx -= speed
                self.isMoving=True
                self.isFaceLeft=True
            if (keys[pygame.K_d]):
                self.dx += speed
                self.isMoving=True
                self.isFaceLeft=False
            self.rect=self.rect.move(self.dx, self.dy)
            self._globalX += self.dx
            self._globalY += self.dy
    
    def Move(self):
        if (self.isMoving):
            self.movementDelay+=1
            if (self.movementDelay>=len(self.images)):
                self.index = (self.index + 1) % len(self.images)
                self.movementDelay=0
        else:
            self.rect=self.rect.move(-self.dx, -self.dy)
            self._globalX -= self.dx
            self._globalY -= self.dy
            self.index=3
            self.movementDelay=0
        self.image=pygame.transform.flip(self.images[self.index],self.isFaceLeft,False)
    
    def GetRoomID(self,levelID,roomArea):
        for i in range(MapSettings.MAX_MAP_LENGTH[levelID]):
            for j in range(MapSettings.MAX_MAP_LENGTH[levelID]):
                room=roomArea[levelID][Hash(i,j,MapSettings.MAX_MAP_LENGTH[levelID])]
                if (room[0][0]==-1):
                    continue
                if (self._globalX>=room[0][0] and self._globalY>=room[0][1]):
                    if (self._globalX+PlayerSettings.playerWidth<=room[1][0] and self._globalY+PlayerSettings.playerHeight<=room[1][1]):
                        return Hash(i,j,MapSettings.MAX_MAP_LENGTH[levelID])
        return -1
    
    def Shoot(self):
        isMousePressed=pygame.mouse.get_pressed()
        if (isMousePressed[0] and self.attackCD==0 and self.mp>=0):
            mousePosition=pygame.mouse.get_pos()
            self.mp-=9-2*self.weapon_index
            pygame.event.post(pygame.event.Event(Events.playerShoot,{0:mousePosition}))
    
    def CDcounter(self):
        self.attackCD=(self.attackCD+1)%WeaponsSettings.attackSpeed[self.weapon_index]
        self.mp=min(int((self.mp+0.02)*100)/100.0,PlayerSettings.playerMP)
        if (self.weapon_switch_time!=0):
            self.weapon_switch_time=(self.weapon_switch_time+1)%50

    def render(self, window):
        window.blit(self.image, self.renderRect)