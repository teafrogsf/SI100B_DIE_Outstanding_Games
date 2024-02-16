# -*- coding:utf-8 -*-

from enum import Enum
import pygame

class WindowSettings:
    name = "Thgink Luos"
    width = 1280
    height = 720
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class SceneSettings:
    city_tileXnum = 48 # 64
    city_tileYnum = 36 # 36

    tileWidth = tileHeight = 40
    hospital_left_x = 16
    hospital_top_y = 2

    gym_left_x = 26
    gym_top_y = 2

    shop_left_x = 6
    shop_top_y = 2

    citystation_left_x = 37
    citystation_top_y = 0

    wildstation_left_x = 0
    wildstation_top_y = 0

    hospitalwall_left_x = 4
    hospitalwall_top_y = 2

    gymwall_left_x = 7
    gymwall_top_y = 0

    gymstone1_left_x = 13
    gymstone2_left_x = 18
    gymstone1_top_y = 1
    gymstone2_top_y = 1

    gymbg_left_x = 10
    gymbg_top_y = 2

    hospitaldoor_left_x = 15
    hospitaldoor_top_y = 11

    shopwall_left_x = 7
    shopwall_top_y = 0

    shopshelf1_left_x = 7
    shopshelf1_top_y = 4

    shopshelf2_left_x = 22
    shopshelf2_top_y = 4

    wild_tileXnum = 48
    wild_tileYnum = 48
    
    hospital_tileXnum = 32
    hospital_tileYnum = 18

    gym_tileXnum = 32
    gym_tileYnum = 18

    shop_tileXnum = 32
    shop_tileYnum = 18
    
    hospitalnone_tileleftXnum = 4
    hospitalnone_tiletopYnum = 4
    hospitalnone_tilerightXnum = 27
    hospitalnone_tilebottomYnum = 13

    gymnone_tileleftXnum = 7
    gymnone_tiletopYnum = 0
    gymnone_tilerightXnum = 24
    gymnone_tilebottomYnum = 17

    shopnone_tileleftXnum = 7
    shopnone_tilerightXnum = 25
    shopnone_tilebottomYnum = 18

class PlayerSettings:
    # Initial Player Settings
    playerSpeed = 7
    playerWidth = 40
    playerHeight = 60
    playerHP = 20
    playerAttack = 5
    playerDefence = 1
    playerMoney = 100

class NPCSettings:
    npcSpeed = 1
    npcWidth = 60
    npcHeight = 60
    npcTalkCD = 30
    npcPatrollingRangeX = 120

class NPCType(Enum):
    DIALOG = 1
    MONSTER = 2
    SHOP = 3

class BossSettings:
    width = 300
    height = 300

class BuildingType(Enum):
    Hospital = 1
    Gym = 2
    Citystation = 3
    Wildstation = 4
    Shop = 5

class DecorationType(Enum):
    Hospitalwall = 1
    Hospitaldoor = 2
    Wildgrass = 3
    Gymwall = 4
    Gymstone = 5
    Gymbg = 6
    Shopwall = 7
    Shopshelf = 8
    Cityroad = 9

class BuildingSettings:
    hospitalWidth = 200
    hospitalHeight = 160
    gymWidth = 200
    gymHeight = 160
    shopWidth = 200
    shopHeight = 160
    citystationWidth = 440
    citystationHeight = 680
    wildstationWidth = 600
    wildstationHeight = 400

class DecorationSettings:
    hospitalwallWidth = 960
    hospitalwallHeight = 240
    hospitaldoorWidth = 120
    hospitaldoorHeight = 120
    gymwallWidth = 720
    gymwallHeight = 80
    gymstoneWidth = 40
    gymstoneHeight = 80
    gymbgWidth = 480
    gymbgHeight = 640
    
    shopwallWidth = 720
    shopwallHeight = 160
    shopshelfWidth = 120
    shopshelfHeight = 560
    
    cityroadWidth = 1280
    cityroadHeight = 960

class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxAlpha = 150
    boxStartX = WindowSettings.width // 4           # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20 # Coordinate Y of the box

    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 + 10         # Coordinate X of the first line of dialog
    textStartY = WindowSettings.height // 3 * 2 + 30    # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3                # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20

    flashCD = 15

