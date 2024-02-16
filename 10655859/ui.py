import pygame
from settings import *

class UI:
    def __init__(self, game):
        self.game = game
        self.health = Player_Initial_Health
        self.armor = 0
            
    def update(self):
        self.health = self.game.player.health
        self.health = max(self.health, 0)
        self.armor = self.game.settings.Player_Armor
        
    def get_map(self):
        for j,row in enumerate(self.mini_map):
            for i,value in enumerate(row):
                if value:
                    self.world_map[(i,j)] = value
                    
    def draw(self):
        for i in range(int(self.health / 5)):
            pygame.draw.rect(self.game.screen, 'white', (1580 - 20 * (int(self.health / 5) - i), 30, 10, 20), 0)
        for i in range(int(self.health / 5), 20):
            pygame.draw.rect(self.game.screen, 'grey', (1580 - 20 * (20 + int(self.health / 5) - i), 30, 10, 20), 2)
        for i in range(int(self.armor / 5)):
            pygame.draw.rect(self.game.screen, (135, 206, 250), (1580 - 20 * (int(self.armor / 5) - i), 55, 10, 20), 0)