# -*- coding:utf-8 -*-

import pygame

from Settings import *
from random import random, randint
from Attributes import *
from Scene import *
from Portal import *
class Block(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, width=SceneSettings.tileWidth, height=SceneSettings.tileHeight):
        super().__init__()
        ##### Your Code Here ↓ #####
        self.image = pygame.transform.scale(image.convert_alpha(),(width,height))
        self.rect = self.image.get_rect(topleft = (x,y))#存图片的rect和碰撞体积的rect
        # self.rect = (0,0,0,0)
        self.img_rect = self.image.get_rect(topleft = (x,y))
        self.pos = None
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        window.blit(self.image, self.img_rect)
        ##### Your Code Here ↑ #####
def gen_index_map():
    ##### Your Code Here ↓ #####
    image = pygame.image.load(GamePath.index)
    # 2024/01/15 lst update begin
    # image = pygame.transform.scale(image,(SceneSettings.House_width,SceneSettings.House_height))
    bg_size = image.get_size()
    image = pygame.transform.scale(image,(WindowSettings.width,WindowSettings.height))
    map_info_setting.map_info = 12
    # 2024/01/15 lst update end
    return image
def gen_village_map():
    ##### Your Code Here ↓ #####
    image = pygame.image.load(GamePath.village)
    # 2024/01/15 lst update begin
    # image = pygame.transform.scale(image,(SceneSettings.House_width,SceneSettings.House_height))
    bg_size = image.get_size()
    displacement_settings.offset_x_max = (bg_size[0]-WindowSettings.width)
    displacement_settings.offset_y_max = (bg_size[1]-WindowSettings.height)
    if(IndexSettin.index_state == 1):
        displacement_settings.village_map_x = displacement_settings.offset_x_max
        displacement_settings.village_map_y = displacement_settings.offset_y_max
        IndexSettin.index_state += 1
    # image = pygame.transform.scale(image,(bg_size[0],bg_size[1]))
    map_info_setting.map_info = 1
    # 2024/01/15 lst update end
    return image

def gen_village_obstacle():
    obstacles = pygame.sprite.Group()
    for i in range(len(GamePath.village_obstacle)):
        image = pygame.image.load(GamePath.village_obstacle[i])
        building=Block(image,ObstaclesLoc.img_x[i]-displacement_settings.village_map_x,ObstaclesLoc.img_y[i]-displacement_settings.village_map_y,ObstacleSize.img_width[i],ObstacleSize.img_height[i])
        # building.rect=(ObstaclesLoc.hitbox_x[i],ObstaclesLoc.hitbox_y[i],ObstacleSize.hitbox_width[i],ObstacleSize.hitbox_height[i])
        # 最后两个传送无需减人高度，无需碰撞检测
        if(i<5):
            building.rect=(ObstaclesLoc.img_x[i]-displacement_settings.village_map_x,ObstaclesLoc.img_y[i]-displacement_settings.village_map_y+PlayerSettings.playerHeight,ObstacleSize.img_width[i],ObstacleSize.img_height[i]-PlayerSettings.playerHeight*2)
        else:
            # building.rect=(ObstaclesLoc.img_x[i]-displacement_settings.village_map_x,ObstaclesLoc.img_y[i]-displacement_settings.village_map_y,ObstacleSize.img_width[i],ObstacleSize.img_height[i]-PlayerSettings.playerHeight)
            building.rect=(ObstaclesLoc.img_x[i]-displacement_settings.village_map_x,ObstaclesLoc.img_y[i]-displacement_settings.village_map_y,0,0)
        obstacles.add(building)
    return obstacles

def gen_house_map():
    image = pygame.image.load(GamePath.house)
    image = pygame.transform.scale(image,(SceneSettings.House_width,SceneSettings.House_height))
    map_info_setting.map_info = 2
    return image

def gen_house_obstacle():
    obstacles = pygame.sprite.Group()
    for i in range(len(GamePath.house_obstacle)):
        image = pygame.image.load(GamePath.house_obstacle[i])
        # building=Block(image,House_ObstaclesLoc.img_x[i],House_ObstaclesLoc.img_y[i],House_ObstacleSize.img_width[i],House_ObstacleSize.img_height[i]-PlayerSettings.playerHeight)
        # 最后1个传送无需减人高度，无需碰撞检测
        # print("i :::::::::: ",i)
        if(i<10):
            building=Block(image,House_ObstaclesLoc.img_x[i],House_ObstaclesLoc.img_y[i],House_ObstacleSize.img_width[i],House_ObstacleSize.img_height[i]-PlayerSettings.playerHeight)
            building.rect=(House_ObstaclesLoc.img_x[i],House_ObstaclesLoc.img_y[i],House_ObstacleSize.img_width[i],House_ObstacleSize.img_height[i] - PlayerSettings.playerHeight)
        else:
            building=Block(image,House_ObstaclesLoc.img_x[i],House_ObstaclesLoc.img_y[i],House_ObstacleSize.img_width[i],House_ObstacleSize.img_height[i])
            building.rect=(House_ObstaclesLoc.img_x[i],House_ObstaclesLoc.img_y[i],0,0)
        # print(building.rect)
        obstacles.add(building)
    return obstacles