class BattleSettings:
    boxWidth = WindowSettings.width * 3 // 4 
    boxHeight = WindowSettings.height * 7 // 8 
    boxAlpha = 150
    boxStartX = WindowSettings.width // 8           # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 
    textPlayerStartX = WindowSettings.width // 6          # Coordinate X of the first line of dialog
    textMonsterStartX = WindowSettings.width // 6 * 4   
    textStartY = WindowSettings.height // 6         # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3            # Vertical distance of two lines
    descriptionX = WindowSettings.width // 6
    descriptionY = WindowSettings.height // 5 * 3

    playerWidth = WindowSettings.width // 5
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8
    playerCoordY = WindowSettings.height // 10 * 3

    monsterWidth = WindowSettings.width // 5
    monsterHeight = WindowSettings.height // 3
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 10 * 3

    pokeBallWidth = 200
    pokeBallHeight = 200
    pokeBallCoorX = WindowSettings.width // 5 * 2
    pokeBallCoorY = WindowSettings.height // 5 * 3

    settleCoorX = WindowSettings.width // 10 * 3
    settleCoorY = WindowSettings.height // 2
    moveCoorX = [
        WindowSettings.width // 7,
        WindowSettings.width // 50 * 21,
        WindowSettings.width // 7,
        WindowSettings.width // 50 * 21,
    ]
    moveCoorY = [
        WindowSettings.height // 8 * 6,
        WindowSettings.height // 8 * 6,
        WindowSettings.height // 8 * 7,
        WindowSettings.height // 8 * 7,
    ]
    actCoorX = [
        WindowSettings.width // 2,
        WindowSettings.width // 10 * 7,
        WindowSettings.width // 2,
        WindowSettings.width // 10 * 7,
    ]
    actCoorY = [
        WindowSettings.height // 8 * 6,
        WindowSettings.height // 8 * 6,
        WindowSettings.height // 8 * 7,
        WindowSettings.height // 8 * 7,
    ]

    moveDescriptionX = WindowSettings.width // 3 * 2
    moveDescriptionY = WindowSettings.height // 4 * 3

    stepSize = 20
    animationCount = 15

    moveSelectCD = 6
    actSelectCD = 6
    bagSelectCD = 6
    pokeSelectCD = 6
    pressCD = 10

    encounterProbability = 30
    encounterCD = 60
    battleCD = 90

    # state code
    stateAct = 4
    stateMove = 0
    stateBag = 1
    statePoke = 2
    stateEscape = 3

class SubMenuSetting:
    # background
    boxWidth = WindowSettings.width * 3 // 4 
    boxHeight = WindowSettings.height * 7 // 8 
    boxAlpha = 150
    boxStartX = WindowSettings.width // 8
    boxStartY = WindowSettings.height // 8

    # menu
    menuWidth = WindowSettings.width // 4
    menuHeight = WindowSettings.height // 5 * 2
    menuAlpha = 150
    menuStartX = WindowSettings.width // 4 * 3
    menuStartY = WindowSettings.height // 5
    menuTextStartX = WindowSettings.width // 5 * 4
    menuTextStartY = WindowSettings.height // 4

    #pokemon
    startImageWidth = 240
    startImageHeight = 240
    otherImageWidth = 100
    otherImageHeight = 100
    startPokeCoorX = WindowSettings.width // 6
    startPokeCoorY = WindowSettings.height // 5
    otherPokeCoorX = WindowSettings.width // 20 * 9
    otherPokeCoorY = WindowSettings.height // 25 * 6

    startTextStartX = WindowSettings.width // 6
    startTextStartY = WindowSettings.height // 2
    otherTextStartX = WindowSettings.width // 2
    otherTextStartY = WindowSettings.height // 4
    todoTextStartX = WindowSettings.width // 6
    todoTextStartY = WindowSettings.height // 4 * 3
    textVerticalDist = WindowSettings.height // 8

    # pokemon overview
    imageWidth = 360
    imageHeight = 360
    imageCoorX = WindowSettings.width // 8
    imageCoorY = WindowSettings.height // 6
    leftTextStartX = WindowSettings.width // 5
    leftTextStartY = WindowSettings.height // 3 * 2
    middleTextStartX = WindowSettings.width // 20 * 9
    middleTextStartY = WindowSettings.height // 4
    rightTextStartX = WindowSettings.width // 20 * 13
    rightTextStartY = WindowSettings.height // 4

    # bag
    itemStartX = WindowSettings.width // 25 * 16
    itemStartY = WindowSettings.height // 4
    quitCoorX = WindowSettings.width // 25 * 16
    quitCoorY = WindowSettings.height // 8 * 7

    itemImageCoorX = WindowSettings.width // 6
    itemImageCoorY = WindowSettings.height // 5 * 3
    bagImageCoorX = WindowSettings.width // 5
    bagImageCoorY = WindowSettings.height // 5
    textStartX = WindowSettings.width // 6
    textStartY = WindowSettings.height // 4 * 3

    itemImageWidth = 100
    itemImageHeight = 100
    bagImageWidth = 200
    bagImageHeight = 200

    # keydown control
    menuSelectCD = 6
    bagSelectCD = 6
    pokeSelectCD = 6
    pressCD = 10

    # state code
    statePokemon = 0
    stateBag = 1
    stateSave = 2
    stateBack = 3
    stateExit = 4
    stateMenu = 5

