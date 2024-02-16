# -*- coding:utf-8 -*-

import sys
import pygame
import Maps
from Player import Player
import Scene 
from Scene import *
from Settings import *
from PopUpBox import *

class GameManager:
    def __init__(self,window):
        self.player=Player(PlayerSettings.playerInitialX,PlayerSettings.playerInitialY)
        self.playerlist=pygame.sprite.Group()
        self.playerlist.add(self.player)
        self.window = window
        self.clock = pygame.time.Clock()
        self.scene = StartMenu(window)
        self.collideindex=0
        self.music=BgmPlayer()
        self.bgm=self.gengamemanager()
  
    def gengamemanager(self):
        self.music.play(0)
    def game_reset(self):
        self.player.initialdata()
        self.music.stop()
        self.music.play(0)

    # Necessary game components here ↓
    def tick(self, fps):
        self.clock.tick(fps)

    # Scene-related update functions here ↓
    def flush_scene(self):
        if self.scene.type == SceneType.HOME:
            self.scene = WildScene(self.window)
            self.music.stop()
            self.music.play(1)
        elif self.scene.type == SceneType.WILD:
            self.scene = HomeScene(self.window)
            self.music.stop()
            self.music.play(0)
            self.scene.animals=self.player.eggborn()
        elif self.scene.type == SceneType.MENU:
            self.scene = HomeScene(self.window)
            self.scene.animals=self.player.eggborn()

    def update(self):
        self.clock.tick(30)
        if self.scene.type == SceneType.MENU:
            self.update_main_menu(pygame.event.get())
        elif self.scene.type == SceneType.HOME:
            self.update_home(pygame.event.get())
        elif self.scene.type == SceneType.WILD:
            self.update_wild(pygame.event.get())

    def update_main_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 传送
            if event.type == GameEvent.EVENT_SWITCH:
                self.player.scenereset(self.scene,2)
                GameManager.flush_scene(self)
            
    def update_home(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.player.exportdata()
                pygame.quit()
                sys.exit()
            if event.type== GameEvent.EVENT_SWITCH:
                GameManager.flush_scene(self)
                self.player.scenereset(self.scene,2)
            elif event.type==GameEvent.EVENT_RESTART:
                self.game_reset()
                self.scene.animals=pygame.sprite.Group()

        if self.player.collidingWith['dialog_npc']==True and self.scene.dialogbox==None:
            self.player.dx=0
            self.player.dy=0
            self.player.dialog=True
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG))
            self.scene.trigger_dialog(self.player.collidingObject['dialog_npc'])
            #print("triggerd dialog in game manager")
        if self.player.collidingWith['animalgame_npc']==True and self.scene.animalgamebox==None:
            self.player.dx=0
            self.player.dy=0
            self.player.dialog=True
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_ANIMALDIALOG))
            self.scene.trigger_animaldialog(self.player.collidingObject['animalgame_npc'])
            #print("triggerd animalgame in game manager")
        if self.player.collidingWith['shop_npc']==True and self.scene.shoppingbox==None:
            self.player.dx=0
            self.player.dy=0
            self.player.dialog=True
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP))
            self.scene.trigger_shop(self.player)
            #print("triggerd shop in game manager")

        if self.scene.dialogbox==None and self.scene.animalgamebox==None and self.scene.shoppingbox==None:
            self.update_collide()
            for each in self.scene.obstacles.sprites():
                each.update()
            for each in self.scene.decorates.sprites():
                each.update()
            for each in self.scene.breakobj.sprites():
                each.update()
            for each in self.scene.portals.sprites():
                each.update()
            for each in self.scene.dialog_npcs.sprites():
                each.update()
            for each in self.scene.animalgame_npc.sprites():
                each.update()
            for each in self.scene.animals.sprites():
                each.walk(self.playerlist,self.scene.animals,self.scene.breakobj,self.scene.obstacles)

            for each in self.scene.wildanimals.sprites():
                each.walk(self.playerlist,self.scene.wildanimals,self.scene.breakobj,self.scene.obstacles)
            if self.player.readytoplay==2:
                self.music.stop()
                self.music.play(0)
                self.player.readytoplay=0
        else:
            if self.scene.dialogbox!=None and self.scene.dialogbox.donedialog==1:
                #print(self.scene.shoppingbox==None,"game manager end dialog after then")
                self.scene.end_dialog(self.player)
            if self.scene.animalgamebox!=None and self.scene.animalgamebox.donedialog!=0:
                if self.scene.animalgamebox.donedialog==1:
                    self.player.readytoplay=0
                if self.scene.animalgamebox.donedialog==2:
                    self.player.readytoplay=1
                    self.scene.trigger_animalgame(self.scene.animalgamebox.hardlevel)
                    self.music.stop()
                    self.music.play(3)
                self.scene.end_animaldialog(self.player)
            if self.scene.shoppingbox!=None and self.scene.shoppingbox.doneshopping==1:
                self.scene.end_shop(self.player)

    def update_wild(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.player.exportdata()
                pygame.quit()
                sys.exit()
            # 传送
            elif event.type== GameEvent.EVENT_SWITCH:
                self.player.scenereset(self.scene,1)
                GameManager.flush_scene(self)


        if self.player.collidingWith['monster']==True and self.scene.battlebox==None:
            self.player.dx=0
            self.player.dy=0
            self.player.battle=True
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))
            self.scene.trigger_battle(self.player)
            self.music.stop()
            if self.player.collidingObject['monster'].type==4:
                self.music.play(4)
            else:
                self.music.play(2)

        if self.scene.battlebox==None:    
            self.update_collide()
            for each in self.scene.obstacles.sprites():
                each.update()
            for each in self.scene.decorates.sprites():
                each.update()
            for each in self.scene.monsters.sprites():
                each.update()
            for each in self.scene.portals.sprites():
                each.update()
        else:
            if self.scene.battlebox.readytoleave==1:
                self.player.money+=self.scene.battlebox.coin
                self.scene.end_battle(self.player)
                self.music.stop()
                self.music.play(1)

    # Collision-relate update funtions here ↓
    def update_collide(self):
        self.player.try_move()
        if pygame.sprite.spritecollide(self.player, self.scene.obstacles, False) :
            self.player.collidingWith["obstacle"]=True
        else:
            self.player.collidingWith["obstacle"]=False

        # Player -> Monsters
        if pygame.sprite.spritecollide(self.player, self.scene.monsters, False) :
            self.player.collidingWith["monster"]=True
            self.player.collidingObject["monster"]=(pygame.sprite.spritecollide(self.player,self.scene.monsters,False)[0])
        
        if pygame.sprite.spritecollide(self.player, self.scene.animalgame_npc, False) :
            self.player.collidingWith["animalgame_npc"]=True
            self.player.collidingObject["animalgame_npc"]=(pygame.sprite.spritecollide(self.player,self.scene.animalgame_npc,False)[0])

        if pygame.sprite.spritecollide(self.player, self.scene.decorates, False) :
            self.player.collidingWith["decorate"]=True
        else:
            self.player.collidingWith["decorate"]=False

        #player→breakableobjects
        if pygame.sprite.spritecollide(self.player, self.scene.breakobj, False) :
            self.player.collidingWith["bra"]=True
            self.player.collidingObject["bra"]=(pygame.sprite.spritecollide(self.player,self.scene.breakobj,False))
        else:
            self.player.collidingWith["bra"]=False
            self.player.collidingObject["bra"]=[]

        if pygame.sprite.spritecollide(self.player, self.scene.animals, False) :
            self.player.collidingWith["animal"]=True
        else:
            self.player.collidingWith["animal"]=False

        if pygame.sprite.spritecollide(self.player, self.scene.wildanimals, False) :
            self.player.collidingWith["animal"]=True
        else:
            self.player.collidingWith["animal"]=False
            
        if pygame.sprite.spritecollide(self.player,self.scene.portals,False) :
            self.player.collidingWith["portal"]=True

        else:
            self.player.collidingWith["portal"]=False

        if pygame.sprite.spritecollide(self.player,self.scene.shop_npcs,False) :
            self.player.collidingWith["shop_npc"]=True
            self.player.collidingObject["shop_npc"]=(pygame.sprite.spritecollide(self.player,self.scene.shop_npcs,False)[0])
        if pygame.sprite.spritecollide(self.player,self.scene.dialog_npcs,False) :
            self.player.collidingWith["dialog_npc"]=True
            self.player.collidingObject["dialog_npc"]=(pygame.sprite.spritecollide(self.player,self.scene.dialog_npcs,False)[0])


    # Render-relate update functions here ↓
    def render(self):
        if self.scene.type==SceneType.MENU:
            self.render_main_menu()
        elif self.scene.type == SceneType.WILD:           
            self.render_wild()
        elif self.scene.type == SceneType.HOME:
            self.render_home()
    
    def render_main_menu(self):
        self.scene.update_menu(self.window)
    
    def render_home(self):
        self.scene.render(self.player)

    def render_wild(self):
        self.scene.render(self.player)
        keys=pygame.key.get_pressed()


