import random
from typing import *
from Settings import *
import pygame
from Player import *
from Functions import *


class ShoppingMall:
    def __init__(self, window,
                 fontSize: int = DialogSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255),
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.bg = pygame.Surface((ShopSettings.boxWidth,
                                  ShopSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)

        self.npcImage=None
        self.player=None
        self.resource=None
        self.items=None
        self.selectedID=0
        self.operateCD=0
        self.goodList=[]
        self.costList=[]
        self.isOpen=True
    
    def GetMerchant(self,merchant):
        self.npcImage=merchant.image

    def GetData(self,player,resource):
        self.player=player
        self.resource=resource

    def GetGoods(self,goodList,costList):
        self.costList=costList
        self.goodList=goodList
        self.goodName=[ShopSettings.goodDict[itemName] for itemName in goodList]
        self.items=[self.goodName[i]+' '+CostTextMake(self.costList[i]) for i in range(len(self.goodName))]
    
    def ChangeChoice(self,keys):
        if (self.operateCD==0):
            if (keys[pygame.K_w]):
                self.selectedID=(self.selectedID-1+len(self.goodList))%len(self.goodList)
                self.operateCD=1
            if (keys[pygame.K_s]):
                self.selectedID=(self.selectedID+1+len(self.goodList))%len(self.goodList)
                self.operateCD=1
     
    def BuyItem(self,keys):
        if (self.operateCD==0 and keys[pygame.K_b]):
            playerMoney=self.resource.playerMoney
            cost=self.costList[self.selectedID]
            if (cost>=0):
                if (playerMoney>=cost):
                    pygame.event.post(pygame.event.Event(Events.shopAction
                                                         ,{0:cost,1:self.goodName[self.selectedID]}))
                    self.operateCD=1
            else:
                if (playerMoney>=-cost):
                    pygame.event.post(pygame.event.Event(Events.shopAction
                                                         ,{0:playerMoney,1:self.goodName[self.selectedID]}))
                    self.operateCD=1

    def render(self):
        self.window.blit(self.bg,
                         (ShopSettings.boxStartX, ShopSettings.boxStartY))

        offset = 0
        curID=0
        for text in self.items:
            if curID == self.selectedID:
                text = '-->' + text
            else:
                text = '   ' + text
            self.window.blit(self.font.render(text, True, self.fontColor),
                             (ShopSettings.textStartX, ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
            curID+=1

        texts = ["Coins: " + str(self.resource.playerMoney),
                 "HpPortion: " + str(self.resource.playerPortionCount[0]),
                 "MpPortion: " + str(self.resource.playerPortionCount[1]),
                 "Level: " + str(self.player.weaponLevel),
                 "Has Sniper: " + str(2 in self.player.weapons)]

        offset = 0
        for text in texts:
            self.window.blit(self.font.render(text, True, self.fontColor),
                             (
                                 ShopSettings.textStartX + ShopSettings.boxWidth * 3 / 4,
                                 ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
    
    def CDUpdate(self):
        if (self.operateCD!=0):
            self.operateCD=(self.operateCD+1)%(ShopSettings.operateCD+1)