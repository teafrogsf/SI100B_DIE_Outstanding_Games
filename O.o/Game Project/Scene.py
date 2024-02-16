# -*- coding:utf-8 -*-

import pygame
from random import randint, random

from Settings import *
from NPCs import *
from PopUpBox import *
from Portal import *
from BgmPlayer import *
from Tile import *


class Scene:
    def __init__(self, window):
        ##### Your Code Here ↓ #####
        self.window = window
        self.map = pygame.sprite.Group()
        self.sceneType = None

        self.width, self.height = (int(WindowSettings.width * WindowSettings.outdoorScale),
                                   int(WindowSettings.height * WindowSettings.outdoorScale))
        self.dx, self.dy = 0, 0
        self.cameraX, self.cameraY = 0, 0

        self.obstacles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.dialogBox = None
        self.shoppingBox = None
        self.battleBox = None
        
        ##### Your Code Here ↑ #####

    def trigger_dialog(self, npc: DialogNPC):
        ##### Your Code Here ↓ #####
        npc.talking = True
        self.dialogBox = DialogBox(self.window, npc, npc.dialog)
        ##### Your Code Here ↑ #####

    def end_dialog(self):
        ##### Your Code Here ↓ #####
        self.dialogBox = None
        ##### Your Code Here ↑ #####

    def trigger_battle(self, player, monster):
        ##### Your Code Here ↓ #####
        monster.action = Action.STANDING
        self.battleBox = BattleBox(self.window, player, monster)
        ##### Your Code Here ↑ #####

    def end_battle(self, monster):
        ##### Your Code Here ↓ #####
        self.battleBox = None
        try:
            monster.action = Action.DIE
        except:
            monster.kill()
        ##### Your Code Here ↑ #####

    def trigger_shop(self, npc, player):
        ##### Your Code Here ↓ #####
        self.shoppingBox = ShoppingBox(self.window, npc, player)
        npc.talking = True
        ##### Your Code Here ↑ #####

    def end_shop(self):
        ##### Your Code Here ↓ #####
        self.shoppingBox = None
        pygame.mouse.set_visible(1)
        ##### Your Code Here ↑ #####

    def update_camera(self, player):
        ##### Your Code Here ↓ #####
        self.dx, self.dy = 0, 0
        if player.rect.x > WindowSettings.width / 4 * 3:
            self.cameraX += player.speed
            if self.cameraX < self.width - WindowSettings.width:
                self.dx = - player.speed
            else:
                self.cameraX = self.width - WindowSettings.width
                self.dx = 0
        elif player.rect.x < WindowSettings.width / 4:
            self.cameraX -= player.speed
            if self.cameraX > 0:
                self.dx = player.speed
            else:
                self.cameraX = 0
                self.dx = 0
        if player.rect.y > WindowSettings.height / 4 * 3:
            self.cameraY += player.speed
            if self.cameraY < self.height - WindowSettings.height:
                self.dy = - player.speed
            else:
                self.cameraY = self.height - WindowSettings.height
                self.dy = 0
        elif player.rect.y < WindowSettings.height / 4:
            self.cameraY -= player.speed
            if self.cameraY > 0:
                self.dy = player.speed
            else:
                self.cameraY = 0
                self.dy = 0
        
        ##### Your Code Here ↑ #####

    def render(self, player):
        ##### Your Code Here ↓ #####
        for pixel in self.map:
            pixel.draw(self.window, self.dx,
                       self.dy)
        for obstacle in self.obstacles:
            obstacle.draw(self.window, self.dx,
                          self.dy)
        for fire in self.fires:
            fire.draw(self.window, self.dx,
                      self.dy)
        for portal in self.portals:
            portal.draw(self.window, self.dx,
                        self.dy)
        for monster in self.monsters:
            monster.update()
            monster.draw(self.window, self.dx,
                         self.dy)
        for npc in self.npcs:
            npc.update()
            npc.draw(self.window, self.dx,
                     self.dy)
        for boss in self.bosses:
            boss.draw(self.window, self.dx,
                      self.dy)
        player.draw(self.window, self.dx,
                    self.dy)
        player.state_update(self.window)
        if self.dialogBox:
            self.dialogBox.draw()
        if self.shoppingBox:
            self.shoppingBox.draw()
        if self.battleBox:
            self.battleBox.draw()

        ##### Your Code Here ↑ #####


class StartMenu():
    def __init__(self, window):
        ##### Your Code Here ↓ #####
        self.bg = pygame.image.load(GamePath.menu)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width,
                                                   WindowSettings.height))
        self.window = window
        self.font = pygame.font.Font(None, ManuSettings.textSize)
        self.text = self.font.render('Press ENTER to start', True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2,
                                                   WindowSettings.height - 50))
        self.blinkTimer = 0

        ##### Your Code Here ↑ #####

    def render(self, time):
        ##### Your Code Here ↓ #####
        self.window.blit(self.bg, (0, 0))

        self.blinkTimer += 1
        if self.blinkTimer < time:
            self.window.blit(self.text, self.textRect)
        elif self.blinkTimer == time * 2:
            self.blinkTimer = 0

        ##### Your Code Here ↑ #####


class CityScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.gen_CITY()
        self.sceneType = SceneType.CITY
        self.window = window

    def gen_city_map(self):
        ##### Your Code Here ↓ #####
        images = [pygame.image.load(tile) for tile in GamePath.cityTiles]

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.map.add(Tile(images[randint(0, len(images) - 1)], i * SceneSettings.tileWidth,
                                  j * SceneSettings.tileHeight))
        self.fires.add(Tree([pygame.image.load(img) for img in GamePath.fire], 8 * SceneSettings.tileWidth, 
                         12 * SceneSettings.tileHeight, 2*SceneSettings.tileWidth, 2*SceneSettings.tileHeight))
        
        ##### Your Code Here ↑ #####

    def gen_city_obstacle(self):
        ##### Your Code Here ↓ #####
        image = pygame.image.load(GamePath.cityWall)

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                if i == 0 or i == SceneSettings.tileXnum - 1 \
                        or j == 0 or j == SceneSettings.tileYnum - 1:
                    self.obstacles.add(Tile(image, i * SceneSettings.tileWidth,
                                            j * SceneSettings.tileHeight))
        tree = [[pygame.image.load(img) for img in images] for images in GamePath.animated_tree]
        self.obstacles.add(Tree(tree[0], 11 * SceneSettings.tileWidth, 6 * SceneSettings.tileHeight))
        self.obstacles.add(Tree(tree[1], 11 * SceneSettings.tileWidth, 5 * SceneSettings.tileHeight))
        self.obstacles.add(Tree(tree[2], 12 * SceneSettings.tileWidth, 6 * SceneSettings.tileHeight))
        self.obstacles.add(Tree(tree[3], 12 * SceneSettings.tileWidth, 5 * SceneSettings.tileHeight))

        ##### Your Code Here ↑ #####

    def gen_CITY(self):

        ##### Your Code Here ↓ #####
        self.gen_city_map()
        self.gen_city_obstacle()
        self.portals.add(Portal(PortalSettings.coordX,
                                PortalSettings.coordY, self.sceneType))
        self.npcs.add(DialogNPC(self.width // 5, self.height // 5, 'YTG', ['Welcome Back, My Hero.',
                                                                           'Would you like to play Blackjack ?',
                                                                           'You need to have at least 15 coins to play!']))
        self.npcs.add(ShopNPC(self.width // 3 * 2, self.height // 3 * 2, 'ZZY',
                              {'Attack +1': 'Coin -15', 'Defence +1': 'Coin -15',
                               'HP +3': 'Coin -15', '???': 'HP -5', 'Exit': ''}, {}))
        ##### Your Code Here ↑ #####


