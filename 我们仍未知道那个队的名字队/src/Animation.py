import pygame
from Setting import GamePath, fps, baseWidth
class Animation:
    def __init__(self, type):
        self.frames = None
        self.speed = 0
        self.currentFrame = 0  # 当前帧
        self.isPlaying = False  # 动画是否在播放
        self.type = type
        self.CD = 0
        self.position = (0,0)
        if self.type == 'Sword' or self.type == 'Sword2':
            self.frames = [pygame.image.load(frame) for frame in GamePath.swordFrames]
            self.speed = 10
        elif self.type == 'Gun':
            self.frames = [pygame.image.load(frame) for frame in GamePath.gunFrames]
            self.speed = 10
        elif self.type == 'Axe':
            self.frames = [pygame.image.load(frame) for frame in GamePath.axeFrames]
            self.speed = 10
        elif self.type == 'Hand':
            self.frames = [pygame.image.load(frame) for frame in GamePath.handFrames]
            self.speed = 10
        elif self.type == 'Shield':
            self.frames = [pygame.image.load(frame) for frame in GamePath.shieldFrames]
            self.speed = 10
        elif self.type == 'Charge':
            self.frames = [pygame.image.load(frame) for frame in GamePath.chargeFrames]
            self.speed = 10
        elif self.type == 'Poison':
            self.frames = [pygame.image.load(frame) for frame in GamePath.poisonFrames]
            self.speed = 10
        elif self.type == 'Enemy':
            self.frames = [pygame.image.load(frame) for frame in GamePath.enemyFrames]
            self.speed = 10

    def play(self, position):
        self.isPlaying = True
        self.currentFrame = 0  # 从第一帧开始播放
        self.position = position

    def update(self):
        if self.isPlaying:
            if self.type == 'Sword' or self.type == 'Sword2':
                self.CD += 1
                self.position = (self.position[0] + baseWidth // 12, self.position[1])
                if self.CD == fps // 5 * 3:
                    self.isPlaying = False
            else:
                if self.CD < fps // 4 // len(self.frames):
                    self.CD += 1
                else:
                    self.CD = 0
                    self.currentFrame += 1
                    if self.currentFrame == len(self.frames):
                        self.isPlaying = False

    def draw(self, surface):
        if self.isPlaying:
            frame = self.frames[self.currentFrame]
            frameRect = frame.get_rect()
            frameRect.center = self.position
            surface.blit(frame, frameRect)
