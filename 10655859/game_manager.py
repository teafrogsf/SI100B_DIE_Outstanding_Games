import pygame
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from weapon import *
from sound import *
from cg import *
from opening import *
from scene_manager import *
from event_manager import *
from ui import *

class Game:
    def __init__(self, game):
        pygame.font.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.opening = Opening(self)
        self.opening.run()
        self.scene_manager = SceneManager(self)
        self.event_manager = EventManager(self)
        self.settings = Settings(self)
        self.ui = UI(self)
        self.new_game(0)
    
    def new_game(self, map_num):
        self.settings.Enemy_Num += 2
        self.settings.Player_Armor += 30
        self.game_on = True
        self.player = Player(self)
        self.map = Map(self, map_num)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.sound.bgm.play(loops=2)
        self.ui.update()
    
    def update(self):
        self.event_manager.check()
        self.settings.update()
        self.player.update()
        self.raycasting.update()
        self.map.update()
        self.weapon.update()
        self.scene_manager.portal_detection()
        self.scene_manager.language()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        self.map.draw()
        self.player.draw()
        self.ui.draw()
        
    def run(self):
        while True:
            self.update()
            self.draw()