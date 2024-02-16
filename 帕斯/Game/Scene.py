# -*- coding:utf-8 -*-

import pygame
import Maps

from enum import Enum
from Settings import *
from NPCs import *
from PopUpBox import *
from BgmPlayer import *
from Player import *

class Scene():
    def __init__(self, window):
        self.type = None
        self.monsters=pygame.sprite.Group()
        self.map = None
        self.decorates=pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.breakobj=pygame.sprite.Group()
        self.dialog_npcs = pygame.sprite.Group()
        self.shop_npcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.animals=pygame.sprite.Group()
        self.wildanimals=pygame.sprite.Group()
        self.animalgame_npc=pygame.sprite.Group()
        self.hint=pygame.sprite.Group()
        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height
        self.battlebox=None
        self.dialogbox=None
        self.shoppingbox=None
        self.animalgamebox=None
        self.animalgaming=0
        self.cameraX =0
        self.cameraY=0      
        self.gamelevel=0
        self.win=0

    def trigger_dialog(self, npc):
        self.dialogbox=DialogBox(self.window,npc)
        #print("init dialog done,dialog event done")

    def end_dialog(self,player):
        self.dialogbox=None
        player.reset_pos()
        player.collidingWith['dialog_npc']=False
        player.collidingObject['dialog_npc']=[]

    def trigger_animaldialog(self,npc):
        self.animalgamebox=AniamlgameBox(self.window,npc)
        
    def end_animaldialog(self,player):
        self.gamelevel=self.animalgamebox.hardlevel
        self.animalgamebox=None
        player.reset_pos()
        player.collidingWith['animalgame_npc']=False
        player.collidingObject['animalgame_npc']=[]
        
    def trigger_animalgame(self,level):
        
        for animals in self.wildanimals:
            animals.speed=animals.speed*[1,2,3.2][level-1]
        self.animalgaming=1


    def end_animalgame(self,player):
        
        
        self.cameraX=0
        self.cameraY=60
        self.animalgaming=0
        if self.win==1:
            player.money+=[10,50,1000][self.gamelevel-1]
        player.reset_pos()
        for animals in self.wildanimals:
            animals.speed=1
            animals.touchplayer=0

    def trigger_battle(self, player):
        self.battlebox=BattleBox(self.window,player,player.collidingObject["monster"])
        #pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))
        #print("init battle done,battle event done")

    def end_battle(self,player):
        self.battlebox=None
        player.reset_pos()
        player.collidingWith['monster']=False
        player.collidingObject['mosnter']=[]
        
    def trigger_shop(self,player):
        self.shoppingbox=ShoppingBox(self.window,player)

    def end_shop(self,player):
        player.reset_pos()
        self.shoppingbox=None
        player.collidingWith['shop_npc']=False
        player.collidingObject['shop_npc']=[]
    def get_width(self):
        return WindowSettings.width * WindowSettings.outdoorScale

    def get_height(self):
        return WindowSettings.height * WindowSettings.outdoorScale
    
    def update_camera(self, player):

            if player.rect.x > WindowSettings.width //2+ 50:
                self.cameraX += player.speed

                if self.cameraX < self.get_width() - WindowSettings.width:
                    player.fix_to_middle(player.speed, 0)
                else:
                    self.cameraX = self.get_width() - WindowSettings.width
                    
            elif player.rect.x < WindowSettings.width//2-50:
                self.cameraX -= player.speed
                if self.cameraX > 0:
                    player.fix_to_middle(-player.speed, 0)
                else:
                    self.cameraX = 0
            if player.rect.y > WindowSettings.height //2+50:
                self.cameraY += player.speed
                if self.cameraY < self.get_height() - WindowSettings.height:
                    player.fix_to_middle(0, player.speed)
                else:
                    self.cameraY = self.get_height() - WindowSettings.height
            elif player.rect.y < WindowSettings.height //2-50:
                self.cameraY -= player.speed
                if self.cameraY > 0:
                    player.fix_to_middle(0, -player.speed)
                else:
                    self.cameraY = 0

    def render(self, player:Player):
        self.update_camera(player)
        keys=pygame.key.get_pressed()
        if self.type==SceneType.WILD:
            self.render_wild(player,keys)
                
        if self.type==SceneType.HOME:
            self.render_home(player,keys)