class WildScene(Scene):
    def __init__(self, window, level: int, weak: int):
        super().__init__(window=window)

        ##### Your Code Here ↓ #####
        self.gen_WILD(level, weak)
        self.sceneType = SceneType.WILD
        self.window = window

        ##### Your Code Here ↑ #####

    def gen_wild_map(self):

        ##### Your Code Here ↓ #####
        images = [pygame.image.load(tile) for tile in GamePath.groundTiles]

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.map.add(Tile(images[randint(0, len(images) - 1)], i * SceneSettings.tileWidth,
                                  j * SceneSettings.tileHeight))
        ##### Your Code Here ↑ #####

    def gen_wild_obstacle(self):

        ##### Your Code Here ↓ #####
        image = pygame.image.load(GamePath.tree)

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                if random() < 0.9*SceneSettings.obstacleDensity:
                    self.obstacles.add(Tile(image, i * SceneSettings.tileWidth,
                                            j * SceneSettings.tileHeight))
                elif random() < 0.1*SceneSettings.obstacleDensity:
                    self.fires.add(Tree([pygame.image.load(img) for img in GamePath.fire],
                                         i * SceneSettings.tileWidth, 
                                         j * SceneSettings.tileHeight))
        ##### Your Code Here ↑ #####

    def gen_WILD(self, level: int, weak: int):

        ##### Your Code Here ↓ #####
        self.gen_wild_map()
        self.gen_wild_obstacle()
        self.gen_portals()
        self.gen_monsters(level, weak)
        ##### Your Code Here ↑ #####

    def gen_monsters(self, level: int, weak: int, num=10):

        ##### Your Code Here ↓ #####
        idx = 0
        while idx < num:
            monster = Monster(randint(0, self.width), randint(0, self.height),
                              level, weak)
            # 判断monster不与已经生成的物品重合
            if not pygame.sprite.spritecollide(monster, self.obstacles, False) \
                    and not pygame.sprite.spritecollide(monster, self.monsters, False) \
                    and not pygame.sprite.spritecollide(monster, self.portals, False) \
                    and not pygame.sprite.spritecollide(monster, self.fires, False) \
                    and abs(monster.rect.x - WindowSettings.width // 2) > 3 \
                    and abs(monster.rect.y - WindowSettings.height // 2) > 3:  # 确保不会在人物周围三格生成
                self.monsters.add(monster)
                idx += 1
        ##### Your Code Here ↑ #####

    def gen_portals(self):
        portalToCity = Portal(PortalSettings.coordX - PortalSettings.width * 4,
                              PortalSettings.coordY - PortalSettings.height,
                              SceneType.CITY)
        portalToBoss = Portal(PortalSettings.coordX,
                              PortalSettings.coordY,
                              SceneType.BOSS)
        self.portals.add(portalToCity, portalToBoss)
        # 将与传送门重合的障碍物移除
        for portal in self.portals:
            while pygame.sprite.spritecollideany(portal, self.obstacles):
                pygame.sprite.spritecollideany(portal, self.obstacles).kill()
            while pygame.sprite.spritecollideany(portal, self.fires):
                pygame.sprite.spritecollideany(portal, self.fires).kill()


class BossScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.gen_BOSS()
        self.sceneType = SceneType.BOSS
        self.window = window

    # Overwrite Scene's function
    def trigger_battle(self, player, boss):
        ##### Your Code Here ↓ #####
        self.battleBox = BattleBox(self.window, player, boss)
        ##### Your Code Here ↑ #####

    def gen_boss_obstacle(self):
        ##### Your Code Here ↓ #####
        image = pygame.image.load(GamePath.bossWall)

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                if i == 0 or i == SceneSettings.tileXnum - 1 \
                        or j == 0 or j == SceneSettings.tileYnum - 1:
                    self.obstacles.add(Tile(image, i * SceneSettings.tileWidth,
                                            j * SceneSettings.tileHeight))
        ##### Your Code Here ↑ #####

    def gen_boss_map(self):
        ##### Your Code Here ↓ #####
        images = [pygame.image.load(tile) for tile in GamePath.bossTiles]

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.map.add(Tile(images[randint(0, len(images) - 1)], i * SceneSettings.tileWidth,
                                  j * SceneSettings.tileHeight))
        ##### Your Code Here ↑ #####

    def gen_BOSS(self):
        ##### Your Code Here ↓ #####
        self.gen_boss_map()
        self.gen_boss_obstacle()
        self.bosses.add(Boss())
        ##### Your Code Here ↑ #####


class EndMenu():
    def __init__(self, window, time):
        self.bg = None
        self.window = window
        self.font = pygame.font.Font(None, ManuSettings.textSize)
        self.text = self.font.render('PRESS ENTER TO RESTART', True, (0, 0, 0))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2,
                                                   WindowSettings.height - 50))
        self.blinkTimer = 0
        self.time = time
        self.data = self.font.render('GAME TIME: ' + self.time, True, (0, 0, 0))  # 显示游戏时长
        self.dataRect = self.data.get_rect(center=(WindowSettings.width // 2 + 150,
                                                   WindowSettings.height // 2 + 50))
        self.image = None
        self.imageRect = None

    def render(self, time):
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.data, self.dataRect)
        self.window.blit(self.image, self.imageRect)
        self.blinkTimer += 1
        if self.blinkTimer < time:
            self.window.blit(self.text, self.textRect)
        elif self.blinkTimer == time * 2:
            self.blinkTimer = 0


class VictoryMenu(EndMenu):
    def __init__(self, window, time):
        super().__init__(window, time)
        self.bg = pygame.image.load(GamePath.victory_menu)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width,
                                                   WindowSettings.height))
        self.image = pygame.image.load(GamePath.player_win)
        self.image = pygame.transform.scale(self.image, (DialogSettings.npcWidth, DialogSettings.npcHeight))
        self.imageRect = self.image.get_rect(center=(WindowSettings.width // 2 - 200,
                                                     WindowSettings.height // 2))


class DefeatMenu(EndMenu):
    def __init__(self, window, time):
        super().__init__(window, time)
        self.bg = pygame.image.load(GamePath.defeat_menu)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width,
                                                   WindowSettings.height))
        self.image = pygame.image.load(GamePath.player_died)
        self.image = pygame.transform.scale(self.image, (DialogSettings.npcWidth, DialogSettings.npcHeight))
        self.imageRect = self.image.get_rect(center=(WindowSettings.width // 2 - 300,
                                                     WindowSettings.height // 2))
