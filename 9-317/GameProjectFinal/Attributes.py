import pygame
import Player
import NPCs
import Scene
from Settings import *

# check player collid with every sprites
class Collidable:
    def __init__(self, scene:Scene.Scene):
        self.collidingWith = {
            "npcNormal":False,
            "npcTrader":False, 
            "npcTrainer":False,
            "npcBoss":False, 
            "obstacle":False,
            "walls":False,
            "stones":False,
            "gym":False,
            "shop":False,
            "citystation":False,
            "wildstation":False,
            "hospital":False,
            "grass": False,
            "portal": False,
        }
        self.collidingObject = {
            "npcNormal":scene.npcsNormal,
            "npcTrader":scene.npcsTrader, 
            "npcTrainer":scene.npcsTrainer,
            "npcBoss":None,
            "obstacle":scene.obstacles,
            "walls":scene.walls,
            "stones":scene.stones,
            "gym":scene.gym,
            "shop":scene.shop,
            "citystation":scene.citystation,
            "wildstation":scene.wildstation,
            "hospital":scene.hospital,
            "grass": scene.grasses,
            "portal": scene.portal,
        }
    
    def is_colliding_npcNormal(self, player:Player.Player, npc:NPCs.NPCnormal):
        if pygame.sprite.collide_rect(player, npc):
            self.collidingWith["npcNormal"] = True
        else:
            self.collidingWith["npcNormal"] = False
        return self.collidingWith["npcNormal"]
    def is_colliding_npcTrader(self, player:Player.Player, npc:NPCs.NPCtrader):
        if pygame.sprite.collide_rect(player, npc):
            self.collidingWith["npcTrader"] = True
        else:
            self.collidingWith["npcTrader"] = False
        return self.collidingWith["npcTrader"]
    def is_colliding_npcTrainer(self, player:Player.Player, npc:NPCs.NPCtrainer):
        if pygame.sprite.collide_rect(player, npc):
            self.collidingWith["npcTrainer"] = True
        else:
            self.collidingWith["npcTrainer"] = False
        return self.collidingWith["npcTrainer"]
    def is_colliding_npcBoss(self, player:Player.Player):
        for npc in self.collidingObject["npcBoss"].sprites():
            if pygame.sprite.collide_rect(player, npc):
                self.collidingWith["npcBoss"] = True
            else:
                self.collidingWith["npcBoss"] = False
        return self.collidingWith["npcBoss"]
    
    def is_colliding_obstacle(self, player:Player.Player):
        if self.collidingObject["obstacle"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["obstacle"], False):
                self.collidingWith["obstacle"] = True
            else:
                self.collidingWith["obstacle"] = False
        else:
            self.collidingWith["obstacle"] = False
    def is_colliding_walls(self, player:Player.Player):
        if self.collidingObject["walls"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["walls"], False):
                self.collidingWith["walls"] = True
            else:
                self.collidingWith["walls"] = False
        else:
            self.collidingWith["walls"] = False
    def is_colliding_stones(self, player:Player.Player):
        if self.collidingObject["stones"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["stones"], False):
                self.collidingWith["stones"] = True
            else:
                self.collidingWith["stones"] = False
        else:
            self.collidingWith["stones"] = False
    def is_colliding_gym(self, player:Player.Player):
        if self.collidingObject["gym"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["gym"], False):
                self.collidingWith["gym"] = True
            else:
                self.collidingWith["gym"] = False
        else:
            self.collidingWith["gym"] = False
    def is_colliding_shop(self, player:Player.Player):
        if self.collidingObject["shop"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["shop"], False):
                self.collidingWith["shop"] = True
            else:
                self.collidingWith["shop"] = False
        else:
            self.collidingWith["shop"] = False
    def is_colliding_citystation(self, player:Player.Player):
        if self.collidingObject["citystation"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["citystation"], False):
                self.collidingWith["citystation"] = True
            else:
                self.collidingWith["citystation"] = False
        else:
            self.collidingWith["citystation"] = False
    def is_colliding_wildstation(self, player:Player.Player):
        if self.collidingObject["wildstation"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["wildstation"], False):
                self.collidingWith["wildstation"] = True
            else:
                self.collidingWith["wildstation"] = False
        else:
            self.collidingWith["wildstation"] = False
    def is_colliding_hospital(self, player:Player.Player):
        if self.collidingObject["hospital"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["hospital"], False):
                self.collidingWith["hospital"] = True
            else:
                self.collidingWith["hospital"] = False
        else:
            self.collidingWith["hospital"] = False

    # check every object that stop player moving
    def is_colliding_not_move(self, player:Player.Player):
        self.is_colliding_obstacle(player)
        self.is_colliding_walls(player)
        self.is_colliding_stones(player)
        self.is_colliding_gym(player)
        self.is_colliding_shop(player)
        self.is_colliding_citystation(player)
        self.is_colliding_wildstation(player)
        self.is_colliding_hospital(player)
        
        return (self.collidingWith["obstacle"] or
                self.collidingWith["walls"] or
                self.collidingWith["stones"] or
                self.collidingWith["gym"] or
                self.collidingWith["shop"] or
                self.collidingWith["citystation"] or
                self.collidingWith["wildstation"] or
                self.collidingWith["hospital"])
    
    def is_colliding_grass(self, player:Player.Player):
        if self.collidingObject["grass"] is not None:
            if pygame.sprite.spritecollide(player, self.collidingObject["grass"], False):
                self.collidingWith["grass"] = True
            else:
                self.collidingWith["grass"] = False
        else:
            self.collidingWith["grass"] = False
        return self.collidingWith["grass"]
    
    
    def is_colliding_portal(self, player:Player.Player, portal):
        if pygame.sprite.collide_rect(player, portal):
            self.collidingWith["portal"] = True
        else:
            self.collidingWith["portal"] = False
        return self.collidingWith["portal"]
