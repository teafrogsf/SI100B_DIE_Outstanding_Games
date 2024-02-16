import pygame
from random import randint

class MapCreator:
    def __init__(self, game, map):
        self.game = game
        self.map = map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        
    def BerlinNoise(self):
        layers = []
        for i in range(26):
            layers.append([])
            for j in range(26):
                layers[i].append(1)
        for i in range(int(24 * 24 * 0.6)):
            x = randint(1, 24)
            y = randint(1, 24)
            while layers[x][y] == 0:
                x = randint(1, 24)
                y = randint(1, 24)
            layers[x][y] = 0
        for i in range(1, 6):
            for j in range(1, 6):
                layers[i][j] = 0
        layers[2][0] = 2
        for i in range(22, 25):
            for j in range(22, 25):
                layers[i][j] = 0
        layers[24][25] = 2
        layers = self.CreatPath(1, 1, 24, 24, layers)
        layers = self.CheckMap(layers)
        return layers
    
    def CreatPath(self, x1, y1, x2, y2, m):
        x, y = x1, y1
        dx , dy = int((x2-x1)/abs(x2-x1)), int((y2-y1)/abs(y2-y1))
        for i in range(x2 - x1 + y2 - y1):
            a = randint(0, 1)
            if a:
                if x == x2:
                    y += dy
                else:
                    x += dx
            else:
                if y == y2:
                    x += dy
                else:
                    y += dx
            m[x][y] = 0
        return m
    
    def CheckMap(self, m):
        m2 = m
        m2[1][1] = 5
        m2 = self.dfs(1, 1, m2)
        for i in range(26):
            for j in range(26):
                if m2[i][j] == 0:
                    self.map.irreachable[(j, i)] = 1
                elif m2[i][j] == 5:
                    m[i][j] = 0
        return m
        
    def dfs(self, x, y, m):
        for dx, dy in self.ways:
            if m[x+dx][y+dy] == 0:
                m[x+dx][y+dy] = 5
                m = self.dfs(x+dx, y+dy, m)
        return m
        