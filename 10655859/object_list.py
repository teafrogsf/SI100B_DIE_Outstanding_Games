import pygame
from random import randrange
from sprite_object import *
from npc import *

class ObjectList:
    def __init__(self, map):
        self.map = map
        self.game = map.game
        self.sprite_list = []
        self.anim_sprite_path = 'resources/sprites/objects/'
        self.npc_list = []
        self.enemy_path = 'resources/sprites/enemy/'
        
        self.num_npc = 0
        
        if self.map.num:
            self.enemy_numbers = 5
            self.num_s = 10
            self.num_d = 10
        else:
            self.enemy_numbers = self.game.settings.Enemy_Num
            self.num_s = 3
            self.num_d = 0
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.victory_counter = 0
        
        self.sprite_position_list = {}
        self.enemy_position_list = {}
        
        self.add_sprite()
        
        self.add_npc()
        
    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        self.num_npc = 0
        for npc in self.npc_list:
            if self.num_npc < 6 or (not npc.isalive):
                npc.update(1)
                if npc.trace_trigger and npc.isalive:
                    self.num_npc += 1
            else:
                npc.update(0)
        self.enemy_position_list = {npc.map_pos for npc in self.npc_list if npc.isalive and npc.state}
        if not len(self.enemy_position_list) and self.victory_counter < 10:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            self.game.object_renderer.player_win()
            pygame.time.delay(400)
            if self.game.weapon.animation_trigger:
                self.victory_counter += 1
            
    
    def add_sprite(self):
        directions = [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]
        for y in range(1, self.map.map_length - 1):
            for x in range(1, self.map.map_width - 1):
                delta_x, delta_y = 0.5, 0.5
                num = 0
                for dx, dy in directions:
                    if (x + dx, y + dy) in self.map.world_map:
                        delta_x += 0.1 * dx
                        delta_y += 0.1 * dy
                        num += 1
                    if (x + dx, y + dy) in self.sprite_position_list:
                        num = 10
                        break
                if 7 > num > 3:
                    self.sprite_list.append(AnimatedObject(self.game, path=self.anim_sprite_path+'0.png', pos=(x + delta_x, y + delta_y)))
                    self.sprite_position_list[(x, y)] = 1
        
    def add_npc(self):
        for i in range(self.enemy_numbers):
            pos = x, y = randrange(self.map.map_width), randrange(self.map.map_length)
            while (pos in self.map.world_map) or (pos in self.restricted_area) or (pos in self.map.irreachable):
                pos = x, y = randrange(self.map.map_width), randrange(self.map.map_length)
            randnum = randint(1, 10)
            if randnum > self.num_s:
                self.npc_list.append(Soldier(self.game, pos=(x+0.5, y+0.5)))
            elif randnum > self.num_d:
                self.npc_list.append(Demon(self.game, pos=(x+0.5, y+0.5)))
            else:
                self.npc_list.append(Giant(self.game, pos=(x+0.5, y+0.5)))
            if self.game.settings.Enemy_Num <= 90:
                self.restricted_area.add((x, y))