# house场景切换门图片
def gen_village_portals():
    portals = pygame.sprite.Group()
    img = pygame.image.load(GamePath.village_portal)
    img = pygame.transform.scale(img,(PortalSettings.width,PortalSettings.height))
    portals.add(Portal(img,ObstaclesLoc.img_x[1]-displacement_settings.village_map_x+ObstacleSize.img_width[1]//2-PortalSettings.width//2,ObstaclesLoc.img_y[1]-displacement_settings.village_map_y+ObstacleSize.img_height[1]//2-PortalSettings.height//2,SceneType.Village,SceneType.HOUSE))
    return portals

# 地牢地图 2024/01/17
def gen_dungeon_map():
    image = pygame.image.load(GamePath.dungeon)
    image = image.convert()
    image = pygame.transform.scale(image,(WindowSettings.width,WindowSettings.height))
    map_info_setting.map_info = 3
    return image
# 地牢障碍 2024/01/17
def gen_dungeon_obstacle():
    obstacles = pygame.sprite.Group()
    for i in range(len(GamePath.dungeon_obstacle)):
        image = pygame.image.load(GamePath.dungeon_obstacle[i])
        # building=Block(image,House_ObstaclesLoc.img_x[i],House_ObstaclesLoc.img_y[i],House_ObstacleSize.img_width[i],House_ObstacleSize.img_height[i]-PlayerSettings.playerHeight)
        # 最后1个传送无需减人高度，无需碰撞检测
        # print("i :::::::::: ",i)
        if(i<12):
            building=Block(image,Dungeon_ObstaclesLoc.img_x[i],Dungeon_ObstaclesLoc.img_y[i],Dungeon_ObstacleSize.img_width[i],Dungeon_ObstacleSize.img_height[i]-PlayerSettings.playerHeight)
            building.rect=(Dungeon_ObstaclesLoc.img_x[i],Dungeon_ObstaclesLoc.img_y[i],Dungeon_ObstacleSize.img_width[i],Dungeon_ObstacleSize.img_height[i] - PlayerSettings.playerHeight)
        else:
            building=Block(image,Dungeon_ObstaclesLoc.img_x[i],Dungeon_ObstaclesLoc.img_y[i],Dungeon_ObstacleSize.img_width[i],Dungeon_ObstacleSize.img_height[i])
            building.rect=(Dungeon_ObstaclesLoc.img_x[i],Dungeon_ObstaclesLoc.img_y[i],0,0)
        # print(building.rect)
        obstacles.add(building)
    return obstacles
# # house场景切换门图片
# def gen_village_transmit_dungeon():
#     portals = pygame.sprite.Group()
#     img = pygame.image.load(GamePath.village_transmit_dungeon)
#     img = pygame.transform.scale(img,(PortalSettings.width,PortalSettings.height))
#     portals.add(Portal(img,ObstaclesLoc.img_x[1]-displacement_settings.village_map_x+ObstacleSize.img_width[1]//2-PortalSettings.width//2,ObstaclesLoc.img_y[1]-displacement_settings.village_map_y+ObstacleSize.img_height[1]//2-PortalSettings.height//2,SceneType.Village,SceneType.HOUSE))
#     return portals
# 野外图 2024/01/17
def gen_wild_map():
    image = pygame.image.load(GamePath.wild)
    # image = pygame.transform.scale(image,(WindowSettings.width,WindowSettings.height))
    map_info_setting.map_info = 4
    return image
# 野外障碍 2024/01/17
def gen_wild_obstacle():
    obstacles = pygame.sprite.Group()
    for i in range(len(GamePath.wild_obstacle)):
        image = pygame.image.load(GamePath.wild_obstacle[i])
        # building=Block(image,House_ObstaclesLoc.img_x[i],House_ObstaclesLoc.img_y[i],House_ObstacleSize.img_width[i],House_ObstacleSize.img_height[i]-PlayerSettings.playerHeight)
        # 最后1个传送无需减人高度，无需碰撞检测
        # print("i :::::::::: ",i)
        building=Block(image,Wild_ObstaclesLoc.img_x[i],Wild_ObstaclesLoc.img_y[i],Wild_ObstacleSize.img_width[i],Wild_ObstacleSize.img_height[i])
        # 传送不需要有碰撞检测
        if(i<4):
            building.rect=(Wild_ObstaclesLoc.img_x[i],Wild_ObstaclesLoc.img_y[i],Wild_ObstacleSize.img_width[i],Wild_ObstacleSize.img_height[i] )
        else:
            building.rect=(Wild_ObstaclesLoc.img_x[i],Wild_ObstaclesLoc.img_y[i],0,0)

        # print(building.rect)
        obstacles.add(building)
    return obstacles
# boss图 2024/01/17
def gen_boss_map():
    image = pygame.image.load(GamePath.boss)
    image = pygame.transform.scale(image,(WindowSettings.width,WindowSettings.height))
    map_info_setting.map_info = 5
    return image
# 游戏失败场景 2024/01/27
def gen_game_over_map():
    image = pygame.image.load(GamePath.game_over)
    image = image.convert()
    image = pygame.transform.scale(image,(WindowSettings.width,WindowSettings.height))
    map_info_setting.map_info = 3
    return image
def gen_boss_obstacle():
    ##### Your Code Here ↓ #####
    pass
# 游戏失败场景 2024/01/27
def gen_game_victory_map():
    image = pygame.image.load(GamePath.game_victory)
    image = image.convert()
    image = pygame.transform.scale(image,(WindowSettings.width,WindowSettings.height))
    map_info_setting.map_info = 13
    return image