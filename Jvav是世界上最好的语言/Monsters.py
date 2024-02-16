from Settings import *
from random import random,randint
from Functions import *
from Weapons import Bullet
from math import sin,cos
import pygame
import typing


class Monster(pygame.sprite.Sprite):
    def __init__(self, globalX:int, globalY:int, typeID:int, orderNum:int):
        super().__init__()
        self.images=[pygame.transform.scale(pygame.image.load(img)
                    ,(MonsterSettings.monsterWidth,MonsterSettings.monsterHeight))
                     for img in MonsterImagePaths.MONSTER[typeID]]
        self.index=1
        self.image=self.images[self.index]
        self.movementDelay=0
        self.name=MonsterSettings.monsterName[typeID]
        self.damage=MonsterSettings.monsterDamage[typeID]
        self.health=MonsterSettings.monsterHealth[typeID]
        self.speed=MonsterSettings.monsterSpeed[typeID]
        self.globalX=globalX
        self.globalY=globalY
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.globalX, self.globalY)
        self.action=(1,(0,0))
        self.actionDelay=0
        self.type=typeID
        self.isMoving=False
        self.isFaceLeft=False
        self.orderNum=orderNum
        self.attackType=MonsterSettings.attackType[typeID]
        self.attackCD=0
        self.isAlive=True
        self.gold_drop=MonsterSettings.monster_Gold_drop[typeID]
        self.actionTime=MonsterSettings.actionTime
    
    def IsAlive(self)->bool:
        return self.isAlive
    
    def get_money(self):
        pocket_money=0
        if self.health <= 0:
            pocket_money += self.gold_drop
        return pocket_money

    def IsMonster(self)->bool:
        return True
    
    # return (actionType,(dx,dy))
    # actionType=0 => attack, meanwhile dx=0, dy=0
    # actionType=1 => Move (dx,dy)
    def UpdateAction(self)->typing.Tuple[int,typing.Tuple[int,int]]:
        if (not self.isAlive):
            return (1,(0,0))
        if (self.actionDelay>0 and self.actionDelay<=self.actionTime):
            self.actionDelay=(self.actionDelay+1)%(self.actionTime*2)
            return self.action
        if (self.actionDelay>self.actionTime and self.actionDelay<self.actionTime):
            self.action=(1,(0,0))
            self.actionDelay=(self.actionDelay+1)%(self.actionTime*2)
            # print("Wait")
            return self.action
        self.actionDelay=1
        if (self.action[0]==0):
            doAttack=int(random()*10000)<=MonsterSettings.monsterAttackDesire[self.type]
            if (doAttack):
                self.action=(0,(0,0))
            else:
                self.action=(1,(0,0))
            return self.action
        doAttack=int(random()*10000)<=MonsterSettings.monsterAttackDesire[self.type]
        if (doAttack):
            self.action=(0,(0,0))
            return self.action
        direction=MonsterSettings.monsterDirection[int(random()*99)%9]
        dx=direction[0]*self.speed
        dy=direction[1]*self.speed
        self.action=(1,(dx,dy))
        return self.action
    
    def DoAction(self):
        if (not self.isAlive):
            return None
        if (self.action[0]==0):
            return None
        else:
            dx=self.action[1][0]
            dy=self.action[1][1]
            self.rect=self.rect.move(dx,dy)
            self.globalX+=dx
            self.globalY+=dy
            self.isMoving=True
            self.isFaceLeft=dx<0
    
    def Move(self):
        if (not self.isAlive):
            return None
        if (self.isMoving and self.actionDelay<=self.actionTime):
            self.movementDelay+=1
            if (self.movementDelay>=len(self.images)):
                self.index=(self.index+1)%(len(self.images)-1)+1
                self.movementDelay=0
        else:
            self.rect=self.rect.move(-self.action[1][0],-self.action[1][1])
            self.globalX-=self.action[1][0]
            self.globalY-=self.action[1][1]
            self.index=1
            self.movementDelay=0
        self.image=pygame.transform.flip(self.images[self.index],self.isFaceLeft,False)
    
    def update(self, operType, orderList):
        if (not self.isAlive):
            return None
        if (operType==0): # Action Decision
            self.UpdateAction()
            #if (self.action[0]==0):
            #    print("!")
            self.DoAction()
        elif (operType==1): # Move Step 1
            if (self.orderNum in orderList):
                self.isMoving=False
        elif (operType==2): # Move Step 2
            self.Move()
        elif (operType==3): # attack
            if (self.orderNum in orderList and self.attackCD==0):
                pygame.event.post(pygame.event.Event(Events.monsterAttack,{0:self.orderNum,1:self.damage}))
            elif (self.attackCD==0 and self.attackType>0):
                if (self.attackType in [1,3]):
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:5,3:0,4:self.damage,5:0}))
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:-5,3:0,4:self.damage,5:0}))
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:0,3:5,4:self.damage,5:0}))
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:0,3:-5,4:self.damage,5:0}))
                if (self.attackType in [2,3]):
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:2,3:2,4:self.damage,5:0}))
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:2,3:-2,4:self.damage,5:0}))
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:-2,3:2,4:self.damage,5:0}))
                    pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX,1:self.globalY,2:-2,3:-2,4:self.damage,5:0}))
                if (self.attackType==4):
                    for _ in range((self.type+1)*7):
                        theta=randint(0,359)
                        dx=15*cos(theta)
                        dy=15*sin(theta)
                        pygame.event.post(pygame.event.Event(Events.monsterGenerateBullet,{0:self.globalX+BossSettings.bossWidth//2,1:self.globalY+BossSettings.bossHeight//2,2:dx,3:dy,4:self.damage,5:0}))
            else:
                pass
            self.attackCD=(self.attackCD+1)%(self.actionTime*2)
        elif (operType==4): # get hit
            orderNumList=[orderList[i][0] for i in range(len(orderList))]
            damageList=[orderList[i][1] for i in range(len(orderList))]
            if (self.orderNum in orderNumList):
                pos=0
                for i in range(len(orderNumList)):
                    if (orderNumList[i]==self.orderNum):
                        pos=i
                        break
                self.health-=damageList[pos]
        elif (operType==5): # whether dead
            if (self.health<=0):
                self.isAlive=False
                self.index=0
                self.image=self.images[self.index]
                pygame.event.post(pygame.event.Event(Events.monsterDeath,{0:randint(self.gold_drop[0],self.gold_drop[1])}))
        else:
            pass

class Boss(Monster):
    def __init__(self, globalX:int, globalY:int, typeID:int, orderNum:int):
        super().__init__(globalX,globalY,typeID,orderNum)
        self.name=BossSettings.bossName[typeID]
        self.damage=BossSettings.bossDamage[typeID]
        self.health=BossSettings.bossHealth[typeID]
        self.speed=BossSettings.bossSpeed[typeID]
        self.images=[pygame.transform.scale(pygame.image.load(img)
                    ,(BossSettings.bossWidth,BossSettings.bossHeight))
                     for img in MonsterImagePaths.BOSS[typeID]]
        self.index=1
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.globalX, self.globalY)
        self.gold_drop=BossSettings.boss_Gold_Drop[typeID]
        self.actionTime=BossSettings.actionTime
        self.attackType=BossSettings.attackType[typeID]