class ShopSettings:
    boxWidth = 800
    boxHeight = 200
    boxStartX = WindowSettings.width // 4   # Coordinate X of the box
    boxStartY = WindowSettings.height // 3  # Coordinate Y of the box

    textSize = 56 # Default font size
    textStartX = boxStartX + 10         # Coordinate X of the first line of dialog
    textStartY = boxStartY + 25    # Coordinate Y of the first line of dialog

    selectCD = 4
    pressCD = 10

class PokemonSettings:
    width = WindowSettings.width // 6
    height = WindowSettings.height // 6

class GamePath:
    # Window related path
    origin = r".\assets\background\origin.png"
    menu = r".\assets\background\menu.png"
    endgame = r".\assets\background\endgame.png"
    wild = r".\assets\background\wild.png"
    mapBlock = r".\assets\background\map.png"
    hospitalBG = r".\assets\background\Hospital.png"

    # player/npc related path
    npc = r".\assets\npc\npc.png"
    player_left = [
        r".\assets\player\1.png", 
        r".\assets\player\1.png",
        r".\assets\player\2.png", 
        r".\assets\player\2.png", 
        r".\assets\player\3.png", 
        r".\assets\player\3.png", 
        r".\assets\player\4.png", 
        r".\assets\player\4.png", 
        # 8 frames for a single loop of animation looks much better.
    ]

    player_right = [
        r".\assets\player\5.png", 
        r".\assets\player\5.png",
        r".\assets\player\6.png", 
        r".\assets\player\6.png", 
        r".\assets\player\7.png", 
        r".\assets\player\7.png", 
        r".\assets\player\8.png", 
        r".\assets\player\8.png", 
        # 8 frames for a single loop of animation looks much better.
    ]

    player_up = [
        r".\assets\player\9.png", 
        r".\assets\player\9.png",
        r".\assets\player\10.png", 
        r".\assets\player\10.png", 
        r".\assets\player\11.png", 
        r".\assets\player\11.png", 
        r".\assets\player\12.png", 
        r".\assets\player\12.png", 
        # 8 frames for a single loop of animation looks much better.
    ]

    player_down = [
        r".\assets\player\13.png", 
        r".\assets\player\13.png",
        r".\assets\player\14.png", 
        r".\assets\player\14.png", 
        r".\assets\player\15.png", 
        r".\assets\player\15.png", 
        r".\assets\player\16.png", 
        r".\assets\player\16.png", 
        # 8 frames for a single loop of animation looks much better.
    ]

    pokemonFront = [
        r".\assets\pokemon\front01.png",
        r".\assets\pokemon\front02.png",
        r".\assets\pokemon\front03.png",
        r".\assets\pokemon\front04.png",
        r".\assets\pokemon\front05.png",
        r".\assets\pokemon\front06.png",
        r".\assets\pokemon\front07.png",
        r".\assets\pokemon\front08.png",
        r".\assets\pokemon\front09.png",
        r".\assets\pokemon\front10.png",
        r".\assets\pokemon\front11.png",
        r".\assets\pokemon\front12.png",
        r".\assets\pokemon\front13.png",
        r".\assets\pokemon\front14.png",
        r".\assets\pokemon\front15.png",
        r".\assets\pokemon\front16.png",
        r".\assets\pokemon\front17.png",
        r".\assets\pokemon\front18.png",
    ]
    pokemonBack = [
        r".\assets\pokemon\back01.png",
        r".\assets\pokemon\back02.png",
        r".\assets\pokemon\back03.png",
        r".\assets\pokemon\back04.png",
        r".\assets\pokemon\back05.png",
        r".\assets\pokemon\back06.png",
        r".\assets\pokemon\back07.png",
        r".\assets\pokemon\back08.png",
        r".\assets\pokemon\back09.png",
        r".\assets\pokemon\back10.png",
        r".\assets\pokemon\back11.png",
        r".\assets\pokemon\back12.png",
        r".\assets\pokemon\back13.png",
        r".\assets\pokemon\back14.png",
        r".\assets\pokemon\back15.png",
        r".\assets\pokemon\back16.png",
        r".\assets\pokemon\back17.png",
        r".\assets\pokemon\back18.png",
    ]
    bag = r".\assets\items\bag.png"
    items = [
        r".\assets\items\pokeball.png",
        r".\assets\items\posion.png",
    ]
    monster = r".\assets\npc\monster\1.png"
    boss = r".\assets\npc\boss.png"
    npcTrainer1 = r".\assets\npc\npcTrainer1.png"
    npcTrainer2 = r".\assets\npc\npcTrainer2.png"
    npcTrainer3 = r".\assets\npc\npcTrainer3.png"
    healer = r".\assets\npc\healer.png"
    trader = r".\assets\npc\trader.png"

    wildTiles = [
        r".\assets\tiles\wild1.png", 
        r".\assets\tiles\wild2.png", 
        r".\assets\tiles\wild3.png", 
        r".\assets\tiles\wild4.png", 
    ]
    
    hospitalTiles = r".\assets\tiles\hospitalTile.png"
    gymTiles = r".\assets\tiles\gymTile.png"
    shopTiles = r".\assets\tiles\shopTile.png"

    cityTiles = [
        r".\assets\tiles\city1.png", 
        r".\assets\tiles\city2.png", 
        r".\assets\tiles\city3.png", 
        r".\assets\tiles\city4.png", 
    ]

    cityWall = r".\assets\tiles\cityWall.png"

    bossTiles = [
        r".\assets\tiles\boss1.png", 
        r".\assets\tiles\boss2.png", 
        r".\assets\tiles\boss3.png", 
        r".\assets\tiles\boss4.png", 
        r".\assets\tiles\boss5.png", 
        r".\assets\tiles\boss6.png", 
    ]

    bossWall = r".\assets\tiles\bossWall.png"
    portal = r".\assets\background\portal.png"
    invisibleWall = r".\assets\tiles\invisibleWall.png"
    hospital = r".\assets\buildings\hospital.png"
    gym = r".\assets\buildings\gym.png"
    shop = r".\assets\buildings\shop.png"
    citystation = r".\assets\buildings\citystation.png"
    cityroad = r".\assets\buildings\road.png"
    wildstation = r".\assets\buildings\wildstation.png"
    tree = r".\assets\tiles\tree.png"
    wildtree = r".\assets\tiles\wildtree.png"
    wildgrass = r".\assets\tiles\wildgrass.png"
    none = r".\assets\tiles\none.png"
    hospitalwall = r".\assets\buildings\hospitalwall.png"
    hospitaldoor = r".\assets\buildings\hospitaldoor.png"
    gymwall = r".\assets\buildings\gymwall.png"
    redwall = r".\assets\tiles\redwall.png"
    gymstone = r".\assets\buildings\gymstone.png"
    gymbg = r".\assets\buildings\gymbg.png"
    shopwall = r".\assets\buildings\shopwall.png"
    shopshelf1 = r".\assets\buildings\shopshelf1.png"
    shopshelf2 = r".\assets\buildings\shopshelf2.png"
    heal = r".\assets\background\heal.png"

    bgm = [r".\assets\bgm\city.mp3",
           r".\assets\bgm\wild.mp3",
           r".\assets\bgm\boss.mp3",
           r".\assets\bgm\shop.mp3",
           r".\assets\bgm\hospital.mp3",
           r".\assets\bgm\gym.mp3",
           r".\assets\bgm\end.mp3"
           ]

