import pygame
from settings import *

class CollisionDetection:
    def __init__(self, game, x, y, dx, dy, scale):
        self.game = game
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.scale = scale
        self.ways = [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1] 
        
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self):
        scale = self.scale
        x1, y1 = 1, 1
        for i in range(0, int(scale * 20) + 1):
            j = i / 20
            for ax, ay in self.ways:
                if not self.check_wall(int(self.x + self.dx + scale * j * ax), int(self.y + scale * j * ay)):
                    x1 = 0
                if not self.check_wall(int(self.x + scale * j * ax), int(self.y + self.dy + scale * j * ay)):
                    y1 = 0
        self.x += self.dx * x1 * self.game.delta_time / 30
        self.y += self.dy * y1 * self.game.delta_time / 30
        return self.x, self.y