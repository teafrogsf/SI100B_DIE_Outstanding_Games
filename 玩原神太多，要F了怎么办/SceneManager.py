# -*- coding:utf-8 -*-

import pygame
import sys
import copy

from Scene import *
import GameLogic
import Player
from Design import *


class SceneManager:
    def __init__(self, window, user) -> None:
        self.window = window
        self.user = user
        self.nowScene = Scene(self.window)
        self.cameraX = 0
        self.cameraY = 0
        self.touchBoard = False
        self.touchShop = False
        self.touchEnemy = False
        self.board = Scene(self.window)

    def gen_map(self, areaID):
        self.nowScene = MainMap(self.window, areaID, self.player)
        self.cameraX = 0  # CameraInitialTopLeft.map[areaID][0][0]
        self.cameraY = 0  # CameraInitialTopLeft.map[areaID][0][1]

    def gen_player(self):
        self.player = Player.Player(self.window, self.user)

    def update_camera(self):
        if WindowSettings.width // 2 < self.player.rect.x < MapSettings.width - WindowSettings.width // 2:
            self.cameraX = self.player.rect.x - WindowSettings.width // 2
        elif self.player.rect.x <= WindowSettings.width // 2:
            self.cameraX = 0
        else:
            self.cameraX = MapSettings.width - WindowSettings.width
        if WindowSettings.height // 2 < self.player.rect.top < MapSettings.height - WindowSettings.height // 2:
            self.cameraY = self.player.rect.top - WindowSettings.height // 2
        elif self.player.rect.top <= WindowSettings.height // 2:
            self.cameraY = 0
        else:
            self.cameraY = MapSettings.height - WindowSettings.height

    def execute(self, cmd):
        if len(cmd) == 1:
            if cmd[0] == "exit":
                pygame.quit()
                sys.exit()
        if len(cmd) == 2:
            if cmd[0] == "cheat":
                def is_int(s):
                    try:
                        int(s)
                        return True
                    except ValueError:
                        return False
                if is_int(cmd[1]):
                    self.player = GameLogic.ExeMoney(
                        int(cmd[1]), ifChange=True).exe(self.player)
            if cmd[0] == "tp":
                entry = cmd[1]
                if entry in self.player.info.get_info("anchor") and BoardDetail.map[entry]["type"] == "Anchor":
                    to_area = BoardDetail.map[entry]["area"]
                    self.player = GameLogic.ExeTP(
                        BoardDetail.map[entry]["x"], BoardDetail.map[entry]["y"], area=to_area).exe(self.player)
                    self.player.info.modify("enemy", [])
                    self.player.save()
                    self.gen_map(to_area)
            if cmd[0] == "map":
                entry = cmd[1]

                def is_int(s):
                    try:
                        int(s)
                        return True
                    except ValueError:
                        return False
                if is_int(cmd[1]):
                    to_area = int(cmd[1])
                    if to_area in self.player.info.get_info("map"):
                        self.player = GameLogic.ExeTP(BirthInfo.point[to_area][0], BirthInfo.point[to_area][1],
                                                      dir=BirthInfo.direction[to_area], area=to_area).exe(self.player)
                        self.player.info.modify("enemy", [])
                        self.player.save()
                        self.gen_map(to_area)

    def tap(self, event):
        playerState = self.player.info.get_info("state")
        # test
        # print(playerState)
        if playerState == 0 and (event.key == pygame.K_TAB or event.key == pygame.K_b):
            self.player.info.modify("state", 4)
            self.menu = Menu(self.window)
        elif playerState in [0, 1]:
            if event.key == pygame.K_BACKQUOTE:
                if playerState == 0:
                    self.player.info.modify("state", 1)
                    self.command = Command(self.window)
                elif playerState == 1:
                    self.player.info.modify("state", 0)
            elif playerState == 1:
                word = self.command.tap(event)
                if len(word) != 0:
                    self.execute(word)
                    self.player.save()
            elif self.touchBoard and event.key == pygame.K_RETURN:
                self.player.info.modify("state", 2)
                self.board.enter(self.player)
            elif self.touchShop and event.key == pygame.K_RETURN:
                self.player.info.modify("state", 5)
                self.shop.state = 1
            elif self.touchEnemy:
                self.player.info.modify("state", 3)
                self.enemy.enter(self.player)
        elif playerState == 2:
            self.player = self.board.tap(event, self.player, self.gen_map)
        elif playerState == 4:
            self.player = self.menu.tap(event, self.player)
        elif playerState == 5:
            self.player = self.shop.tap(event, self.player)
        elif playerState == 3:
            self.player = self.enemy.tap(event, self.player, self.gen_map)

    def update(self, keys, events):
        if self.player.info.get_info("state") == 0:
            zipPlayer = self.player.zip()
            self.player.update(keys)
            ifCollide, collideType, collideList, meetObstacle = GameLogic.collidate(
                self.player, self.nowScene.items)
            self.touchBoard = "Board" in collideType or "Bell" in collideType
            self.touchShop = "Shop" in collideType
            self.touchEnemy = "Enemy" in collideType
            if meetObstacle == True:
                self.player.unzip(zipPlayer)
            # test
            # print(collideType)
            if "Board" in collideType:  # self.touchBoard:
                for boardID in collideList["Board"]:
                    # self.player.info.modify("state", 2)
                    if BoardDetail.map[boardID]["type"] == "Dialogue":
                        self.board = Dialogue(self.window, boardID)
                    if BoardDetail.map[boardID]["type"] == "Shopping":
                        self.board = Shopping(self.window, boardID)
                    if BoardDetail.map[boardID]["type"] == "Treasure":
                        self.board = Treasure(self.window, boardID)
                    if BoardDetail.map[boardID]["type"] == "Anchor":
                        self.board = Anchor(self.window, boardID)
                    pass                                                    # 其他的board种类
                self.board.render()
            elif "Bell" in collideType:
                for bellID in collideList["Bell"]:
                    self.board = BellDialogue(self.window, bellID)
                self.board.render()
            elif "Shop" in collideType:
                for shopID in collideList["Shop"]:
                    self.shop = ShoppingMenu(self.window, shopID)
                self.shop.render(self.player)
            elif "Enemy" in collideType:
                for enemyID in collideList["Enemy"]:
                    self.enemy = EnemyDialogue(self.window, enemyID)
            self.player.save()
            self.update_camera()
        elif self.player.info.get_info("state") == 3:
            self.enemy.update(events)

    def move_with_camera(self, xy):
        return (xy[0] - self.cameraX, xy[1] - self.cameraY)

    def draw_layer(self, drawList):
        rowNum = []
        for item in drawList:
            rowNum.append(item.rect.top)
        rowNum = sorted(set(rowNum))

        rowList = {}
        for item in drawList:
            if item.rect.top in rowList:
                rowList[item.rect.top].append(item)
            else:
                rowList[item.rect.top] = [item]

        for row in rowNum:
            for item in rowList[row]:
                self.window.blit(
                    item.image, self.move_with_camera(item.topleft()))

    def render(self):
        # 相机归位
        self.update_camera()

        # 绘制三个图层
        drawLayer = self.nowScene.render()
        drawLayer[1].append(self.player)
        for drawList in drawLayer:
            self.draw_layer(drawList)

        # 渲染command
        if self.player.info.get_info("state") == 1:
            self.command.render()

        # Board
        if self.touchBoard:
            self.board.render()

        # Shop
        if self.touchShop:
            self.shop.render(self.player)

        # Enemy
        if self.touchEnemy:
            self.enemy.render()

        # 渲染菜单
        if self.player.info.get_info("state") == 4:
            self.menu.render(self.player)
