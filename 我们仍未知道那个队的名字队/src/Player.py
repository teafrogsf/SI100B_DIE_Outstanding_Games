import pygame
from Setting import *
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load(img) for img in GamePath.player]
        self.images = [pygame.transform.scale(img, (PlayerSettings.width, PlayerSettings.width)) for img in self.images]
        self.imgIndex = 0
        self.image = self.images[self.imgIndex]

        self.rect = self.image.get_rect()

        self.speedX = PlayerSettings.speed
        self.speedY = PlayerSettings.speed

        self.HP = PlayerSettings.initHP
        self.ATK = PlayerSettings.initATK
        self.DEF = PlayerSettings.initDEF

        self.money = PlayerSettings.initMoney

        self.inventory = []
        
        self.talking = False
        self.lastUpdateImgTime = pygame.time.get_ticks()

        self.canOnlyMoveInY = False

    def move(self, keys):
        if not self.talking:
            dx = 0
            dy = 0
            if self.canOnlyMoveInY:
                self.speedY = PlayerSettings.universeSpeedY
                if keys[pygame.K_w]:
                    dy -= self.speedY
                if keys[pygame.K_s]:
                    dy += self.speedY
                dx = PlayerSettings.universeSpeedX
            else:
                self.speedY = PlayerSettings.speed
                self.speedX = PlayerSettings.speed    
                if keys[pygame.K_w]:
                    dy -= self.speedY
                if keys[pygame.K_s]:
                    dy += self.speedY
                if keys[pygame.K_a]:
                    dx -= self.speedX
                if keys[pygame.K_d]:
                    dx += self.speedX
            self.rect.centerx += dx
            self.rect.centery += dy

    def move_cancel(self, keys, isCollide):
            if isCollide:
                dx = 0
                dy = 0
                if keys[pygame.K_w]:
                    dy -= self.speedY
                if keys[pygame.K_s]:
                    dy += self.speedY
                if keys[pygame.K_a]:
                    dx -= self.speedX
                if keys[pygame.K_d]:
                    dx += self.speedX
                self.rect = self.rect.move(-dx, -dy)

    def update(self, keys):
        self.rect = self.image.get_rect(center = self.rect.center) # 图片更新
        if self.talking:
            #如果不移动，显示静态图像
            self.imgIndex = 0
            self.image = self.images[self.imgIndex]
        else:
            #如果移动 判断是否是与上次更新间隔一定时间 再更新
            currentTime = pygame.time.get_ticks()
            if currentTime - self.lastUpdateImgTime > fps//3:
                self.lastUpdateImgTime = currentTime
                if keys[pygame.K_s] :
                    self.imgIndex += 1
                    if self.imgIndex < 0 or self.imgIndex > 3 :
                        self.imgIndex = 0
                if keys[pygame.K_a] :
                    self.imgIndex += 1
                    if self.imgIndex < 4 or self.imgIndex > 7 :
                        self.imgIndex = 4
                if keys[pygame.K_d] :
                    self.imgIndex += 1
                    if self.imgIndex < 8 or self.imgIndex > 11 :
                        self.imgIndex = 8
                if keys[pygame.K_w] :
                    self.imgIndex += 1
                    if self.imgIndex < 12 or self.imgIndex > 15 :
                        self.imgIndex = 12
                self.image = self.images[self.imgIndex]