# -*- coding:utf-8 -*-
import random

import pygame

from typing import *
from Settings import *
from Tile import *
from random import randint, random


class DialogBox:
    def __init__(self, window, npc, dialog,
                 fontSize: int = DialogSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255),
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        ##### Your Code Here ↓ #####
        self.window = window

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)
        self.hint = pygame.font.Font(None, ManuSettings.textSize)  # 退出提示
        self.text = self.hint.render('Press ESC to exit                   Press ENTER to play', True,
                                     (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2,
                                                   WindowSettings.height - 20))
        self.bg = pygame.Surface((DialogSettings.boxWidth, DialogSettings.boxHeight),
                                 pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.dialog = dialog

        self.npc = pygame.transform.scale(npc.image, (DialogSettings.npcWidth,
                                                      DialogSettings.npcHeight))
        ##### Your Code Here ↑ #####

    def draw(self):
        ##### Your Code Here ↓ #####
        self.window.blit(self.bg, (DialogSettings.boxStartX, DialogSettings.boxStartY))
        self.window.blit(self.npc, (DialogSettings.npcCoordX, DialogSettings.npcCoordY))
        self.window.blit(self.text, self.textRect)  # 绘制退出提示
        offset = 0
        for text in self.dialog:
            self.window.blit(self.font.render(text, True, self.fontColor),
                             (DialogSettings.textStartX, DialogSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        ##### Your Code Here ↑ #####


class BattleBox:
    def __init__(self, window, player, monster, fontSize: int = BattleSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255),
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 200)):
        ##### Your Code Here ↓ #####

        self.window = window

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.bg = pygame.image.load(GamePath.battleBox)
        self.bg = pygame.transform.scale(self.bg, (BattleSettings.boxWidth, BattleSettings.boxHeight))

        self.HPImage = pygame.transform.scale(pygame.image.load(GamePath.player_HP), (PlayerSettings.heartWidth,
                                                                                      PlayerSettings.heartHeight))
        self.moneyImage = pygame.transform.scale(pygame.image.load(GamePath.player_Money),
                                                 (PlayerSettings.heartWidth, PlayerSettings.heartHeight))

        # 初始化相关角色的参数，没有实际操作的权力
        self.player = player
        self.playerImg = self.player.images[PlayerDirection.Right.value][0]
        self.playerImg = pygame.transform.scale(self.playerImg,
                                                (BattleSettings.playerWidth, BattleSettings.playerHeight))

        self.playerX = BattleSettings.playerCoordX
        self.playerY = BattleSettings.playerCoordY

        self.monster = monster
        try:
            self.monsterImg = monster.images[monster.type][0]
        except:
            self.monsterImg = monster.image
        self.monsterImg = pygame.transform.scale(self.monsterImg,
                                                 (BattleSettings.monsterWidth, BattleSettings.monsterHeight))
        self.monsterImg = pygame.transform.flip(self.monsterImg, True, False)

        self.monsterX = BattleSettings.monsterCoordX
        self.monsterY = BattleSettings.monsterCoordY
        # 默认玩家先手
        self.attacker = 0
        # 区分放动画状态和攻击结算状态
        self.isPlayingAnimation = True
        self.currentPlayingCount = 0
        # 移动方向
        self.dir = 1
        # 是否结束
        self.isFinished = False
        self.hint = pygame.font.Font(None, ManuSettings.textSize)  # 退出提示
        self.text = self.hint.render('Press ENTER to exit', True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2,
                                                   WindowSettings.height // 2 + 50))
        ##### Your Code Here ↑ #####

    def get_result(self):
        if self.attacker == 0:  # 人物或者怪物使用攻击特效
            self.monster.HP = max(0, self.monster.HP -
                                  max(1, (self.player.Attack - self.monster.defence)))
            self.attacker = 1
            self.dir = -1
        else:
            self.player.HP = max(0, self.player.HP -
                                 max(1, (self.monster.attack - self.player.Defence)))
            self.attacker = 0
            self.dir = 1

        self.isPlayingAnimation = True

    def draw(self):
        ##### Your Code Here ↓ #####
        # 绘制背景和文字
        self.window.blit(self.bg, (BattleSettings.boxStartX, BattleSettings.boxStartY))
        self.window.blit(self.playerImg, (self.playerX, self.playerY))
        self.window.blit(self.monsterImg, (BattleSettings.monsterCoordX, self.monsterY))
        text = '×' + str(self.player.HP)
        self.window.blit(self.HPImage, (BattleSettings.boxStartX + 30, BattleSettings.boxStartY + 20))
        self.window.blit(self.font.render(text, True, self.fontColor),
                         (BattleSettings.textPlayerStartX, BattleSettings.textStartY))

        text = str(self.monster.HP) + '×'
        self.window.blit(self.HPImage, (BattleSettings.textMonsterStartX + 55, BattleSettings.boxStartY + 20))
        self.window.blit(self.font.render(text, True, self.fontColor),
                         (BattleSettings.textMonsterStartX, BattleSettings.textStartY))
        # 绘制战斗过程
        if self.isPlayingAnimation:
            if self.attacker == 0:
                if 10 <= self.currentPlayingCount <= 20:
                    self.player.attacking(self.currentPlayingCount, self.window)
            else:
                self.monster.attacking(self.currentPlayingCount, self.window)

            self.currentPlayingCount += 1

            if self.currentPlayingCount == BattleSettings.animationFrameCount * 2:
                self.isPlayingAnimation = False
                self.currentPlayingCount = 0

        # 战斗判定以及结算
        elif not self.isFinished:
            self.get_result()

        if self.player.HP == 0 or self.monster.HP == 0:
            if self.monster.HP == 0:
                text = '+ ' + str(self.monster.money)
                self.window.blit(self.moneyImage, (BattleSettings.boxStartX + BattleSettings.boxWidth // 2 - 50,
                                                   BattleSettings.textStartY - 8))
                self.window.blit(self.text, self.textRect)  # 绘制退出提示
            elif self.player.HP == 0:
                text = 'YOU DIED'
            self.window.blit(self.font.render(text, True, self.fontColor),
                             (BattleSettings.boxStartX + BattleSettings.boxWidth // 2,
                              BattleSettings.textStartY))

            self.isFinished = True
            self.isPlayingAnimation = False
        # 战斗结束

        ##### Your Code Here ↑ #####


class ShoppingBox:
    def __init__(self, window, npc, player,
                 fontSize: int = DialogSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255),
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        ##### Your Code Here ↓ #####
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)
        self.bg = pygame.image.load(GamePath.shopBackground)
        self.bg = pygame.transform.scale(self.bg, (ShopSettings.boxWidth, ShopSettings.boxHeight))
        self.npc = npc
        self.npc_image = pygame.transform.scale(pygame.image.load(GamePath.shopNpc), (DialogSettings.npcWidth,
                                                                                      DialogSettings.npcHeight))

        self.player = player

        self.selectedID = 0
        self.items = pygame.sprite.Group()
        self.items.add(ShopAttack())
        self.items.add(ShopDefence())
        self.items.add(ShopHP())
        self.items.add(ShopLevel())
        self.exit = ShopExit()
        self.mouse = Mouse()
        ##### Your Code Here ↑ #####

    def buy(self):
        ##### Your Code Here ↓ #####
        if self.selectedID == 1:
            self.player.attr_update(addCoins=-15, addAttack=1)
        elif self.selectedID == 2:
            self.player.attr_update(addCoins=-15, addDefence=1)
        elif self.selectedID == 3:
            self.player.attr_update(addCoins=-15, addHP=3)
        elif self.selectedID == 4:
            self.player.attr_update(addHP=-3, addWeak=1)
        ##### Your Code Here ↑ #####

    def draw(self):
        ##### Your Code Here ↓ #####
        self.update()
        self.window.blit(self.bg, (ShopSettings.boxStartX, ShopSettings.boxStartY))
        self.window.blit(self.npc_image, (DialogSettings.npcCoordX, DialogSettings.npcCoordY))

        for item in self.items:
            self.window.blit(item.image, item.rect)
        self.window.blit(self.exit.image, self.exit.rect)
        self.mouse.update(self.window)
        ##### Your Code Here ↑ #####

    def update(self):
        self.blank = True  # 判断鼠标是否在空白处
        for item in self.items:
            if pygame.sprite.collide_mask(item, self.mouse):  # 鼠标碰到的物品图标变化
                self.selectedID = item.ID
                item.image = pygame.transform.scale(item.image, (100, 130))
                self.blank = False
            else:  # 恢复正常大小
                item.image = pygame.transform.scale(item.image, (ShopSettings.itemWidth, ShopSettings.itemHeight))
        if pygame.sprite.collide_mask(self.exit, self.mouse):
            self.selectedID = self.exit.ID
            self.exit.image = pygame.transform.scale(self.exit.image, (90, 50))
            self.blank = False
        else:
            self.exit.image = pygame.transform.scale(self.exit.image, (80, 40))
        if self.blank:  # 鼠标在空白处则物品ID为0
            self.selectedID = 0
