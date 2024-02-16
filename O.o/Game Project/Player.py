# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from typing import *
from random import randint


class Player(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, fontSize: int = DialogSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255)):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)

        ##### Your Code Here ↓ #####
        self.images = [[pygame.transform.scale(pygame.image.load(img), (PlayerSettings.playerWidth,
                                                                        PlayerSettings.playerHeight))
                        for img in image_list] for image_list in GamePath.player]

        self.hpImage = pygame.transform.scale(pygame.image.load(GamePath.player_HP),
                                              (PlayerSettings.heartWidth,
                                               PlayerSettings.heartHeight))
        self.attackImage = pygame.transform.scale(pygame.image.load(GamePath.player_Attack),
                                                  (PlayerSettings.heartWidth,
                                                   PlayerSettings.heartHeight))
        self.defenceImage = pygame.transform.scale(pygame.image.load(GamePath.player_Defence),
                                                   (PlayerSettings.heartWidth,
                                                    PlayerSettings.heartHeight))
        self.moneyImage = pygame.transform.scale(pygame.image.load(GamePath.player_Money),
                                                 (PlayerSettings.heartWidth,
                                                  PlayerSettings.heartHeight))
        self.fires = [pygame.transform.scale(pygame.image.load(img), (PlayerSettings.fireWidth,
                                                                      PlayerSettings.fireHeight)) for img in
                      GamePath.fireImage]
        self.fireIndex = 0
        self.fire = self.fires[self.fireIndex]
        self.flashs = [pygame.transform.scale(pygame.image.load(img),  # 人物攻击特效加载
                                              (BattleSettings.flashWidth, BattleSettings.flashHeight))
                       for img in GamePath.flash[randint(0, 2)]]
        self.flashIndex = 0
        self.flash = self.flashs[self.flashIndex]
        self.sounds = [pygame.mixer.Sound(sound) for sound in GamePath.playerSound]

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.direction = PlayerDirection.Right.value
        self.index = 0
        self.image = self.images[self.direction][self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = PlayerSettings.playerSpeed
        self.talking = False
        self.buying = False
        self.burning = False

        self.movingWest = False
        self.movingEast = False
        self.movingNorth = False
        self.movingSouth = False
        self.dx = 0
        self.dy = 0
        self.facingEast = True

        self.HP = PlayerSettings.playerHP
        self.Attack = PlayerSettings.playerAttack
        self.Defence = PlayerSettings.playerDefence
        self.Money = PlayerSettings.playerMoney
        self.Weak = 0  # 削弱怪物，作为商店中的？？？出售
        ##### Your Code Here ↑ #####

    def attr_update(self, addCoins=0, addHP=0, addAttack=0, addDefence=0, addWeak=0):
        ##### Your Code Here ↓ #####
        if self.Money + addCoins < 0:
            return
        if self.HP + addHP <= 0:
            return
        self.Money += addCoins
        self.HP += addHP
        self.Attack += addAttack
        self.Defence += addDefence
        self.Weak += addWeak
        ##### Your Code Here ↑ #####

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        ##### Your Code Here ↓ #####
        self.rect.x = x
        self.rect.y = y
        ##### Your Code Here ↑ #####

    def reset_scene(self):
        # 人物重置时将重叠的障碍物移除
        if self.collidingWith['obstacle']:
            for obstacle in self.collidingObject['obstacle']:
                obstacle.kill()
            self.collidingWith['obstacle'] = False
            self.collidingObject['obstacle'] = []

    def try_move_width(self):
        ##### Your Code Here ↓ #####
        '''尝试移动'''
        if not self.talking and not self.buying:
            self.dx = 0

            if self.movingWest and self.rect.left > 0:
                self.dx -= self.speed

            if self.movingEast and self.rect.right < WindowSettings.width:
                self.dx += self.speed

            self.rect = self.rect.move(self.dx, 0)

    def try_move_height(self):
        if not self.talking and not self.buying:
            self.dy = 0

            if self.movingNorth and self.rect.top > 0:
                self.dy -= self.speed

            if self.movingSouth and self.rect.bottom < WindowSettings.height:
                self.dy += self.speed

            self.rect = self.rect.move(0, self.dy)
        ##### Your Code Here ↑ #####

    def update(self, width, height):
        ##### Your Code Here ↓ #####
        '''调整坐标，播放角色动画'''
        if not self.talking and not self.buying:
            redx = 0  # 重置移动的距离
            redy = 0
            if self.collidingWith['obstacle']:
                redx = width
                redy = height

            if self.dx or self.dy:
                if self.dx > 0:
                    self.direction = PlayerDirection.Right.value
                if self.dx < 0:
                    self.direction = PlayerDirection.Left.value
                if self.dy > 0:
                    self.direction = PlayerDirection.Down.value
                if self.dy < 0:
                    self.direction = PlayerDirection.Up.value
                self.index = (self.index + 1 / 2) % len(self.images[self.direction])
                self.image = self.images[self.direction][int(self.index)]
            else:
                self.image = self.images[self.direction][0]

            self.rect = self.rect.move(redx, redy)
            self.collidingWith['obstacle'] = False
            self.collidingObject['obstacle'] = []
        else:
            self.index = 0
            self.image = self.images[self.direction][self.index]
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        self.rect = self.rect.move(dx, dy)
        window.blit(self.image, self.rect)
        if self.burning:  # 人物着火
            self.fire_update()
            window.blit(self.fire, (self.rect.x + 17, self.rect.y + 25))

        ##### Your Code Here ↑ #####

    def state_update(self, window):  # 人物状态栏
        if not self.talking:
            if self.HP <= 10:
                for hp in range(self.HP):
                    window.blit(self.hpImage, (50 + hp * PlayerSettings.heartGap, 50))
            else:
                window.blit(self.hpImage, (50, 50))
                window.blit(self.font.render('×' + str(self.HP), True, self.fontColor), (100, 60))
            window.blit(self.attackImage, (50, 100))
            window.blit(self.font.render(':' + str(self.Attack), True, self.fontColor), (100, 110))
            window.blit(self.defenceImage, (50, 150))
            window.blit(self.font.render(':' + str(self.Defence), True, self.fontColor), (100, 160))
            window.blit(self.moneyImage, (50, 200))
            window.blit(self.font.render(':' + str(self.Money), True, self.fontColor), (100, 210))

    def fire_update(self):  # 人物着火动画
        self.fireIndex = (self.fireIndex + 1 / 3) % len(self.fires)
        self.fire = self.fires[int(self.fireIndex)]

    def attacking(self, count, window):  # 人物攻击动画
        if count == 10:  # 每次随机使用技能
            index = randint(0, 2)
            self.flashs = [pygame.transform.scale(pygame.image.load(img),
                                                  (BattleSettings.flashWidth, BattleSettings.flashHeight))
                           for img in GamePath.flash[index]]
            sound = self.sounds[index]
            pygame.mixer.Sound.play(sound)
        self.flashIndex = (self.flashIndex + 1) % len(self.flashs)
        self.flash = self.flashs[self.flashIndex]
        window.blit(self.flash, (BattleSettings.monsterCoordX + 70, BattleSettings.monsterCoordY + 40))
