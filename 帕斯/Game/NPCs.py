# -*- coding:utf-8 -*-

import pygame
from pygame.sprite import Group
import random
from Settings import *
from Attributes import *

class NPC(pygame.sprite.Sprite,Collidable):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.image=pygame.transform.scale(pygame.image.load(GamePath.npc), 
                            (PlayerSettings.playerWidth+10, PlayerSettings.playerHeight+10))
        self.rect=self.image.get_rect()
        self.rect.width=NPCSettings.npcWidth
        self.rect.height=NPCSettings.npcHeight
        self.rect.topleft=(x,y)
        self.originrect_x=x
        self.originrect_y=y
        self.talking=False
        self.name=None
        self.font0=pygame.font.SysFont("impact",NPCSettings.font0size)
        self.text = None
        self.textrect=None
        
    def draw(self, window, dx=0, dy=0):
        self.text = self.font0.render(f"{self.name}",True,NPCSettings.font0color)
        self.textrect=self.text.get_rect()
        self.rect.x=self.originrect_x-dx
        self.rect.y=self.originrect_y-dy
        self.textrect.centerx=self.rect.centerx+10
        self.textrect.centery=self.rect.centery-35

        window.blit(self.image,(self.rect.x-15,self.rect.y-15,self.rect.width,self.rect.height))
        window.blit(self.text,self.textrect)

class DialogNPC(NPC):
    def __init__(self,x,y,dialog):
        super().__init__(x,y)
        self.dialog=dialog
        self.name="Dialog"

class AnimalGamenpc(NPC):
    def __init__(self,x,y,dialog):
        super().__init__(x,y)
        self.dialog=dialog
        self.name="Animal Game"
class ShopNPC(NPC):
    def __init__(self,x,y):
        super().__init__(x, y)
        self.name="ShopNpc"

    def gen_shop(self):
        pass

    
    def update(self, ticks):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
class Animal(pygame.sprite.Sprite):
    def __init__(self,index,x,y) -> None:
        super().__init__()
        self.index=int(index)
        self.touchplayer=0
        speed=AnimalSettings.speedlist
        self.originx=x
        self.originy=y

        self.speed=speed[self.index]
        self.step=50
        self.initialdirection=random.randint(0,3)
        self.directionx,self.directiony=AnimalSettings.originaldirection #[[-1,0],[1,0],[0,1],[0,-1]][self.initialdirection]
        self.flame=0
        self.moving=1
        self.imagelist=[[pygame.transform.scale(pygame.image.load(img), AnimalSettings.catposition) for img in GamePath.cat1],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.catposition) for img in GamePath.cat2],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.catposition) for img in GamePath.cat3],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.catposition) for img in GamePath.cat4],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.fishposition) for img in GamePath.fish],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.elfposition) for img in GamePath.elf],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.chickenposition) for img in GamePath.chicken1],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.chickenposition) for img in GamePath.chicken2],
                        [pygame.transform.scale(pygame.image.load(img), AnimalSettings.goldenbirdposition) for img in GamePath.goldenbird],

                        ]
        self.images=self.imagelist[self.index]            
        self.image=self.images[self.flame]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.rect.width=self.rect.width//2
        self.rect.height=self.rect.height//2
        self.lastdx=0
        self.lastdy=0

    def walk(self,player,animals,bra,obstacles):
        self.rect.x+=self.directionx*self.speed
        self.rect.y+=self.directiony*self.speed
        
#pygame.sprite.spritecollide(self, animals, False) player.is_colliding_animal
        if pygame.sprite.spritecollide(self,bra, False) or pygame.sprite.spritecollide(self, obstacles, False):
            self.rect.x-=1*self.directionx*self.speed
            self.rect.y-=1*self.directiony*self.speed

            if self.directionx!=0:
                self.directiony=-1*self.directionx
                self.directionx=0
            else:
                self.directionx=1*self.directiony
                self.directiony=0

        for animal in animals:
            if self != animal and self.rect.colliderect(animal.rect):
                self.rect.x-=1*self.directionx*self.speed
                self.rect.y-=1*self.directiony*self.speed
                b=[-1,1][random.randint(0,1)]
                if self.directionx!=0:
                    self.directiony=b*self.directionx
                    self.directionx=0
                else:
                    self.directionx=-1*b*self.directiony
                    self.directiony=0

                #self.directionx=self.directionx*-1
                #self.directiony=self.directiony*-1#random.choice([-1,1])


        if pygame.sprite.spritecollide(self,player,False):
            self.touchplayer=1
            self.rect.x-=self.directionx*self.speed
            self.rect.y-=self.directiony*self.speed
            self.moving=0
        else:
            if self.moving==0:
                self.directionx=self.directionx*-1
                self.directiony=self.directiony*-1
            self.moving=1
            
        if self.step<40:
            self.step+=1
        else:
            b=[-1,1][random.randint(0,1)]
            if self.directionx!=0:
                self.directiony=b*self.directionx
                self.directionx=0
            else:
                self.directionx=-1*b*self.directiony
                self.directiony=0
            self.step=0
    def draw(self, window, dx=0, dy=0):
        if self.flame<12:
            self.flame+=1
        else:
            self.flame=0
        if self.moving==1:
            if self.directiony==-1:
                self.image=self.images[4*(self.flame//4)+3]
            elif self.directiony==1:
                self.image=self.images[4*(self.flame//4)]
            elif self.directionx==-1:
                self.image=self.images[4*(self.flame//4)+1]
            elif self.directionx==1:
                self.image=self.images[4*(self.flame//4)+2]
        else:
            if self.directiony==-1:
                self.image=self.images[3]
            elif self.directiony==1:
                self.image=self.images[0]
            elif self.directionx==-1:
                self.image=self.images[1]
            elif self.directionx==1:
                self.image=self.images[2]

        self.rect.x-=dx-self.lastdx
        self.rect.y-=dy-self.lastdy
        self.lastdx=dx
        self.lastdy=dy
        window.blit(self.image,(self.rect.x-20,self.rect.y-20,self.rect.width,self.rect.height))
    print()
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y,type, order,HP, Atk, Money):
        super().__init__()
        self.index=0
        self.type=type
        if self.type<3:
            self.images = [pygame.transform.scale(pygame.image.load(img), 
                                    (BattleSettings.monsterWidth//3, BattleSettings.monsterHeight//3)) for img in GamePath.monster2]
        else:
           self.images = [pygame.transform.scale(pygame.image.load(img), 
                                    (BattleSettings.monsterWidth//3, BattleSettings.monsterHeight//3)) for img in GamePath.monster]
        self.image=self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.font= pygame.font.Font(None,NPCSettings.fontsize)
        self.originrect_x=x
        self.originrect_y=y
        self.HP = HP
        self.ATK = Atk
        self.money= Money
        self.order=order
        font0=pygame.font.SysFont("impact",NPCSettings.font0size)
        textlist=["    WARM UP",f"    WEEK QUIZ{self.order}",f" MONTH EXAM{self.order}",f"MIDTERM EXAM{self.order}"," FINAL EXAM"]
        self.name=font0.render(textlist[self.type],True,MonsterSettings.font0color)
        self.textrect=self.name.get_rect()
    def draw(self, window, dx=0, dy=0):
        if self.index==39:
            self.index=0
        else:
            self.index+=1
        self.image=self.images[4*(self.index//10)]
        self.rect.x=self.originrect_x-dx
        self.rect.y=self.originrect_y-dy
        window.blit(self.image,self.rect)
        self.textrect.centerx=self.rect.centerx-5
        self.textrect.centery=self.rect.centery-35
        window.blit(self.name,self.textrect),



