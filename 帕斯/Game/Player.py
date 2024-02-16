# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
import random
from NPCs import Animal
import os

class Player(pygame.sprite.Sprite, Collidable):
    
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (PlayerSettings.playerWidth+10, PlayerSettings.playerHeight+10)) for img in GamePath.player]
        self.index = 0
        self.hadbattle=1
        self.image = self.images[self.index]
        self.battle=False
        self.dialog=False
        self.shopping=False
        self.rect = self.image.get_rect()
        self.rect.width=PlayerSettings.rectwidth
        self.rect.height=PlayerSettings.rectheight
        self.rect.topleft = (x,y)
        self.next_rect=self.rect
        self.speed = PlayerSettings.playerSpeed
        self.talking = False
        self.dx=0
        self.dy=0
        self.egg=0
        self.readytoplay=0
        self.money,self.ATK,self.OriginHP,self.price1,self.price2,self.price3,self.animal=self.importdata()
        self.HP=self.OriginHP
        self.font0=pygame.font.SysFont("impact",PlayerSettings.font0size)
        self.text = None
        self.textrect=None
        self.homeportaldata=PlayerSettings.homeportal
        self.wildportaldata=PlayerSettings.wildportal
        self.scenecameray=0
        self.scenecamerax=0


    def reset_pos(self):
        if self.collidingWith["monster"]==True:
            postionlist=PlayerSettings.reset_position_list
            self.rect.x=self.collidingObject["monster"].rect.x+postionlist[self.collidingObject["monster"].order-1][0]
            self.rect.y=self.collidingObject["monster"].rect.y+postionlist[self.collidingObject["monster"].order-1][1]
        if self.collidingWith["dialog_npc"]==True:
            self.rect.x=self.collidingObject["dialog_npc"].rect.x-60
            self.rect.y=self.collidingObject["dialog_npc"].rect.y

        if self.collidingWith["animalgame_npc"]==True or self.readytoplay==2:
            if self.readytoplay==1:#play
                self.rect.x=self.collidingObject["animalgame_npc"].rect.x
                self.rect.y=self.collidingObject["animalgame_npc"].rect.y+150
            if self.readytoplay==0 :#quit
                self.rect.x=self.collidingObject["animalgame_npc"].rect.x
                self.rect.y=self.collidingObject["animalgame_npc"].rect.y-70
            if self.readytoplay==2:#reset
                self.rect.topleft=(200,370)
                

        return self.rect
    def scenereset(self,scene,type):
        if type==2:

            scene.cameraX,scene.cameraY,self.rect.x,self.rect.y=self.wildportaldata
        if type==1:
            self.wildportaldata=(scene.cameraX,scene.cameraY,self.rect.x-100,self.rect.y)

            scene.cameraX,scene.cameraY,self.rect.x,self.rect.y=self.homeportaldata


        #self.rect.x=3100
        #self.rect.y=1300
    def try_move(self):
        keys=pygame.key.get_pressed()

            # Update Player Position
        dx=0
        dy=0
        if keys[pygame.K_w] and self.rect.top > 0 :
            dy -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < WindowSettings.height:
            dy += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            dx -= self.speed
        if keys[pygame.K_d] and self.rect.right < WindowSettings.width:
            dx += self.speed
            
        self.rect.x+=dx
        self.rect.y+=dy
        self.dx=dx
        self.dy=dy


        return self.rect ,self.dy,self.dx

    def update(self, width,height):
        if self.index==119:
            self.index=0
        else:
            self.index+=1
        self.image=self.images[self.index]

    def draw(self, window, dx=0, dy=0):
        self.text = self.font0.render(f"COIN:{self.money}",True,(220,220,220))
        self.textrect=self.text.get_rect()
        self.textrect.centerx=self.rect.centerx
        self.textrect.centery=self.rect.centery-35

        self.update(PlayerSettings.playerWidth,PlayerSettings.playerHeight)
        self.rect.x-=dx
        self.rect.y-=dy
        window.blit(self.image, (self.rect.x-25,self.rect.y-28,self.rect.width,self.rect.height))
        window.blit(self.text,self.textrect)

    def fix_to_middle(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy

    def eggborn(self):
        if self.hadbattle and self.egg!=0:
            for i in range(self.egg):
                a=len(self.animal)
                b=random.randint(0,100)
                if b<95:
                    typ=b%8
                else:
                    typ=8
                self.animal.add(Animal(typ,600+(a%30)*60,100+60*(a//30)))
        self.egg=0
        return self.animal

    def initialcoin(self):

        initialcoin=0
        for animal in self.animal:
            if animal.index<=4:
                initialcoin+=20
            elif animal.index<7 and animal.index>4:
                initialcoin+=10
            else:
                initialcoin+=100
        return initialcoin

    def importdata(self):
        money=0
        atk=0
        hp=0
        price1=0
        price2=0
        price3=0
        animal=pygame.sprite.Group()
        with open(f"./Data.txt","r",encoding="utf-8") as data:
            for line in data:
                if "money" in line:
                    money=int(line[6:])
                elif "atk" in line:
                    atk=int(line[4:])
                elif "hp" in line:
                    hp=int(line[3:])
                elif "price1" in line:
                    price1=int(line[7:])
                elif "price2" in line:
                    price2=int(line[7:])
                elif "price3" in line:
                    price3=int(line[7:])
                elif "animal" in line:
                    animals=line[9:]
                    animallist=animals.split("--")
                    for animali in animallist:
                        if animali!="":
                            animaldata=animali.split(",")
                            animal.add(Animal(int(animaldata[0]),int(animaldata[1]),int(animaldata[2])))
        data.close()
        return money,atk,hp,price1,price2,price3,animal
    
    def exportdata(self):
        self.hadbattle=1
        self.eggborn()
        modifylines=[]
        modifylines.append(str(f"money={self.money}\n"))
        modifylines.append(str(f"atk={self.ATK}\n"))
        modifylines.append(str(f"hp={self.OriginHP}\n"))
        modifylines.append(str(f"price1={self.price1}\n"))
        modifylines.append(str(f"price2={self.price2}\n"))
        modifylines.append(str(f"price3={self.price3}\n"))
        animallist=["animal="]
        for animal in self.animal:
            animallist.append(f"{animal.index},{animal.originx},{animal.originy}")
        animallist="--".join(animallist)
        modifylines.append(animallist)
        with open(f"./Data.txt","w") as newdata:
            newdata.writelines(modifylines)
    def initialdata(self):
        modifylines=["money=400\n","atk=3\n","hp=100\n","price1=50\n","price2=50\n","price3=30\n"]
        with open(f"./Data.txt","w") as newdata:
            newdata.writelines(modifylines)
        self.money,self.ATK,self.OriginHP,self.price1,self.price2,self.price3,self.animal=self.importdata()
        self.HP=self.OriginHP
        self.egg=0
