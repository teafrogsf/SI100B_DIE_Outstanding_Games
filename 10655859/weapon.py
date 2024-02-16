import pygame
from collections import deque
from sprite_object import *

class Weapon(AnimatedObject):
    def __init__(self, game, path='resources/sprites/weapon/0.png', scale=0.5, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque([
            pygame.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
            for img in self.images
            ])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 20
        
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render('__   __', True, 'white')
        
    def fire_animation(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter >= self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
        
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
        self.game.screen.blit(self.text, (737, 500))
        
    def update(self):
        self.check_animation_time()
        self.fire_animation()