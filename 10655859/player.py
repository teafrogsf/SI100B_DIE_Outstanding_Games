from settings import *
from collision_detction import *
import pygame
import math
import time

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = Player_Pos
        self.angle = Player_Angle
        self.shot = False
        self.health = Player_Initial_Health
        self.armor = self.game.settings.Player_Armor
        self.rel = 0
        self.speed = Player_Speed
        self.font = pygame.font.Font(None, 60)
        self.key = pygame.key.get_pressed()
    
    def update(self):
        if self.game.weapon.frame_counter == 0 and self.game.game_on and (self.game.map.object_list.victory_counter == 0 or self.game.map.object_list.victory_counter == 10):
            self.movement()
            self.mouse_control()
        else:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            self.rel = 0
        if self.map_pos in self.game.map.world_map:
            self.x, self.y = Player_Pos
        if self.x < 0 or self.y < 0 or self.x > self.game.map.map_width or self.y > self.game.map.map_length:
            self.x, self.y = Player_Pos
                
        
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = self.speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        key = pygame.key.get_pressed()
        self.key = key
        if key[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if key[pygame.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if key[pygame.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if key[pygame.K_d]:
            dx += -speed_sin
            dy += speed_cos
        
        collision_detection = CollisionDetection(self.game, self.x, self.y, dx, dy, Player_Size_Scale / 100)
        self.x, self.y = collision_detection.check_wall_collision()
        
    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BOARDER_LEFT or mx > MOUSE_BOARDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if my < MOUSE_BOARDER_LEFT or my > HEIGHT - MOUSE_BOARDER_LEFT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        
        self.angle %= math.tau
        
    def get_damage(self, damage):
        d_health = min(damage, self.game.settings.Player_Armor)
        self.game.settings.Player_Armor -= d_health
        self.health -= (damage - d_health)
        pygame.event.post(pygame.event.Event(Player_Hit_Event))
        
    def check_if_end(self):
        if self.health < 1:
            self.game.object_renderer.player_get_over()
            pygame.display.flip()
            self.game.sound.bgm.stop()
            pygame.time.delay(1500)
            self.game.game_on = False
            self.game.new_game(self.game.map.num)
        
    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
        
    def draw(self):
        pygame.draw.line(self.game.screen, 'yellow', (self.x*10, self.y*10),
                     (self.x*10 + 20*math.cos(self.angle),
                     self.y*10 + 20*math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x*10, self.y*10), 2)
        
