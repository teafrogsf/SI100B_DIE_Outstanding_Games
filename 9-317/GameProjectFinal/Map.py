import pygame
from Settings import *
from random import randint

# generating maps in every scene
class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.lastCameraX = 0
        self.lastCameraY = 0

    def update(self, cameraX, cameraY):
        self.rect.x -= (cameraX - self.lastCameraX)
        self.rect.y -= (cameraY - self.lastCameraY)
        self.lastCameraX = cameraX
        self.lastCameraY = cameraY

def gen_city_map():
    images = [pygame.image.load(tile) for tile in GamePath.cityTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.city_tileXnum):
        tmp = []
        for j in range(SceneSettings.city_tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)

    return mapObj

def gen_wild_map():
    images = [pygame.image.load(tile) for tile in GamePath.wildTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.wild_tileXnum):
        tmp = []
        for j in range(SceneSettings.wild_tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)

    return mapObj

def gen_hospital_map():
    image = pygame.image.load(GamePath.hospitalTiles)
    image = pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight))

    mapObj = []
    for i in range(SceneSettings.hospital_tileXnum):
        tmp = []
        for j in range(SceneSettings.hospital_tileYnum):
            tmp.append(image)
        mapObj.append(tmp)

    return mapObj

def gen_gym_map():
    image = pygame.image.load(GamePath.gymTiles)
    image = pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight))

    mapObj = []
    for i in range(SceneSettings.gym_tileXnum):
        tmp = []
        for j in range(SceneSettings.gym_tileYnum):
            tmp.append(image)
        mapObj.append(tmp)

    return mapObj

def gen_shop_map():
    image = pygame.image.load(GamePath.shopTiles)
    image = pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight))

    mapObj = []
    for i in range(SceneSettings.shop_tileXnum):
        tmp = []
        for j in range(SceneSettings.shop_tileYnum):
            tmp.append(image)
        mapObj.append(tmp)

    return mapObj

