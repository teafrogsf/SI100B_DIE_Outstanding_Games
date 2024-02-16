import math
import pygame

RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

Player_Pos = 2.5, 2.4
Player_Angle = 0
Player_Speed = 0.0025
Player_Rot_Speed = 0.002
Player_Size_Scale = 10
Player_Initial_Health = 100

MOUSE_SENSITIVITY = 0.0002
MOUSE_MAX_REL = 40
MOUSE_BOARDER_LEFT = 100
MOUSE_BOARDER_RIGHT = WIDTH - MOUSE_BOARDER_LEFT

FOV = math.pi / 2.5
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

FLOOR = (0, 0, 0)

RECOIL = 0.2

Kill_Event = pygame.USEREVENT + 0
Player_Hit_Event = pygame.USEREVENT + +1

class Settings:
    def __init__(self, game):
        self.game = game
        self.fov = FOV
        self.half_fov = HALF_FOV
        self.delta_angle = DELTA_ANGLE
        self.screen_dist = SCREEN_DIST
        self.Player_Armor = 0
        self.Enemy_Num = 30
        self.Enemy_Attack = 10
        
    def update(self):
        if self.game.weapon.frame_counter == 1:
            self.fov = math.pi / 2.25
        elif self.game.weapon.frame_counter == 2:
            self.fov = math.pi / 2
        elif self.game.weapon.frame_counter == 3:
            self.fov = math.pi / 2.25
        else:
            self.fov = FOV
        self.half_fov = self.fov / 2
        self.delta_angle = self.fov / NUM_RAYS
        self.screen_dist = HALF_WIDTH / math.tan(self.half_fov)