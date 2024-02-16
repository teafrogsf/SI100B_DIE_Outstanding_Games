'''
EVENT 进入游戏
EVENT 退出游戏
EVENT 按键
EVENT 场景切换
EVENT 碰撞检测
EVENT 游戏结束
......
def event检测
'''
import Box
import pygame
import sys
import pygame
from Setting import GameState

class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_SHOP = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SWITCH = pygame.USEREVENT + 5 # Event: Switch between scenes
    EVENT_VALUECALLCULATE = pygame.USEREVENT + 6
    EVENT_DIED = pygame.USEREVENT + 7
    EVENT_WIN = pygame.USEREVENT + 8

class EventChecker:
    def event_checker(self, scene, manager):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == GameEvent.EVENT_RESTART:
                manager.needRestart = True
            if event.type == GameEvent.EVENT_SWITCH:
                manager.flush_scene(event.target)
            if event.type == GameEvent.EVENT_VALUECALLCULATE:
                manager.value_settler(event.value)
            if event.type == GameEvent.EVENT_BATTLE:
                if scene.box == None:
                    scene.box = Box.BattleBox(manager.window, manager.player, event.enemy)
                    manager.player.talking = True
            if event.type == GameEvent.EVENT_DIALOG:
                if event.dialogType == 'Dialog_GuideBox' and scene.box == None:
                    scene.box = Box.Dialog_GuideBox(manager.window, event.dialogNPC)
                    manager.player.talking = True
            if event.type == GameEvent.EVENT_SHOP:
                if event.shopType == 'Shop_HomeBox' and scene.box == None:
                    scene.box = Box.Shop_HomeBox(manager.window, manager.player)
                    manager.player.talking = True
                if event.shopType == 'Shop_KFCBox' and scene.box == None:
                    scene.box = Box.Shop_KFCBox(manager.window, manager.player)
                    manager.player.talking = True
            if event.type == pygame.KEYDOWN:
                manager.keyDown = event.key
            if event.type == GameEvent.EVENT_WIN:
                manager.state = GameState.GAME_WIN
                manager.flush_scene(None)
            if event.type == GameEvent.EVENT_DIED:
                manager.state = GameState.GAME_OVER
                manager.flush_scene(None)