class GameState(Enum):
    MAIN_MENU = 1
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_CITY = 6
    GAME_PLAY_GYM = 7
    GAME_PLAY_BOSS = 8
    GAME_PLAY_HOSPITAL = 9
    GAME_PLAY_WILD = 10
    GAME_PLAY_SHOP = 11
    GAME_PLAY_ORIGIN =12
    END_GAME = 13

class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_SWITCH = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5
    EVENT_SUBMENU = pygame.USEREVENT + 6
    EVENT_ENDGAME = pygame.USEREVENT + 7

class PortalSettings:
    portalWidth = 40
    portalHeight = 40
    portalCD = 30
    Type = [
        [18 ,6 ,GameState.GAME_PLAY_HOSPITAL, 16, 11],#CITY TO HOS
        [16 ,12 ,GameState.GAME_PLAY_CITY, 9, 3],#HOS TO CITY
        [28 ,6 ,GameState.GAME_PLAY_GYM, 15, 16],#CITY TO GYM
        [15 ,16 ,GameState.GAME_PLAY_CITY, 14, 3],#GYM TO CITY
        [42, 17, GameState.GAME_PLAY_WILD, 10, 10],#CITY TO WILD
        [10, 10 ,GameState.GAME_PLAY_CITY, 25, 9],#WILD TO CITY
        [8, 6, GameState.GAME_PLAY_SHOP, 15, 16],#CITY TO SHOP
        [15, 16, GameState.GAME_PLAY_CITY, 4, 3]#SHOP TO CITY
    ]


