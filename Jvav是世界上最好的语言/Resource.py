import pygame
from Settings import *

class ResourceSystem:
    def __init__(self):
        self.playerMoney=PlayerSettings.playerPocketMoney
        self.playerPortionCount=[0,0] # HP portion, MP portion
        self.useCD=0
    
    def ChangeMoney(self,delta):
        self.playerMoney+=delta
    
    def UsePortion(self,keys):
        # HP Portion
        whetherUse=[False,False]
        if (keys[pygame.K_LSHIFT]):
            if (self.playerPortionCount[0]>=1 and self.useCD==0):
                self.playerPortionCount[0]-=1
                whetherUse[0]=True
                self.useCD=1
        # MP portion
        if (keys[pygame.K_LCTRL]):
            if (self.playerPortionCount[1]>=1 and self.useCD==0):
                self.playerPortionCount[1]-=1
                whetherUse[1]=True
                self.useCD=1
        return whetherUse
    
    def CDUpdate(self):
        if (self.useCD!=0):
            self.useCD=(self.useCD+1)%(PortionSettings.useCD+1)