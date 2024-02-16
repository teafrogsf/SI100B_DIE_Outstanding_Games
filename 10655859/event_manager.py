import pygame
import sys
from settings import *
from collision_detction import *

class EventManager:
    def __init__(self, game):
        self.game = game
        
        
    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.game.game_on:
                if event.button == 1 and not self.game.player.shot and not self.game.weapon.reloading:
                    self.fire_event()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and self.game.scene_manager.enable:
                    self.portal_event()
            if event.type == Kill_Event:
                self.grow()
            if event.type == Player_Hit_Event:
                self.damage()
        
    def fire_event(self):
        self.game.sound.shotgun.play()
        self.game.player.shot = True
        self.game.weapon.reloading = True
        self.game.scene_manager.counter11 = 30
        
    def portal_event(self):
        self.game.sound.bgm.stop()
        self.game.new_game((self.game.map.num + 1) % 2)
        
    def grow(self):
        self.game.settings.Player_Armor += 10
        self.game.ui.update()
        
    def damage(self):
        self.game.ui.update()
        self.game.object_renderer.player_get_damage()
        self.game.sound.player_pain.play()
        self.game.player.check_if_end()