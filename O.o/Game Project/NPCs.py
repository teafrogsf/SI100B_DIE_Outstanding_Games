# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from random import randint


class NPC(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, name):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)

        ##### Your Code Here ↓ #####
        self.image = pygame.image.load(GamePath.npc)
        self.image = pygame.transform.scale(self.image, ((5 / 3) * NPCSettings.npcWidth,
                                                         NPCSettings.npcHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.name = name

        self.talking = False
        self.talkCD = 0
        ##### Your Code Here ↑ #####

    def update(self):
        raise NotImplementedError

    def reset_talkCD(self):
        ##### Your Code Here ↓ #####
        '''将talkCD重置'''
        self.talkCD = NPCSettings.talkCD
        self.talking = False
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        self.rect = self.rect.move(dx, dy)
        window.blit(self.image, self.rect)
        ##### Your Code Here ↑ #####


class DialogNPC(NPC):
    def __init__(self, x, y, name, dialog):
        ##### Your Code Here ↓ #####
        super().__init__(x=x, y=y, name=name)
        self.speed = NPCSettings.npcSpeed
        self.facing_East = 1
        self.dialog = dialog
        ##### Your Code Here ↑ #####

    def update(self):
        ##### Your Code Here ↓ #####
        '''传入self.tick(self, fps)方法'''
        if not self.talking:
            if self.talkCD > 0:
                self.talkCD -= 1
        ##### Your Code Here ↑ #####


class ShopNPC(NPC):
    def __init__(self, x, y, name, items, dialog):
        super().__init__(x, y, name)

        ##### Your Code Here ↓ #####
        super().__init__(x=x, y=y, name=name)
        self.image = pygame.transform.scale(pygame.image.load(GamePath.shop),
                                            (ShopSettings.shopWidth, ShopSettings.shopHeight))
        self.speed = NPCSettings.npcSpeed
        self.items = items
        self.dialog = dialog
        ##### Your Code Here ↑ #####

    def update(self):
        ##### Your Code Here ↓ #####
        if not self.talking and self.talkCD > 0:
            self.talkCD -= 1
        ##### Your Code Here ↑ #####


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, level: int, weak: int, HP=10, Attack=3, Defence=1, Money=15):
        super().__init__()

        ##### Your Code Here ↓ #####
        self.images = [[pygame.transform.scale(pygame.image.load(img),
                                               (NPCSettings.npcWidth,
                                                NPCSettings.npcHeight)) for img in img_list] for img_list in
                       GamePath.monster]
        self.type = randint(0, len(self.images) - 1)
        self.index = 3
        self.image = self.images[self.type][self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = NPCSettings.npcSpeed
        self.direction = 1
        self.action = Action.SITTING
        self.delay = 20
        self.coefficient = (4 / 3) ** (level-1)  # 根据等级决定属性系数
        self.HP = int(HP * self.coefficient * (3 / 4) ** weak)  # 根据玩家削弱等级削弱怪物
        self.attack = int(Attack * self.coefficient * (3 / 4) ** weak)
        self.defence = int(Defence * self.coefficient * (3 / 4) ** weak)
        self.money = int(Money * (16/15)**(level-1))  # 获得金币不受削弱等级影响
        # 根据怪物类型更改属性
        if self.type == 0:
            self.HP = int(self.HP * 3 / 2)
            self.attack = int(self.attack * 2 / 3)
            self.defence = int(self.defence * 3 / 2)
            self.specialEffects = [pygame.transform.scale(pygame.image.load(img),  # 怪物攻击特效加载
                                                          (BattleSettings.specialWidth,
                                                           BattleSettings.specialHeight * 2))
                                   for img in GamePath.specialEffect[1]]
            self.specialEffectIndex = 0
            self.specialEffect = self.specialEffects[self.specialEffectIndex]
            self.sound = pygame.mixer.Sound(GamePath.tornadoSound)

        elif self.type == 1:
            self.HP = int(self.HP * 2 / 3)
            self.attack = int(self.attack * 3 / 2)
            self.defence = int(self.defence * 1 / 2)
            self.specialEffects = [pygame.transform.scale(pygame.image.load(img),
                                                          (BattleSettings.specialWidth, BattleSettings.specialHeight))
                                   for img in GamePath.specialEffect[0]]
            self.specialEffectIndex = 0
            self.specialEffect = self.specialEffects[self.specialEffectIndex]
            self.sound = pygame.mixer.Sound(GamePath.waterSound)

        elif self.type == 2:
            self.HP = int(self.HP * 3 / 2)
            self.attack = int(self.attack * 3 / 2)
            self.defence = int(self.defence)
            self.money *= 4/3
            self.specialEffects = [pygame.transform.scale(pygame.image.load(img),
                                                          (BattleSettings.specialWidth, BattleSettings.specialHeight))
                                   for img in GamePath.specialEffect[2]]
            self.specialEffectIndex = 0
            self.specialEffect = self.specialEffects[self.specialEffectIndex]
            self.sound = pygame.mixer.Sound(GamePath.windSound)

        ##### Your Code Here ↑ #####

    def update(self):
        if self.action == Action.STANDING:  # monster处于起立状态时，播放起立动画
            if self.index > 0:
                self.index -= 1 / 3
        if self.action == Action.DIE:  # monster死亡后触发死亡动画并移除
            if self.index < len(self.images[self.type]) - 1:
                self.index += 1 / 3
            elif self.delay > 0:
                self.delay -= 1
            else:
                self.kill()

        self.image = self.images[self.type][int(self.index)]

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        self.rect = self.rect.move(dx, dy)
        window.blit(self.image, self.rect)
        ##### Your Code Here ↑ #####

    def attacking(self, currentPlayingCount, window):  # 不同怪物不同攻击特效
        if currentPlayingCount == 0:
            pygame.mixer.Sound.play(self.sound)
        if self.type == 0:
            self.specialEffectIndex = (self.specialEffectIndex + 1) % len(self.specialEffects)
            self.specialEffect = self.specialEffects[self.specialEffectIndex]
            window.blit(self.specialEffect,
                        (BattleSettings.monsterCoordX - currentPlayingCount * BattleSettings.stepSize,
                         BattleSettings.monsterCoordY + 50))
        if self.type == 1:
            self.specialEffectIndex = (self.specialEffectIndex + 1) % len(self.specialEffects)
            self.specialEffect = self.specialEffects[self.specialEffectIndex]
            window.blit(self.specialEffect,
                        (BattleSettings.monsterCoordX - currentPlayingCount * BattleSettings.stepSize,
                         BattleSettings.monsterCoordY + 100))
        if self.type == 2:
            self.specialEffectIndex = (self.specialEffectIndex + 0.33) % len(self.specialEffects)
            self.specialEffect = self.specialEffects[int(self.specialEffectIndex)]
            window.blit(self.specialEffect,
                        (BattleSettings.monsterCoordX - currentPlayingCount * BattleSettings.stepSize * 1.2,
                         BattleSettings.monsterCoordY + 100))


class Boss(pygame.sprite.Sprite):
    def __init__(self, x=(WindowSettings.width / 2) + 200, y=WindowSettings.height / 2):
        super().__init__()

        ##### Your Code Here ↓ #####
        self.image = pygame.transform.scale(pygame.image.load(GamePath.boss),
                                            (BossSettings.width,
                                             BossSettings.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.HP = 666
        self.attack = 50
        self.defence = 20
        self.money = 888
        self.nail = pygame.transform.scale(pygame.image.load(GamePath.nail), (117, 40))
        self.sound = pygame.mixer.Sound(GamePath.windSound)
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        self.rect = self.rect.move(dx, dy)
        window.blit(self.image, self.rect)
        ##### Your Code Here ↑ #####

    def attacking(self, currentPlayingCount, window):
        if currentPlayingCount == 0:
            pygame.mixer.Sound.play(self.sound)
        window.blit(self.nail,
                    (BattleSettings.monsterCoordX - currentPlayingCount * BattleSettings.stepSize * 1,
                     BattleSettings.monsterCoordY + 100))
