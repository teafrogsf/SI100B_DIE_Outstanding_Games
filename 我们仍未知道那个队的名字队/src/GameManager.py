# -*- coding:utf-8 -*-

import pygame
from Player import Player
from Enemy import *
from Scene import *
from Setting import *
from Event import EventChecker
from Menu import Menu
from BGMPlayer import BGMPlayer
from Ending import GameOverScene, GameWinScene
from Weapon import Weapon
from Skill import Skill

class GameManager:
    def __init__(self):
        self.window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height),pygame.HWSURFACE|pygame.DOUBLEBUF)
        pygame.display.set_caption(WindowSettings.title)
        self.clock = pygame.time.Clock()
        self.player = Player() # 初始化玩家
        self.playerInfoDisplayer = self.PlayerInfoDisplay()
        self.scene = Menu()
        self.sceneDic = {'Home':Home_Scene(self.window, self.player),'School':School_Scene(self.window, self.player), 'SLST':SLST_Scene(self.window, self.player),'SPST':SPST_Scene(self.window, self.player),'SIST':SIST_Scene(self.window, self.player),'Underground':Underground_Scene(self.window, self.player), 'KFC':KFC_Scene(self.window,self.player), 'Universe':Universe_Scene(self.window, self.player)}
        self.state = GameState.MAIN_MENU
        self.keys = None
        self.keyDown = None
        self.eventChecker = EventChecker()
        # BGM
        self.BGMPlayer = BGMPlayer(self.scene.BGM)
        self.BGMPlayer.play()
        self.needRestart = False
    def flush_scene(self, target):
        if self.state == GameState.GAME_PLAY or self.state == GameState.MAIN_MENU:
            self.BGMPlayer.stop()
            self.scene = self.sceneDic[f'{target}']
            self.BGMPlayer = BGMPlayer(self.scene.BGM)
            self.BGMPlayer.play()
            self.state = GameState.GAME_PLAY
            self.player.rect.center = self.scene.playerPos

            if  target == 'Universe':
                self.player.canOnlyMoveInY = True
            else:
                self.player.canOnlyMoveInY = False

        elif self.state == GameState.GAME_OVER:
            self.BGMPlayer.stop()
            self.scene = GameOverScene(self.window)
            self.BGMPlayer = BGMPlayer(self.scene.BGM)
            self.BGMPlayer.play()
        
        elif self.state == GameState.GAME_WIN:
            self.BGMPlayer.stop()
            self.scene = GameWinScene(self.window)
            self.BGMPlayer = BGMPlayer(self.scene.BGM)
            self.BGMPlayer.play()

    def update(self):
        self.clock.tick(fps)
        self.keys = pygame.key.get_pressed()
        self.eventChecker.event_checker(self.scene, self)
        if self.state == GameState.GAME_PLAY:
            self.scene.update(self.player, self.keyDown, self.keys)
        elif self.state == GameState.MAIN_MENU or self.state == GameState.GAME_OVER or self.state == GameState.GAME_WIN:
            self.scene.update(self.keyDown)
        self.keyDown = None

    def render(self):
        self.window.fill((0,0,0)) # fill the very background of the window with black
        if self.state == GameState.GAME_PLAY:
            self.scene.render(self.player)
            if self.scene.box == None:
                self.playerInfoDisplayer.player_info_render(self.player)
        elif self.state == GameState.MAIN_MENU or self.state == GameState.GAME_OVER or self.state == GameState.GAME_WIN:
            self.scene.render()
        pygame.display.update()
    
    def value_settler(self, value):
        if 'money' in value:
            self.player.money += value['money']
        if 'HP' in value:
            value['sprite'].HP += value['HP']
        if 'weapon' in value:
            self.player.inventory.append(value['weapon'])
        if 'DEF' in value:
            value['sprite'].DEF = value['DEF']
        if 'skill' in value:
            self.player.inventory.append(value['skill'])
        if self.player.HP <= 0:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIED))
        if 'sprite' in value:
            if isinstance(value['sprite'], Boss) and value['sprite'].HP <= 0:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_WIN))
            if isinstance(value['sprite'], Enemy_SIST) and value['sprite'].HP <= 0:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'skill': Skill("超载冲击")}))
            if isinstance(value['sprite'], Enemy_SLST) and value['sprite'].HP <= 0:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'skill': Skill("毒素注射")}))
            if isinstance(value['sprite'], Enemy_SPST) and value['sprite'].HP <= 0:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'skill': Skill("合金护盾")}))

    class PlayerInfoDisplay:
        def __init__(self, fontSize: int = 25, fontColor: tuple = (0, 0, 0)):
            self.fontSize = fontSize
            self.fontColor = fontColor
            self.font = pygame.font.Font(GamePath.font, self.fontSize)
            self.font.set_bold(True)
            self.textOffsetY = baseHeight // 2
            self.displaySurface = pygame.display.get_surface()
        def player_info_render(self, player):
            self.displaySurface.blit(self.font.render(f"HP: {player.HP}", True, self.fontColor), (baseWidth // 4, self.textOffsetY))
            self.displaySurface.blit(self.font.render(f"ATK: {player.ATK}", True, self.fontColor), (baseWidth // 4, self.textOffsetY * 2))
            self.displaySurface.blit(self.font.render(f"DEF: {player.DEF}", True, self.fontColor), (baseWidth // 4, self.textOffsetY * 3))
            self.displaySurface.blit(self.font.render(f"Money: {player.money}", True, self.fontColor), (baseWidth // 4, self.textOffsetY * 4))

            if player.inventory != []:
                self.displaySurface.blit(self.font.render(f"Inventory: ", True, self.fontColor), (baseWidth // 4, baseHeight * 10 - self.textOffsetY * 8))
                lineNumber = 0
                for i in range(len(player.inventory)):
                    if isinstance(player.inventory[i], Weapon):
                        self.displaySurface.blit(self.font.render(f"Weapon: {str(player.inventory[i])}", True, self.fontColor), (baseWidth // 4, baseHeight * 10 - self.textOffsetY * (7 - lineNumber)))
                        lineNumber += 1
                        self.displaySurface.blit(self.font.render(f"ATK: {player.inventory[i].ATK} DEF: {player.inventory[i].DEF}", True, self.fontColor), (baseWidth // 4, baseHeight * 10 - self.textOffsetY * (7 - lineNumber)))
                        lineNumber += 1
                    elif isinstance(player.inventory[i], Skill):
                        self.displaySurface.blit(self.font.render(f"Skill: {str(player.inventory[i])}", True, self.fontColor), (baseWidth // 4, baseHeight * 10 - self.textOffsetY * (7 - lineNumber)))
                    lineNumber += 1
