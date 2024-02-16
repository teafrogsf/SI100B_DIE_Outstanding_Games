import pygame
import copy
from Settings import *

class CollisionSystem:
    def __init__(self):
        self.obstacles=None
        self.monsters=None
        self.player=None
        pass
    
    def GetSprites(self,obstacle,monster,player,bullets,portals,merchant,levelID):
        self.obstacles=obstacle
        self.monsters=monster
        self.player=player
        self.bullets=bullets
        self.portals=portals
        self.merchant=merchant
        self.levelID=levelID
    
    def work(self):
        # Obstacles and the Player
        collisionList=pygame.sprite.spritecollide(self.player,self.obstacles,False)
        if (collisionList!=[]):
            pygame.event.post(pygame.event.Event(Events.playerStop,{0:0}))
        
        # Obstacles and Monsters
        for monster in self.monsters.sprites():
            collisionList=pygame.sprite.spritecollide(monster,self.obstacles,False)
            if (collisionList!=[]):
                pygame.event.post(pygame.event.Event(Events.monsterStop,{0:monster.orderNum}))
        
        # Obstacles and Bullets
        for bullet in self.bullets.sprites():
            collisionList=pygame.sprite.spritecollide(bullet,self.obstacles,False)
            if (collisionList!=[]):
                pygame.event.post(pygame.event.Event(Events.bulletEliminate,{0:bullet.orderNum}))
                for obstacle in collisionList:
                    if (obstacle.isDestructible):
                        pygame.event.post(pygame.event.Event(Events.obstacleDestruction,{0:obstacle._order}))

        # Monsters and the player
        collisionList=pygame.sprite.spritecollide(self.player,self.monsters,False)
        for monster in collisionList:
            if (monster.attackType!=0):
                continue
            pygame.event.post(pygame.event.Event(Events.monsterAttack,{0:monster.orderNum,1:monster.damage}))
        
        # Bullets and monsters
        for bullet in self.bullets.sprites():
            isHit=False
            if (bullet.origin!=1):
                continue
            collisionList=pygame.sprite.spritecollide(bullet,self.monsters,False)
            if (collisionList!=[]):
                for monster in collisionList:
                    if (not monster.isAlive):
                        continue
                    isHit=True
                    pygame.event.post(pygame.event.Event(Events.monsterHit,{0:monster.orderNum,1:bullet.damage}))
            if (isHit):
                pygame.event.post(pygame.event.Event(Events.bulletEliminate,{0:bullet.orderNum}))
        
        # Bullets and the Player
        collisionList=pygame.sprite.spritecollide(self.player,self.bullets,False)
        if (collisionList!=[]):
            for bullet in collisionList:
                if (bullet.origin!=0):
                    continue
                pygame.event.post(pygame.event.Event(Events.playerHit,{0:bullet.damage}))
                pygame.event.post(pygame.event.Event(Events.bulletEliminate,{0:bullet.orderNum}))
        
        # Portals and the Player
        collisionList=pygame.sprite.spritecollide(self.player,self.portals,False)
        if (collisionList!=[]):
            pygame.event.post(pygame.event.Event(Events.levelChange,{0:0}))
        
        # NPC and the Player
        collisionList=pygame.sprite.spritecollide(self.player,self.merchant,False)
        if (collisionList!=[]):
            goodList=ShopSettings.goodList[collisionList[0].typeID][self.levelID]
            pygame.event.post(pygame.event.Event(Events.shopActivate
                                                 ,{0:[good[0] for good in goodList],1:[good[1] for good in goodList]
                                                   ,2:collisionList[0]}))