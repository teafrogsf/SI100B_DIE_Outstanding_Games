# -*- coding:utf-8 -*-

import sys
import pygame

from Player import Player
from Scene import *
from Settings import *
from PopUpBox import *
from Blackjack import Blackjack


class GameManager:
    def __init__(self):

        ##### Your Code Here ↓ #####
        self.window = pygame.display.set_mode((WindowSettings.width,
                                               WindowSettings.height))
        pygame.display.set_caption(WindowSettings.name)
        self.fps = WindowSettings.fps
        self.clock = pygame.time.Clock()
        self.state = GameState.MAIN_MENU
        self.scene = StartMenu(self.window)
        self.player = Player(WindowSettings.width // 2, WindowSettings.height // 2)
        self.bgm = BgmPlayer()
        self.bgm.update()
        self.level = 0  # 怪物强度
        self.time = pygame.time.Clock()
        self.time.tick()  # 通关时间
        self.minusHP = 0  # 用于计算火焰伤害的临时变量
        self.blackjack = Blackjack(self.player, self.window)
        ##### Your Code Here ↑ #####

    def game_reset(self):

        ##### Your Code Here ↓ #####
        self.fps = WindowSettings.fps
        self.clock = pygame.time.Clock()
        self.state = GameState.MAIN_MENU
        self.scene = StartMenu(self.window)
        self.player = Player(WindowSettings.width // 2, WindowSettings.height // 2)
        self.bgm = BgmPlayer()
        self.bgm.update()
        self.level = 0  # 重置怪物等级
        self.time = pygame.time.Clock()
        ##### Your Code Here ↑ #####

    # Necessary game components here ↓
    def tick(self, fps):
        ##### Your Code Here ↓ #####
        self.clock.tick(fps)
        ##### Your Code Here ↑ #####

    def get_time(self):  # 获取游戏时长
        ##### Your Code Here ↓ #####
        self.time.tick()
        time = self.time.get_rawtime() // 1000
        return str(time // 60) + ' min ' + str(time % 60) + ' second'
        ##### Your Code Here ↑ #####

    # Scene-related update functions here ↓
    def flush_scene(self, GOTO: SceneType):
        ##### Your Code Here ↓ #####
        if GOTO == SceneType.CITY:
            self.scene = CityScene(self.window)
            self.state = GameState.GAME_PLAY_CITY
            self.player.reset_pos()
            self.bgm.update(GOTO)
        if GOTO == SceneType.WILD:
            self.scene = WildScene(self.window, self.level, self.player.Weak)
            self.state = GameState.GAME_PLAY_WILD
            self.player.reset_pos()
            # 判断人物重置后是否与生成的障碍物重叠， 如果重叠侧将他们移除
            self.update_collide()
            self.player.reset_scene()
            self.bgm.update(GOTO)
        if GOTO == SceneType.BOSS:
            self.scene = BossScene(self.window)
            self.state = GameState.GAME_PLAY_BOSS
            self.player.reset_pos()
            self.bgm.update(GOTO)
        if GOTO == SceneType.VICTORY:
            self.scene = VictoryMenu(self.window, self.get_time())
            self.state = GameState.GAME_OVER
            self.bgm.update(GOTO)
        if GOTO == SceneType.DEFEAT:
            self.scene = DefeatMenu(self.window, self.get_time())
            self.state = GameState.GAME_OVER
            self.bgm.update(GOTO)


        ##### Your Code Here ↑ #####

    def update(self):
        ##### Your Code Here ↓ #####
        self.tick(self.fps)
        if self.state == GameState.MAIN_MENU:
            self.update_main_menu(pygame.event.get())
        elif self.state == GameState.GAME_PLAY_WILD:
            self.update_wild(pygame.event.get())
        elif self.state == GameState.GAME_PLAY_CITY:
            self.update_city(pygame.event.get())
        elif self.state == GameState.GAME_PLAY_BOSS:
            self.update_boss(pygame.event.get())
        elif self.state == GameState.GAME_OVER:
            self.update_end_menu(pygame.event.get())
        ##### Your Code Here ↑ #####

    def update_main_menu(self, events):
        ##### Your Code Here ↓ #####
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.flush_scene(SceneType.CITY)
                    self.time.tick()
        ##### Your Code Here ↑ #####

    def update_end_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_reset()


    def update_city(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # 开始角色移动
                if event.key == pygame.K_d:
                    self.player.movingEast = True
                if event.key == pygame.K_a:
                    self.player.movingWest = True
                if event.key == pygame.K_w:
                    self.player.movingNorth = True
                if event.key == pygame.K_s:
                    self.player.movingSouth = True

            if event.type == pygame.KEYUP:  # 停止角色移动
                if event.key == pygame.K_d:
                    self.player.movingEast = False
                if event.key == pygame.K_a:
                    self.player.movingWest = False
                if event.key == pygame.K_w:
                    self.player.movingNorth = False
                if event.key == pygame.K_s:
                    self.player.movingSouth = False

            if event.type == GameEvent.EVENT_SWITCH:
                self.flush_scene(SceneType.WILD)
                self.level += 1  # 每次进入野外怪物强度都会提升,第一次进入时为0

            if event.type == GameEvent.EVENT_DIALOG:
                self.scene.trigger_dialog(self.player.collidingObject['npc'])
                self.player.talking = True

            if self.player.talking and event.type == pygame.KEYDOWN:  # 使用ESC退出对话
                if event.key == pygame.K_ESCAPE:
                    self.scene.end_dialog()
                    self.player.talking = False
                    self.player.collidingObject['npc'].reset_talkCD()
                    self.player.collidingWith['npc'] = False
                    self.player.collidingObject['npc'] = []
                elif event.key == pygame.K_RETURN and self.player.Money >= 15:
                    self.scene.end_dialog()
                    self.blackjack = Blackjack(self.player, self.window)
                    self.blackjack.run_game()
                    self.player.talking = False
                    self.player.collidingObject['npc'].reset_talkCD()
                    self.player.collidingWith['npc'] = False
                    self.player.collidingObject['npc'] = []

            if event.type == GameEvent.EVENT_SHOP:
                self.player.collidingObject['npc'].reset_talkCD()
                self.scene.trigger_shop(self.player.collidingObject['npc'], self.player)
                self.player.buying = True

            if self.player.buying and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.scene.shoppingBox.selectedID == 5:
                        self.scene.end_shop()
                        self.player.buying = False
                        self.player.collidingObject['npc'].reset_talkCD()
                        self.player.collidingWith['npc'] = False
                        self.player.collidingObject['npc'] = []
                    elif 1 <= self.scene.shoppingBox.selectedID <= 4:
                        self.scene.shoppingBox.buy()
                    else:
                        print(self.scene.shoppingBox.selectedID)

            if event.type == GameEvent.EVENT_FIRE:
                self.minusHP += 1/30
                self.player.burning = True
            else:
                self.player.burning = False
            if self.minusHP >= 1:   # 临时变量记满1则将生命值减一
                self.player.HP -= 1
                self.minusHP = 0


        ##### Your Code Here ↑ #####

        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        self.player.try_move_width()   # 分别检测横向移动碰撞与纵向移动碰撞
        self.update_collide()          # 以解决障碍物边缘的卡顿问题
        self.player.update(-self.player.dx, 0)
        self.player.try_move_height()
        self.update_collide()
        self.player.update(0, -self.player.dy)
        self.update_NPCs()
        self.scene.update_camera(self.player)
        if self.player.HP <= 0:
            self.flush_scene(SceneType.DEFEAT)
            return                             # 生命值扣完直接失败
        ##### Your Code Here ↑ #####

    def update_wild(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # 开始角色移动
                if event.key == pygame.K_d:
                    self.player.movingEast = True
                if event.key == pygame.K_a:
                    self.player.movingWest = True
                if event.key == pygame.K_w:
                    self.player.movingNorth = True
                if event.key == pygame.K_s:
                    self.player.movingSouth = True

            if event.type == pygame.KEYUP:  # 停止角色移动
                if event.key == pygame.K_d:
                    self.player.movingEast = False
                if event.key == pygame.K_a:
                    self.player.movingWest = False
                if event.key == pygame.K_w:
                    self.player.movingNorth = False
                if event.key == pygame.K_s:
                    self.player.movingSouth = False

            if event.type == GameEvent.EVENT_SWITCH:
                self.flush_scene(self.player.collidingObject['portal'].sceneType)

            if event.type == GameEvent.EVENT_DIALOG:
                self.player.collidingObject['npc'].reset_talkCD()
                self.scene.trigger_dialog(self.player.collidingObject['npc'])
                self.player.talking = True

            if event.type == GameEvent.EVENT_SHOP:
                self.player.collidingObject['npc'].reset_talkCD()
                self.scene.trigger_shop(self.player.collidingObject['npc'])
                self.player.talking = True

            if event.type == GameEvent.EVENT_BATTLE:
                self.scene.trigger_battle(self.player, self.player.collidingObject['monster'])
                self.player.talking = True

            if self.player.talking and event.type == pygame.KEYDOWN:  # 结束战斗，如果player死亡则重新开始游戏
                if self.scene.battleBox.isFinished and event.key == pygame.K_RETURN:
                    if self.player.HP > 0:
                        self.player.attr_update(addCoins=self.player.collidingObject['monster'].money)
                        self.scene.end_battle(self.player.collidingObject['monster'])
                        self.player.talking = False
                    else:
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_END))

            if event.type == GameEvent.EVENT_END:
                self.flush_scene(SceneType.DEFEAT)
                return
            
            if event.type == GameEvent.EVENT_FIRE:
                self.minusHP += 1/30
                self.player.burning = True
            else:
                self.player.burning = False
            if self.minusHP >= 1:   # 临时变量记满1则将生命值减一
                self.player.HP -= 1
                self.minusHP = 0

        ##### Your Code Here ↑ #####

        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        self.player.try_move_width()
        self.update_collide()
        self.player.update(-self.player.dx, 0)
        self.player.try_move_height()
        self.update_collide()
        self.player.update(0, -self.player.dy)
        self.update_NPCs()
        self.scene.update_camera(self.player)
        if self.player.HP <= 0:
            self.flush_scene(SceneType.DEFEAT)
            return
        ##### Your Code Here ↑ #####

    def update_boss(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # 开始角色移动
                if event.key == pygame.K_d:
                    self.player.movingEast = True
                if event.key == pygame.K_a:
                    self.player.movingWest = True
                if event.key == pygame.K_w:
                    self.player.movingNorth = True
                if event.key == pygame.K_s:
                    self.player.movingSouth = True

            if event.type == pygame.KEYUP:  # 停止角色移动
                if event.key == pygame.K_d:
                    self.player.movingEast = False
                if event.key == pygame.K_a:
                    self.player.movingWest = False
                if event.key == pygame.K_w:
                    self.player.movingNorth = False
                if event.key == pygame.K_s:
                    self.player.movingSouth = False

            if event.type == GameEvent.EVENT_DIALOG:
                self.player.collidingObject['npc'].reset_talkCD()
                self.scene.trigger_dialog(self.player.collidingObject['npc'])
                self.player.talking = True

            if event.type == GameEvent.EVENT_SHOP:
                self.player.collidingObject['npc'].reset_talkCD()
                self.scene.trigger_shop(self.player.collidingObject['npc'])
                self.player.talking = True

            if event.type == GameEvent.EVENT_BATTLE:
                self.scene.trigger_battle(self.player, self.player.collidingObject['boss'])
                self.player.talking = True

            if self.player.talking and event.type == pygame.KEYDOWN:
                if self.scene.battleBox.isFinished and event.key == pygame.K_RETURN:
                    if self.player.HP > 0:
                        self.player.attr_update(addCoins=self.player.collidingObject['boss'].money)
                        self.scene.end_battle(self.player.collidingObject['boss'])
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_END))  # 触发游戏结束事件
                    else:
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_END))

            if event.type == GameEvent.EVENT_END:  # 游戏结束并判断结果
                if self.player.HP > 0:
                    self.flush_scene(SceneType.VICTORY)
                    return
                else:
                    self.flush_scene(SceneType.DEFEAT)
                    return
                
            if event.type == GameEvent.EVENT_FIRE:
                self.minusHP += 1/30
            if self.minusHP >= 1:   # 临时变量记满1则将生命值减一
                self.player.HP -= 1
                self.minusHP = 0


        ##### Your Code Here ↑ #####

        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        self.player.try_move_width()
        self.update_collide()
        self.player.update(-self.player.dx, 0)
        self.player.try_move_height()
        self.update_collide()
        self.player.update(0, -self.player.dy)
        self.update_NPCs()
        self.scene.update_camera(self.player)
        if self.player.HP <= 0:
            self.flush_scene(SceneType.DEFEAT)
            return
        ##### Your Code Here ↑ #####

    # Collision-relate update funtions here ↓
    def update_collide(self):
        # Player -> Obstacles
        ##### Your Code Here ↓ #####
        for obstacle in self.scene.obstacles:
            if pygame.sprite.collide_mask(self.player, obstacle):
                self.player.collidingWith['obstacle'] = True
                self.player.collidingObject['obstacle'].append(obstacle)
        ##### Your Code Here ↑ #####

        # Player -> NPCs; if multiple NPCs collided, only first is accepted and dealt with.
        ##### Your Code Here ↓ #####
        for npc in self.scene.npcs:
            if npc.talkCD == 0:
                if pygame.sprite.collide_mask(self.player, npc):
                    self.player.collidingWith['npc'] = True
                    self.player.collidingObject['npc'] = npc
                    if isinstance(npc, ShopNPC):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP))
                    elif isinstance(npc, DialogNPC):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG))
        ##### Your Code Here ↑ #####

        # Player -> Monsters
        ##### Your Code Here ↓ #####
        for monster in self.scene.monsters:
            if pygame.sprite.collide_mask(self.player, monster) and monster.action == Action.SITTING:
                self.player.collidingWith['monster'] = True
                self.player.collidingObject['monster'] = monster
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))
                # 向事件队列发送战斗事件

        ##### Your Code Here ↑ #####

        # Player -> Portals
        ##### Your Code Here ↓ #####
        for portal in self.scene.portals:
            if pygame.sprite.collide_mask(self.player, portal):
                self.player.collidingWith['portal'] = True
                self.player.collidingObject['portal'] = portal
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH))
                # 向事件队列发送传送事件

        ##### Your Code Here ↑ #####

        # Player -> Boss
        ##### Your Code Here ↓ #####
        for boss in self.scene.bosses:
            if pygame.sprite.collide_mask(self.player, boss) and not self.player.talking:
                self.player.collidingWith['boss'] = True
                self.player.collidingObject['boss'] = boss
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))
        ##### Your Code Here ↑ #####
                
        # Player -> Fire
        for fire in self.scene.fires:
            if pygame.sprite.collide_mask(self.player, fire):
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_FIRE))

    def update_NPCs(self):
        # This is not necessary. If you want to re-use your code you can realize this.
        ##### Your Code Here ↓ #####
        for npc in self.scene.npcs:
            npc.update()
        ##### Your Code Here ↑ #####

    # Render-relate update functions here ↓
    def render(self):
        ##### Your Code Here ↓ #####
        if self.state == GameState.MAIN_MENU:
            self.render_main_menu()
        elif self.state == GameState.GAME_PLAY_WILD:
            self.render_wild()
        elif self.state == GameState.GAME_PLAY_CITY:
            self.render_city()
        elif self.state == GameState.GAME_PLAY_BOSS:
            self.render_boss()
        elif self.state == GameState.GAME_OVER:
            self.render_end_menu()
        ##### Your Code Here ↑ #####

    def render_main_menu(self):
        ##### Your Code Here ↓ #####
        self.scene.render(ManuSettings.blinkInterval)
        ##### Your Code Here ↑ #####

    def render_end_menu(self):
        self.scene.render(ManuSettings.blinkInterval)
    def render_city(self):
        ##### Your Code Here ↓ #####
        self.scene.render(self.player)
        ##### Your Code Here ↑ #####

    def render_wild(self):
        ##### Your Code Here ↓ #####
        self.scene.render(self.player)
        ##### Your Code Here ↑ #####

    def render_boss(self):
        ##### Your Code Here ↓ #####
        self.scene.render(self.player)
        ##### Your Code Here ↑ #####
