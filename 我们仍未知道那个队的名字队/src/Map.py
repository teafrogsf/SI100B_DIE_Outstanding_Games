from Setting import *
from pytmx.util_pygame import load_pygame
from NPC import *
from Enemy import *
from Box import *

def load_obstacles(tmx_file):
    obstacles = []
    tmxData = load_pygame(tmx_file)
    
    # 障碍物在名为 '障碍物' 的图层
    obstaclesLayer = tmxData.get_layer_by_name('障碍物')
    
    for x, y, image in obstaclesLayer.tiles():
        obstacles.append(Tile(pos = (x * 32, y * 32), image = image))
    
    return obstacles

def load_portal(tmx_file, layername, portalTarget):
    portals = []
    tmxData = load_pygame(tmx_file)
    portalLayer = tmxData.get_layer_by_name(f'{layername}')
    for portal in portalLayer:
        if portal.image:
            portals.append(Portal(pos = (portal.x, portal.y), image = portal.image, target = portalTarget))
    return portals

def load_npc(tmx_file, layername):
    npcs = []
    tmxData = load_pygame(tmx_file)
    npcLayer = tmxData.get_layer_by_name(f'{layername}')
    for npc in npcLayer:
        if npc.image:
            npcs.append(globals()[layername](pos = (npc.x, npc.y), image = npc.image))
    return npcs

def load_ground(tmx_file):
    ground = []
    tmxData = load_pygame(tmx_file)
    
    groundLayer = tmxData.get_layer_by_name('地面')
    
    for x, y, image in groundLayer.tiles():
        ground.append(Tile(pos = (x*32, y*32), image = image))
    
    return ground

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos = (0, 0), width=TileSettings.tileLength, height=TileSettings.tileLength):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Portal(pygame.sprite.Sprite):
    def __init__(self, image, pos = (0, 0), width=TileSettings.tileLength, height=TileSettings.tileLength, target = None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.portalTarget = target