typeTable = [[1, 1, 1, 1, 1, 0.5, 1, 0, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [2, 1, 0.5, 0.5, 1, 2, 0.5, 0, 2, 1, 1, 1, 1, 0.5, 2, 1, 2, 0.5],
             [1, 2, 1, 1, 1, 0.5, 2, 1, 0.5, 1, 1, 2, 0.5, 1, 1, 1, 1, 1],
             [1, 1, 1, 0.5, 0.5, 0.5, 1, 0.5, 0, 1, 1, 2, 1, 1, 1, 1, 1, 2],
             [1, 1, 0, 2, 1, 2, 0.5, 1, 2, 2, 1, 0.5, 2, 1, 1, 1, 1, 1],
             [1, 0.5, 2, 1, 0.5, 1, 2, 1, 0.5, 2, 1, 1, 1, 1, 2, 1, 1, 1],
             [1, 0.5, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 0.5, 1, 2, 1, 2, 1, 1, 2, 0.5],
             [0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 0.5, 1],
             [1, 1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 0.5, 1, 0.5, 1, 2, 1, 1, 2],
             [1, 1, 1, 1, 1, 0.5, 2, 1, 2, 0.5, 0.5, 2, 1, 1, 2, 0.5, 1, 1],
             [1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 0.5, 0.5, 1, 1, 1, 0.5, 1, 1],
             [1, 1, 0.5, 0.5, 2, 2, 0.5, 1, 0.5, 0.5, 2, 0.5, 1, 1, 1, 0.5, 1, 1],
             [1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 2, 0.5, 0.5, 1, 1, 0.5, 1, 1],
             [1, 2, 1, 2, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 1, 0, 1],
             [1, 1, 2, 1, 2, 1, 1, 1, 0.5, 0.5, 0.5, 2, 1, 1, 0.5, 2, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1, 1, 2, 1, 0],
             [1, 0.5, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 0.5, 0.5],
             [1, 2, 1, 0.5, 1, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 1, 2, 2, 1]] #Table[i][j] i Atk j Def

natureList = ["Hardy", "Lonely", "Adamant", "Naughty", "Brave",
              "Bold", "Docile", "Impish", "Lax", "Relaxed",
              "Modest", "Mild", "Bashful", "Rash", "Quiet",
              "Calm", "Gentle", "Careful", "Quirky", "Sassy",
              "Timid", "Hasty", "Jolly", "Naive", "Serious"]
natureTable = {}
for i in range(5):
    for j in range(5):
        li = [0 for _ in range(5)]
        li[i] += 0.1
        li[j] -= 0.1
        natureTable[natureList[(i * 5) + j]] = (li[0], li[1], li[2], li[3], li[4])

expList = [5 * _ for _ in range(101)]
typeList = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel",
            "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]

class Types:
    NORMAL = 0
    FIGHTING = 1
    FLYING = 2
    POISON = 3
    GROUND = 4
    ROCK = 5
    BUG = 6
    GHOST = 7
    STEEL = 8
    FIRE = 9
    WATER = 10
    GRASS = 11
    ELECTRIC = 12
    PSYCHIC = 13
    ICE = 14
    DRAGON = 15
    DARK = 16
    FAIRY = 17

class ItemID:
    pokeBall = 0
    posion = 1

itemCost = {
    ItemID.pokeBall :200,
    ItemID.posion   :300,
}
itemList = {
    "Poke Ball  ":"$ 200",
    "Posion     ":"$ 300",
    "Back":""
}

itemNameList = ["Poke Ball", "Posion"]
itemDescription = [
    "A prop for capturing wild Pokemon",
    "Heal 20 HP to Pokemon",
]

class StatID:
    HP = 0  # Health
    Atk = 1 # Attack
    Def = 2 # Defense
    SpA = 3 # Special Attack
    SpD = 4 # Special Defense
    Spd = 5 # Speed
    Acc = 6 # Accuracy

class InfoID:
    name = 0
    type = 1
    nature = 2
    level = 3
    exp = 4
    HP = 5
    Atk = 6
    Def = 7
    SpA = 8
    SpD = 9
    Spd = 10

class MoveCategory(Enum):
    PHYSICAL = 1
    SPECIAL = 2
    STATUS = 3

