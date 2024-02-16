import pygame
import sys
from collections import deque
import os
from settings import *

class Opening:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load('resources/Opening.jpeg')
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.start_trigger = False
        
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render('Press Any Key to Enter...', True, 'white')
        
    def run(self):
        while True:
            self.game.screen.blit(self.image, (0, 0))
            self.game.screen.blit(self.text, (600, 700))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.start_trigger = True
            if self.start_trigger:
                break