# -*- coding:utf-8 -*-

import pygame
import copy
from Settings import *
from Attributes import *

class NPC(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, name):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.name=name
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update(self):
        raise NotImplementedError

    def reset_talkCD(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####


class DialogNPC(NPC):
    def __init__(self, x, y, name):
        ##### Your Code Here ↓ #####
        super().__init__(x,y,name)
        if self.name==dialognpc.merchant:
            self.image=pygame.image.load(GamePath.npc[0])
            self.image=pygame.transform.scale(self.image,(NPCSettings.npcWidth-20,NPCSettings.npcHeight+10))
        elif self.name==dialognpc.village_chief:
            self.image=pygame.image.load(GamePath.npc[1])
            self.image=pygame.transform.scale(self.image,(NPCSettings.npcWidth-20,NPCSettings.npcHeight+0))
        elif self.name==dialognpc.ghost:
            self.image=pygame.image.load(GamePath.npc[2])
            self.image=pygame.transform.scale(self.image,(NPCSettings.npcWidth-20,NPCSettings.npcHeight+0))    
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.talking=False
        self.talkCD=0
        self.firsttalk=0
        self.talktimes=1
        self.talktwo=1
        self.choose=True
        ##### Your Code Here ↑ #####
    
    def update(self):
        ##### Your Code Here ↓ #####
        if not self.talking:
            if self.talkCD>0:
                self.talkCD-=1 
        if self.firsttalk>=len(DialogSettings.npcmeettextcontent[self.name.name]):
                self.firsttalk=0  
        if self.talktimes>len(DialogSettings.npctextcontent[self.name.name][self.talktwo]):
            self.talktimes=1 
        if self.talktwo>len(DialogSettings.npctextcontent[self.name.name]):
            self.talktwo=1
    def reset_talk_CD(self):
        self.talkCD=50
    def can_talk(self):
        return self.talkCD==0      
    def draw(self, window, dx=0, dy=0):
        window.blit(self.image, self.rect)
        ##### Your Code Here ↑ #####

class ShopNPC(NPC):
    def __init__(self, x, y, name, items, dialog):
        super().__init__(x, y, name)

        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
    def update(self, ticks):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    

class Monster(pygame.sprite.Sprite):
    def __init__(self, img, x=0,  y=0, HP = 10, Attack = 3):
        super().__init__()
        ##### Your Code Here ↓ #####
        self.image = img
        self.be_poisoned = None
        self.HP = HP
        self.attack = Attack
        self.rect = self.image.get_rect(topleft = (x,y))
        self.init_HP = copy.copy(self.HP)
        self.is_mimic =False
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        window.blit(self.image,(self.rect.x+dx,self.rect.y+dy))
        ##### Your Code Here ↑ #####

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