def gen_hospitaledge():
    image_none = pygame.image.load(GamePath.none)
    edge = pygame.sprite.Group()

    for i in range(SceneSettings.hospital_tileXnum):
        if i < SceneSettings.hospitalnone_tileleftXnum or i > SceneSettings.hospitalnone_tilerightXnum:
            for j in range(SceneSettings.hospital_tileYnum):
                edge.add(Block(image_none, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
        else:
            for j in range(SceneSettings.hospital_tileYnum):
                if j >= SceneSettings.hospitalnone_tiletopYnum and j <= SceneSettings.hospitalnone_tilebottomYnum:
                    pass
                else:
                    edge.add(Block(image_none, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

    return edge

def gen_gymobstacles():
    image_none = pygame.image.load(GamePath.none)
    image_wall = pygame.image.load(GamePath.redwall)
    obstacles = pygame.sprite.Group()

    for i in range(SceneSettings.gym_tileXnum):
        if i < SceneSettings.gymnone_tileleftXnum or i > SceneSettings.gymnone_tilerightXnum:
            for j in range(SceneSettings.gym_tileYnum):
                obstacles.add(Block(image_none, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
        else:
            for j in range(SceneSettings.gym_tileYnum):
                if j >= SceneSettings.gymnone_tiletopYnum and j <= SceneSettings.gymnone_tilebottomYnum:
                    if j == SceneSettings.gymnone_tiletopYnum + 5 and i <= SceneSettings.gymnone_tilerightXnum - 2:
                        obstacles.add(Block(image_wall, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
                    if j == SceneSettings.gymnone_tiletopYnum + 8 and i >= SceneSettings.gymnone_tileleftXnum + 2 and not i == SceneSettings.gymnone_tilerightXnum - 12 and not i == SceneSettings.gymnone_tilerightXnum - 13 and not i == SceneSettings.gymnone_tilerightXnum - 8 and not i == SceneSettings.gymnone_tilerightXnum - 9:
                        obstacles.add(Block(image_wall, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
                    if j == SceneSettings.gymnone_tiletopYnum + 11 and i <= SceneSettings.gymnone_tilerightXnum - 2 and not i == SceneSettings.gymnone_tilerightXnum - 8 and not i == SceneSettings.gymnone_tilerightXnum - 9 and not i == SceneSettings.gymnone_tilerightXnum - 3 and not i == SceneSettings.gymnone_tilerightXnum - 4:
                        obstacles.add(Block(image_wall, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
                    if j == SceneSettings.gymnone_tiletopYnum + 14 and i >= SceneSettings.gymnone_tileleftXnum + 2:
                        obstacles.add(Block(image_wall, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
                else:
                    obstacles.add(Block(image_none, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles

def gen_shopedge():
    image_none = pygame.image.load(GamePath.none)
    edge = pygame.sprite.Group()

    for i in range(SceneSettings.shopnone_tileleftXnum):
        for j in range(SceneSettings.shopnone_tilebottomYnum):
            edge.add(Block(image_none, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    for i in range(SceneSettings.shopnone_tilerightXnum, SceneSettings.shop_tileXnum):
        for j in range(SceneSettings.shopnone_tilebottomYnum):
            edge.add(Block(image_none, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

    return edge

class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        super().__init__()

        if type == DecorationType.Hospitalwall:
            self.image = pygame.transform.scale(image, (DecorationSettings.hospitalwallWidth, DecorationSettings.hospitalwallHeight))
        if type == DecorationType.Hospitaldoor:
            self.image = pygame.transform.scale(image, (DecorationSettings.hospitaldoorWidth, DecorationSettings.hospitaldoorHeight))
        if type == DecorationType.Wildgrass:
            self.image = pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight))
        if type == DecorationType.Gymwall:
            self.image = pygame.transform.scale(image, (DecorationSettings.gymwallWidth, DecorationSettings.gymwallHeight))
        if type == DecorationType.Gymstone:
            self.image = pygame.transform.scale(image, (DecorationSettings.gymstoneWidth, DecorationSettings.gymstoneHeight)) 
        if type == DecorationType.Gymbg:
            self.image = pygame.transform.scale(image, (DecorationSettings.gymbgWidth, DecorationSettings.gymbgHeight))
        if type == DecorationType.Shopwall:
            self.image = pygame.transform.scale(image, (DecorationSettings.shopwallWidth, DecorationSettings.shopwallHeight))
        if type == DecorationType.Shopshelf:
            self.image = pygame.transform.scale(image, (DecorationSettings.shopshelfWidth, DecorationSettings.shopshelfHeight))
        if type == DecorationType.Cityroad:
            self.image = pygame.transform.scale(image, (DecorationSettings.cityroadWidth, DecorationSettings.cityroadHeight))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.lastCameraX = 0
        self.lastCameraY = 0

    def update(self, cameraX, cameraY):
        self.rect.x -= (cameraX - self.lastCameraX)   
        self.rect.y -= (cameraY - self.lastCameraY)
        self.lastCameraX = cameraX
        self.lastCameraY = cameraY

def gen_city_road():
    image_road = pygame.image.load(GamePath.cityroad)
    road = pygame.sprite.Group()

    road.add(Decoration(image_road, SceneSettings.tileWidth * 0, SceneSettings.tileHeight * 2, DecorationType.Cityroad))
    return road


def gen_hospital_wall():
    image_wall = pygame.image.load(GamePath.hospitalwall)
    hospital_wall = pygame.sprite.Group()

    hospital_wall.add(Decoration(image_wall, SceneSettings.tileWidth * SceneSettings.hospitalwall_left_x, SceneSettings.tileHeight * SceneSettings.hospitalwall_top_y, DecorationType.Hospitalwall))

    return hospital_wall

def gen_hospital_door():
    image_door = pygame.image.load(GamePath.hospitaldoor)
    hospital_door = pygame.sprite.Group()

    hospital_door.add(Decoration(image_door, SceneSettings.tileWidth * SceneSettings.hospitaldoor_left_x, SceneSettings.tileHeight * SceneSettings.hospitaldoor_top_y, DecorationType.Hospitaldoor))

    return hospital_door

def gen_gym_bg():
    image_bg = pygame.image.load(GamePath.gymbg)
    gym_bg = pygame.sprite.Group()

    gym_bg.add(Decoration(image_bg, SceneSettings.tileWidth * SceneSettings.gymbg_left_x, SceneSettings.tileHeight * SceneSettings.gymbg_top_y, DecorationType.Gymbg))

    return gym_bg

def gen_gym_wall():
    image_wall = pygame.image.load(GamePath.gymwall)
    gym_wall = pygame.sprite.Group()

    gym_wall.add(Decoration(image_wall, SceneSettings.tileWidth * SceneSettings.gymwall_left_x, SceneSettings.tileHeight * SceneSettings.gymwall_top_y, DecorationType.Gymwall))
    
    return gym_wall

def gen_gym_stone():
    image_stone = pygame.image.load(GamePath.gymstone)
    gym_stone = pygame.sprite.Group()

    gym_stone.add(Decoration(image_stone, SceneSettings.tileWidth * SceneSettings.gymstone1_left_x, SceneSettings.tileHeight * SceneSettings.gymstone1_top_y, DecorationType.Gymstone))
    gym_stone.add(Decoration(image_stone, SceneSettings.tileWidth * SceneSettings.gymstone2_left_x, SceneSettings.tileHeight * SceneSettings.gymstone2_top_y, DecorationType.Gymstone))

    return gym_stone

def gen_shop_wall():
    image_wall = pygame.image.load(GamePath.shopwall)
    image_shopshelf1 = pygame.image.load(GamePath.shopshelf1)
    image_shopshelf2 = pygame.image.load(GamePath.shopshelf2)
    shop_wall = pygame.sprite.Group()

    shop_wall.add(Decoration(image_wall, SceneSettings.tileWidth * SceneSettings.shopwall_left_x, SceneSettings.tileHeight * SceneSettings.shopwall_top_y, DecorationType.Shopwall))
    shop_wall.add(Decoration(image_shopshelf1, SceneSettings.tileWidth * SceneSettings.shopshelf1_left_x, SceneSettings.tileHeight * SceneSettings.shopshelf1_top_y, DecorationType.Shopshelf))
    shop_wall.add(Decoration(image_shopshelf2, SceneSettings.tileWidth * SceneSettings.shopshelf2_left_x, SceneSettings.tileHeight * SceneSettings.shopshelf2_top_y, DecorationType.Shopshelf))

    return shop_wall

def gen_obstacles():
    image_wall = pygame.image.load(GamePath.cityWall)
    obstacles = pygame.sprite.Group()

    for i in range(SceneSettings.city_tileXnum):
        for j in range(SceneSettings.city_tileYnum):
            if j <= 1 and i <= 36:
                obstacles.add(Block(image_wall, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            elif j >= 26:
                obstacles.add(Block(image_wall, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            elif i >= 46 and j >= 17:
                obstacles.add(Block(image_wall, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
            else:
                pass
    return obstacles

def gen_wild_grass():
    image_grass = pygame.image.load(GamePath.wildgrass)
    grass = pygame.sprite.Group()

    for i in range(15, 31):
        for j in range(33, 44):
            grass.add(Decoration(image_grass, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j, DecorationType.Wildgrass))
    
    return grass

def gen_wild_trees():
    image_tree = pygame.image.load(GamePath.wildtree)
    trees = pygame.sprite.Group()

    for i in range(0, SceneSettings.wild_tileXnum):
        for j in range(0, SceneSettings.wild_tileYnum):
            if i <= 20 and j <= 20:
                pass
            elif j >= 15 and j <= 20 and i <= 40:
                pass
            elif i >= 35 and i <= 40 and j >= 20 and j <= 43:
                pass
            elif i >= 15 and i <= 40 and j >= 33 and j <= 43:
                pass
            else:
                trees.add(Block(image_tree, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

    return trees


class Building(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        super().__init__()

        if type == BuildingType.Hospital:
            self.image = pygame.transform.scale(image, (BuildingSettings.hospitalWidth, BuildingSettings.hospitalHeight))
        if type == BuildingType.Gym:
            self.image = pygame.transform.scale(image, (BuildingSettings.gymWidth, BuildingSettings.gymHeight))
        if type == BuildingType.Shop:
            self.image = pygame.transform.scale(image, (BuildingSettings.shopWidth, BuildingSettings.shopHeight))
        if type == BuildingType.Citystation:
            self.image = pygame.transform.scale(image, (BuildingSettings.citystationWidth, BuildingSettings.citystationHeight))
        if type == BuildingType.Wildstation:
            self.image = pygame.transform.scale(image, (BuildingSettings.wildstationWidth, BuildingSettings.wildstationHeight))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.lastCameraX = 0
        self.lastCameraY = 0

    def update(self, cameraX, cameraY):
        self.rect.x -= (cameraX - self.lastCameraX)   
        self.rect.y -= (cameraY - self.lastCameraY)
        self.lastCameraX = cameraX
        self.lastCameraY = cameraY
    

def gen_hospital():
    image = pygame.image.load(GamePath.hospital)
    hospital = pygame.sprite.Group()
    
    hospital.add(Building(image, SceneSettings.tileWidth * SceneSettings.hospital_left_x, SceneSettings.tileHeight * SceneSettings.hospital_top_y, BuildingType.Hospital))
    
    return hospital
    
def gen_gym():
    image = pygame.image.load(GamePath.gym)
    gym = pygame.sprite.Group()

    gym.add(Building(image, SceneSettings.tileWidth * SceneSettings.gym_left_x, SceneSettings.tileHeight * SceneSettings.gym_top_y, BuildingType.Gym))

    return gym

def gen_shop():
    image = pygame.image.load(GamePath.shop)
    shop = pygame.sprite.Group()

    shop.add(Building(image, SceneSettings.tileWidth * SceneSettings.shop_left_x, SceneSettings.tileHeight * SceneSettings.shop_top_y, BuildingType.Shop))

    return shop

def gen_citystation():
    image = pygame.image.load(GamePath.citystation)
    citystation = pygame.sprite.Group()

    citystation.add(Building(image, SceneSettings.tileWidth * SceneSettings.citystation_left_x, SceneSettings.tileHeight * SceneSettings.citystation_top_y, BuildingType.Citystation))

    return citystation

def gen_wildstation():
    image = pygame.image.load(GamePath.wildstation)
    wildstation = pygame.sprite.Group()

    wildstation.add(Building(image, SceneSettings.tileWidth * SceneSettings.wildstation_left_x, SceneSettings.tileHeight * SceneSettings.wildstation_top_y, BuildingType.Wildstation))

    return wildstation
    
    