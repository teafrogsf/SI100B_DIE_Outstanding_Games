import pygame
from sprite_object import *
from collision_detction import *
from pathfinding import *
from random import randint, random, choice

class NPC(AnimatedObject):
    def __init__(self, game, path='resources/sprites/enemy/soldier/0.png', pos=(8.5,3.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.path = path.rsplit('/', 1)[0]
        self.attack_images = self.get_images(self.path + '/attack')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')
        self.death_images = self.get_images(self.path + '/death')

        self.attack_dist = 6
        self.attack_tick = 0
        self.attack_counter = 0
        self.attack_damage = self.game.settings.Enemy_Attack
        self.accuracy_1 = 0.5
        self.accuracy_2 = 0.02
        self.accuracy = self.accuracy_1
        self.last_dist = 6
        
        self.speed = 0.06
        self.size = 0.1
        
        self.health = 100
        self.isalive = True
        self.ispain = False
        self.isattack = False
        self.death_frame_counter = 0
        self.state = False
        
        self.ray_cast_value = False
        self.trace_trigger = False
        
    def update(self, state):
        self.check_animation_time()
        self.get_sprite()
        self.state = state
        if self.isalive:
            self.ray_cast_value = self.ray_cast()
            if self.ray_cast_value:
                self.trace_trigger = True
            self.check_if_hit()
            if self.ispain:
                self.pain_anim()
                self.game.sound.enemy_pain.play()
            self.check_if_dead()
        if state:
            self.enemy_logic()
        self.draw()
        
    def pain_anim(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.ispain = False
            
    def death_anim(self):
        if not self.isalive:
            if self.animation_trigger and self.death_frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.death_frame_counter += 1
        
    def check_if_hit(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.spirit_half_width - 75 < self.screen_x < HALF_WIDTH + self.spirit_half_width + 75:
                self.ispain = True
                self.health -= self.game.weapon.damage
                self.game.scene_manager.counter11 = 0
                if self.dist < 4:
                    self.health -= self.game.weapon.damage * 9

    def check_if_dead(self):
        if self.health < 1:
            self.game.sound.enemy_death.play()
            self.isalive = False
            pygame.event.post(pygame.event.Event(Kill_Event))
            
    def movement(self, next_p):
        self.animate(self.walk_images)
        
        next_x, next_y = next_p
        next_p_map = int(next_x), int(next_y)
                
        if next_p_map not in self.game.map.object_list.enemy_position_list:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            collision_detection = CollisionDetection(self.game, self.x, self.y, dx, dy, self.size)
            self.x, self.y = collision_detection.check_wall_collision()
            
    def attack_act(self):
        if self.animation_trigger:
            self.image = self.attack_images[0]
            if self.attack_counter == self.attack_tick:
                self.game.sound.enemy_attack.play()
                if random() < self.accuracy:
                    self.game.player.get_damage(self.attack_damage)
            self.attack_counter += 1
            self.attack_images.rotate(-1)
            if self.attack_counter == len(self.attack_images):
                self.attack_counter = 0
                
    def enemy_logic(self):
        if self.map_pos in self.game.map.world_map:
            ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
            for dx, dy in ways:
                if (int(self.x) + dx, int(self.y) + dy) not in self.game.map.world_map:
                    self.x, self.y = self.x + dx, self.y + dy
                    break
        if self.isalive:
            if self.ispain:
                pass
            elif self.ray_cast_value:
                if self.dist < self.attack_dist:
                    self.accuracy = self.accuracy_1
                    if self.dist < self.last_dist or (self.attack_dist == 6 and self.dist < 1):
                        self.accuracy = self.accuracy_2
                    self.attack_act()
                    self.last_dist = self.dist
                else:
                    if self.attack_counter > 0:
                        self.attack_counter = 0
                        self.attack_images = self.get_images(self.path + '/attack')
                    self.movement(Pathfinding(self.game).get_path(self.map_pos, self.game.player.map_pos))
            elif self.trace_trigger:
                if self.attack_counter > 0:
                    self.attack_counter = 0
                    self.attack_images = self.get_images(self.path + '/attack')
                self.movement(Pathfinding(self.game).get_path(self.map_pos, self.game.player.map_pos))
        else:
            self.death_anim()
            
    def ray_cast(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def draw(self):
        if self.isalive:
            if self.trace_trigger:
                pygame.draw.circle(self.game.screen, 'red', (10 * self.x, 10 * self.y), 2)
            else:
                pygame.draw.circle(self.game.screen, 'orange', (10 * self.x, 10 * self.y), 2)
            '''
            if self.ray_cast():
                pygame.draw.line(self.game.screen, 'orange', (10 * self.game.player.x, 10 * self.game.player.y),
                         (10 * self.x, 10 * self.y), 2)
            '''
        else:
            pygame.draw.circle(self.game.screen, 'blue', (10 * self.x, 10 * self.y), 2)
            
class Soldier(NPC):
    def __init__(self, game, path='resources/sprites/enemy/soldier/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        

class Demon(NPC):
    def __init__(self, game, path='resources/sprites/enemy/demon/0.png', pos=(10.5, 6.5), scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.attack_damage = int(self.game.settings.Enemy_Attack * 3)
        self.attack_tick = 2
        self.accuracy_1 = 0.8
        self.accuracy_2 = 0.8
        
        self.speed = 0.08
        
        self.health = 200
        

class Giant(NPC):
    def __init__(self, game, path='resources/sprites/enemy/giant/0.png', pos=(11.5, 6.0), scale=1.2, shift=0.04, animation_time=400):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 7
        self.attack_damage = int(self.game.settings.Enemy_Attack * 8)
        self.attack_tick = 6
        self.accuracy_1 = 1
        self.accuracy_2 = 1
        
        self.speed = 0.02
        
        self.health = 600