class StartMenu:
    def __init__(self, window):
        self.index=0
        self.type=SceneType.MENU
        self.images=[ pygame.transform.scale(pygame.image.load(img) ,
                     (WindowSettings.width,550)) for img in GamePath.menu]
        self.startimg=pygame.transform.scale(pygame.image.load(GamePath.dialog) ,(300,50)) 
        self.image=self.images[self.index]
        self.window=window
        self.startrect=self.startimg.get_rect()
        self.wordcenter=(WindowSettings.width // 2-8 , (WindowSettings.height ) // 2+100)
        #self.start_rect.center=self.wordcenter

        self.textsize=40
        self.textsize2=30
        self.position3=(350,620)
        self.choosing=0

        font0=pygame.font.SysFont("impact", self.textsize)
        self.text = font0.render("START",True,(20,0,0))
        self.textrect=self.text.get_rect()
        #self.text_rect.center=self.wordcenter

        font1=pygame.font.SysFont("inkfree", self.textsize2)
        self.text2=font1.render("If you don't risk anything, you risk even more",True,(150,150,150))
    def selectanimate(self,size=1):
        self.startimg=pygame.transform.scale(pygame.image.load(GamePath.dialog) ,(300*size,50*size)) 
        self.startrect=self.startimg.get_rect()
        font0=pygame.font.SysFont("impact", int(self.textsize*size))
        self.text = font0.render("START",True,(20,0,0))
        self.textrect=self.text.get_rect()
        self.startrect.center=self.wordcenter
        self.textrect.center=self.wordcenter
    def update_menu(self,window):
        if self.index<94*4:
            self.index+=1
        else:
            self.index=0
        self.image=self.images[self.index//4]
        mousepos=pygame.mouse.get_pos()
        if mousepos[0] >= self.startrect.x and mousepos[0]<self.startrect.x+self.startrect.width and mousepos[1] >self.startrect.y  and mousepos[1]<self.startrect.y+self.startrect.height  :
            self.selectanimate(1.25)

            if pygame.mouse.get_pressed()[0]:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH))               
        else:
            self.selectanimate(1)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH)) 
        window.blit(self.image,(0,75))
        window.blit(self.startimg,self.startrect)
        window.blit(self.text,self.textrect)
        window.blit(self.text2,(self.position3))
class HomeScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.type=SceneType.HOME
        self.obstacles,self.decorates,self.breakobj,self.portals,self.wildanimals,self.hint=Maps.gen_home_obstacle()
        self.map=Maps.gen_home_map()
        self.shop_npcs.add(ShopNPC(300,220))
        self.dialog_npcs.add(DialogNPC(300,140,None))
        self.animalgame_npc.add(AnimalGamenpc(200,500,None))

    def render_home(self,player,keys):
        if self.dialogbox!=None or self.animalgamebox!=None or self.shoppingbox!=None:
            if self.dialogbox!=None:
                self.dialogbox.update_dialog()
            elif self.animalgamebox!=None:
                self.animalgamebox.update_animalgame()
            elif self.shoppingbox!=None:
                self.shoppingbox.update_dialog()
        else:
            for i in range(SceneSettings.tileXnum):
                for j in range(SceneSettings.tileYnum):
                    self.window.blit(self.map[i][j], 
                                    (SceneSettings.tileWidth * i- self.cameraX, SceneSettings.tileHeight * j- self.cameraY))
            for hintblock in self.hint.sprites():
                self.window.blit(hintblock.image,(hintblock.x- self.cameraX, hintblock.y- self.cameraY))
            for obs in self.obstacles.sprites():
                obs.draw(self.window,self.cameraX,self.cameraY)
            for dec in self.decorates.sprites():             
                dec.draw(self.window,self.cameraX,self.cameraY)
            for bra in self.breakobj.sprites(): 
                bra.draw(self.window,self.cameraX,self.cameraY)
            for portal in self.portals.sprites():
                portal.draw(self.window,self.cameraX,self.cameraY)
            for npc in self.shop_npcs.sprites():
                npc.draw(self.window,self.cameraX,self.cameraY)
            for npc in self.dialog_npcs.sprites():
                npc.draw(self.window,self.cameraX,self.cameraY)
            for npc in self.animalgame_npc.sprites():
                #print(len(self.animalgame_npc.sprites()))
                npc.draw(self.window,self.cameraX,self.cameraY)
            for ani in self.animals.sprites(): 
                ani.draw(self.window,self.cameraX,self.cameraY)
            for ani in self.wildanimals.sprites(): 
                ani.draw(self.window,self.cameraX,self.cameraY)

            if self.animalgaming==1 :
                for animals in self.wildanimals:
                    if animals.touchplayer==1:
                        player.cameraX=self.cameraX
                        player.cameraY=self.cameraY
                        player.readytoplay=2
                        self.win=0
                        self.end_animalgame(player)

                if player.collidingWith["decorate"]:
                    player.cameraX=self.cameraX
                    player.cameraY=self.cameraY
                    player.readytoplay=2
                    self.win=1
                    self.end_animalgame(player)

                
            if player.is_colliding():
                player.draw(self.window,player.dx,player.dy)
            else:
                player.draw(self.window,0,0)
            if player.collidingWith["bra"] and keys[pygame.K_SPACE]:
                for bra in player.collidingObject["bra"]:
                    self.breakobj.remove(bra)
            if player.collidingWith["portal"]:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH))

class WildScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.type=SceneType.WILD
        self.obstacles,self.decorates,self.breakobj,self.portals=Maps.gen_wild_obstacle()
        self.map=Maps.gen_wild_map()
        self.monsters=self.gen_monsters()#x y order hp atk money

    def gen_monsters(self):
        monsters=pygame.sprite.Group()
        monsters.add(Monster(560,200,0,1,50,1,1))
        monsters.add(Monster(1280,280,1,2,100,1,1))
        monsters.add(Monster(120,1040,1,3,100,2,1))
        monsters.add(Monster(1000,1040,1,4,100,3,1))
        monsters.add(Monster(440,1400,2,5,300,3,1))
        monsters.add(Monster(2080,880,3,6,300,3,5))
        monsters.add(Monster(3000,1200,4,7,750,6,5))
        return monsters

    def render_wild(self,player,keys):
        if self.battlebox!=None:
            self.battlebox.Update_card()
                        #print("render in scene")
        else:
            for i in range(SceneSettings.tileXnum):
                    for j in range(SceneSettings.tileYnum):
                        self.window.blit(self.map[i][j], 
                                        (SceneSettings.tileWidth * i- self.cameraX, SceneSettings.tileHeight * j- self.cameraY))
            for obs in self.obstacles.sprites():
                obs.draw(self.window,self.cameraX,self.cameraY)
            for dec in self.decorates.sprites():             
                dec.draw(self.window,self.cameraX,self.cameraY)
            for mon in self.monsters.sprites(): 
                mon.draw(self.window,self.cameraX,self.cameraY)
            for bra in self.breakobj.sprites(): 
                bra.draw(self.window,self.cameraX,self.cameraY)
            for portal in self.portals.sprites():
                portal.draw(self.window,self.cameraX,self.cameraY)

            if player.is_colliding():
                player.draw(self.window,player.dx,player.dy)
            else:
                player.draw(self.window,0,0)
        
            if player.collidingWith["bra"] and keys[pygame.K_SPACE]:
                for bra in player.collidingObject["bra"]:
                    self.breakobj.remove(bra)
            if player.collidingWith["portal"]:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH))
