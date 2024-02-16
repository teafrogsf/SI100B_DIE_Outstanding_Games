# -*- coding:utf-8 -*-

class Collidable:
    def __init__(self):
        self.collidingWith = {
            "obstacle": False, 
            "monster": False,
            "decorate":False,
            "shop_npc": False,
            "dialog_npc":False,  
            "portal": False, 
            "boss": False, 
            "bra":False,
            "animal":False,
            "animalgame_npc":False
        }
        self.collidingObject = {
            "obstacle": [], 
            "decorate":[],
            "shop_npc":[],
            "dialog_npc":[], 
            "monster": None, 
            "portal": None, 
            "boss": None, 
            "bra":[],
            "animalgame_npc":[]
        }
    
    def is_colliding(self):
        return (self.collidingWith["obstacle"] or 
                self.collidingWith["monster"] or
                self.collidingWith["decorate"] or
                self.collidingWith["shop_npc"] or
                self.collidingWith["dialog_npc"] or
                self.collidingWith["portal"] or 
                self.collidingWith["boss"] or
                self.collidingWith["animal"] or
                self.collidingWith["bra"] or
                self.collidingWith["animalgame_npc"])
