import pygame
import sys
from collections import deque
import os
from settings import *

class CG:
    def __init__(self, game, num):
        self.game = game
        self.cg_fps = 12
        if not num:
            self.image = pygame.image.load('resources/CG/town/00.png')
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
            self.path = ('resources/CG/town/00.png').rsplit('/', 1)[0]
            self.images = self.get_images(self.path)
            self.num_images = len(self.images)
        
            self.font = pygame.font.Font(None, 60)
            self.text = self.font.render('Entering the Abandoned Town', True, 'white')
        else:
            self.image = pygame.image.load('resources/CG/arena/0100.png')
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
            self.path = ('resources/CG/arena/0100.png').rsplit('/', 1)[0]
            self.images = self.get_images(self.path)
            self.num_images = len(self.images)
        
            self.font = pygame.font.Font(None, 60)
            self.text = self.font.render('    Entering the Royal Arena', True, 'white')

        self.anim_counter = 0
        
    def run(self):
        while self.anim_counter < self.num_images - 1:
            self.game.delta_time = self.game.clock.tick(self.cg_fps)
            pygame.display.set_caption(f'{self.game.clock.get_fps() :.1f}')
            
            self.cg_logic()
            
            self.game.screen.blit(self.image, (0,0))
            self.game.screen.blit(self.text, (500, 700))
            pygame.display.flip()
            
    def cg_logic(self):
        self.images.rotate(-1)
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.anim_counter += 1
        
    def get_images(self, path):
        images = deque()
        for files in os.listdir(path):
            if os.path.isfile(os.path.join(path, files)):
                img = pygame.image.load(path + '/' + files).convert_alpha()
                images.append(img)
        return images