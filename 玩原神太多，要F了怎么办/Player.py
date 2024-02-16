# -*- coding:utf-8 -*-

import pygame

from Settings import *
import Info
# from Info import *
# import User


class Player(pygame.sprite.Sprite):
    def __init__(self, window, user) -> None:
        super().__init__()
        self.window = window
        self.user = user
        self.info = Info.Info(user.info.info)
        self.speed = PlayerSettings.speed

        self.images = [[pygame.transform.scale(pygame.image.load(img),
                                               (PlayerSettings.width, PlayerSettings.height)) for img in dir] for dir in PlayerSettings.path]
        self.imageID = 0
        self.image = self.images[self.info.get_info("direction")][self.imageID]

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.info.get_info("x"), self.info.get_info("y"))
        self.rect.y += PlayerSettings.height - PlayerSettings.legHeight
        self.rect.height = PlayerSettings.legHeight - PlayerSettings.footHeight
        self.rect.x += (PlayerSettings.width - PlayerSettings.rectWidth) // 2
        self.rect.width = PlayerSettings.rectWidth

    def topleft(self):
        return (self.rect.x - (PlayerSettings.width - PlayerSettings.rectWidth) // 2,
                self.rect.y - (PlayerSettings.height - PlayerSettings.legHeight))

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def updateInfoXY(self):
        xy = self.topleft()
        self.info.modify("x", xy[0])
        self.info.modify("y", xy[1])

    # 注意这里对信息的打包！！！
    def zip(self):
        zipSelf = {
            "info": self.info,
            # "imgaeID" : self.imageID,
            # "image" : self.image,
            "rect": self.rect
        }
        return zipSelf

    def unzip(self, zip):
        self.info = zip["info"]
        # self.imgaeID = zip["imgaeID"]
        # self.image = zip["image"]
        self.rect = zip["rect"]

    def update(self, keys):
        dx = 0
        dy = 0
        ifRunning = keys[pygame.K_LSHIFT]
        self.speed = PlayerSettings.runSpeed if ifRunning else PlayerSettings.speed
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            dy -= self.speed
            if self.info.get_info("direction") != 0:
                self.info.modify("direction", 0)
                self.imageID = 0
            else:
                self.imageID = (self.imageID + 1) % len(
                    self.images[self.info.get_info("direction")] * PlayerSettings.walkPeriod)
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < MapSettings.height:
            dy += self.speed
            if self.info.get_info("direction") != 1:
                self.info.modify("direction", 1)
                self.imageID = 0
            else:
                self.imageID = (self.imageID + 1) % len(
                    self.images[self.info.get_info("direction")] * PlayerSettings.walkPeriod)
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            dx -= self.speed
            if self.info.get_info("direction") != 2:
                self.info.modify("direction", 2)
                self.imageID = 0
            else:
                self.imageID = (self.imageID + 1) % len(
                    self.images[self.info.get_info("direction")] * PlayerSettings.walkPeriod)
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < MapSettings.width:
            dx += self.speed
            if self.info.get_info("direction") != 3:
                self.info.modify("direction", 3)
                self.imageID = 0
            else:
                self.imageID = (self.imageID + 1) % len(
                    self.images[self.info.get_info("direction")] * PlayerSettings.walkPeriod)

        if dx == 0 and dy == 0:
            self.imageID = 0

        self.move(dx, dy)
        # if pygame.sprite.spritecollide(self, obstacles, False):
        # self.move(-dx, -dy)

        self.updateInfoXY()
        self.image = self.images[self.info.get_info(
            "direction")][self.imageID // PlayerSettings.walkPeriod]

    def save(self):
        self.user.saveInfo(self.info)
