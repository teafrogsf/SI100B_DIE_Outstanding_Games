# -*- coding:utf-8 -*-

from enum import Enum
import pygame

class WindowSettings:
    name = "Gennki Impact"
    width = 1353
    height = 779
    outdoorScale = 1.5  # A necessary scale to allow camera movement in outdoor scenes


class MapSettings:
    MAX_SIDE_LENGTH = 41
    MAX_MAP_LENGTH = [5, 7, 7]
    ROOM_COUNT = [7, 13, 11]
    MAX_TYPE_COUNT = 7  # Origin 5
    ROOM_LENGTH = [17, 17, 17, 17, 17, 17, 17]  # Origin [17, 17, 19, 19, 21, 23]
    ROOM_OBSTACLES = [
        [
            [(-1, (0, 5)), (-1, (0, 11)), (-1, (5, 0)), (-1, (11, 0)), (-1, (16, 5)), (-1, (16, 11)), (-1, (5, 16)),
             (-1, (11, 16)),
             (-3, (2, 2)), (-4, (2, 3)), (-4, (2, 4)), (-4, (2, 5)), (-4, (3, 2)), (-4, (3, 3)), (-4, (3, 4)),
             (-3, (3, 5)), (-4, (4, 5)), (-4, (4, 4)), (-4, (4, 3)), (-4, (4, 2)), (-4, (5, 2)), (-2, (5, 3)),
             (-4, (5, 4)), (-4, (5, 5)),
             (-4, (5, 7)), (-4, (5, 8)), (-4, (5, 9)), (-3, (5, 10)), (-4, (5, 11)), (-4, (5, 12)), (-4, (3, 10)),
             (-2, (3, 11)), (-4, (3, 12)), (-4, (4, 10)), (-4, (4, 11)), (-4, (4, 12)), (-4, (6, 7)), (-4, (6, 8)),
             (-4, (6, 9)), (-4, (6, 10)), (-4, (6, 11)), (-4, (6, 12)),
             (-3, (11, 12)), (-4, (11, 13)), (-4, (11, 14)), (-4, (11, 15)), (-3, (12, 12)), (-4, (12, 13)),
             (-4, (12, 14)), (-4, (12, 15)),
             (-4, (10, 3)), (-4, (10, 4)), (-4, (10, 5)), (-4, (10, 6)), (-4, (11, 3)), (-2, (11, 4)), (-4, (11, 5)),
             (-4, (11, 6)), (-4, (12, 3)), (-4, (12, 4)), (-2, (12, 5)), (-4, (12, 6)), (-4, (13, 3)), (-4, (13, 4)),
             (-4, (13, 5)), (-2, (13, 6)), (-4, (14, 3)), (-4, (14, 4)), (-4, (14, 5)), (-4, (14, 6)),
             ],

            [(-2, (5, 0)), (-2, (5, 1)), (-2, (5, 2)), (-2, (6, 3)), (-2, (7, 4)), (-2, (8, 5)), (-2, (9, 6)),
             (-2, (10, 7)), (-2, (11, 8)), (-2, (12, 9)),
             (-1, (16, 0)), (-1, (15, 1)), (-1, (14, 2)), (-4, (13, 3)), (-4, (12, 4)), (-1, (0, 16)), (-1, (1, 15)),
             (-1, (2, 14)), (-4, (3, 13)), (-4, (4, 12)),
             (-2, (11, 16)), (-2, (11, 15)), (-2, (11, 14)), (-2, (10, 13)), (-2, (9, 12)), (-2, (8, 11)),
             (-2, (7, 10)), (-2, (6, 9)), (-2, (5, 8)), (-2, (4, 7)),

             ],

            [(-1, (0, 5)), (-1, (0, 11)), (-1, (5, 0)), (-1, (11, 0)), (-1, (16, 5)), (-1, (16, 11)), (-1, (5, 16)),
             (-1, (11, 16)),
             (-2, (3, 3)), (-2, (3, 4)), (-2, (3, 5)), (-2, (3, 6)), (-2, (4, 3)), (-2, (5, 3)), (-2, (6, 3)),
             (-2, (10, 3)), (-2, (11, 3)), (-2, (12, 3)), (-2, (13, 3)), (-2, (13, 4)), (-2, (13, 5)), (-2, (13, 6)),
             (-2, (3, 10)), (-2, (3, 11)), (-2, (3, 12)), (-2, (3, 13)), (-2, (4, 13)), (-2, (5, 13)), (-2, (6, 13)),
             (-2, (13, 10)), (-2, (13, 11)), (-2, (13, 12)), (-2, (13, 13)), (-2, (12, 13)), (-2, (11, 13)),
             (-2, (10, 13)),
             (-4, (6, 6)), (-4, (6, 7)), (-4, (6, 8)), (-4, (6, 9)), (-4, (6, 10)), (-4, (7, 6)), (-4, (7, 7)),
             (-4, (7, 8)), (-4, (7, 9)), (-4, (7, 10)), (-4, (8, 6)), (-4, (8, 7)), (-4, (8, 8)), (-4, (8, 9)),
             (-4, (8, 10)), (-4, (9, 6)), (-4, (9, 7)), (-4, (9, 8)), (-4, (9, 9)), (-4, (9, 10)), (-4, (10, 6)),
             (-4, (10, 7)), (-4, (10, 8)), (-4, (10, 9)), (-4, (10, 10))
             ],

            [(-2, (4, 9)), (-2, (4, 6)), (-2, (4, 7)), (-2, (4, 8)), (-2, (5, 9)), (-2, (5, 6)), (-2, (5, 7)),
             (-2, (5, 8)), (-2, (6, 9)), (-2, (6, 6)), (-2, (6, 7)), (-2, (6, 8)), (-2, (10, 9)), (-2, (10, 6)),
             (-2, (10, 7)), (-2, (10, 8)), (-2, (11, 9)), (-2, (11, 6)), (-2, (11, 7)), (-2, (11, 8)), (-2, (12, 9)),
             (-2, (12, 6)), (-2, (12, 7)), (-2, (12, 8)),
             (-4, (3, 5)), (-4, (3, 6)), (-4, (3, 7)), (-4, (3, 8)), (-4, (3, 9)), (-4, (3, 10)), (-4, (4, 5)),
             (-4, (4, 4)), (-4, (4, 10)), (-4, (4, 11)), (-4, (5, 5)), (-4, (5, 4)), (-4, (6, 13)), (-4, (5, 10)),
             (-4, (5, 11)), (-4, (5, 12)), (-4, (6, 3)), (-4, (6, 5)), (-4, (6, 4)), (-4, (6, 12)), (-4, (6, 10)),
             (-4, (6, 11)),
             (-4, (7, 3)), (-4, (7, 4)), (-4, (7, 5)), (-4, (7, 6)), (-4, (7, 7)), (-4, (7, 8)), (-4, (7, 9)),
             (-4, (7, 10)), (-4, (7, 11)), (-4, (7, 12)), (-4, (8, 4)), (-4, (8, 5)), (-4, (8, 6)), (-4, (8, 7)),
             (-4, (8, 8)), (-4, (8, 9)), (-4, (8, 10)), (-4, (8, 11)), (-4, (8, 12)), (-4, (8, 13)), (-4, (9, 3)),
             (-4, (9, 4)), (-4, (9, 5)), (-4, (9, 6)), (-4, (9, 7)), (-4, (9, 8)), (-4, (9, 9)), (-4, (9, 10)),
             (-4, (9, 11)), (-4, (9, 12)),
             (-4, (13, 5)), (-4, (13, 6)), (-4, (13, 7)), (-4, (13, 8)), (-4, (13, 9)), (-4, (13, 10)), (-4, (12, 5)),
             (-4, (12, 4)), (-4, (12, 10)), (-4, (12, 11)), (-4, (11, 5)), (-4, (11, 4)), (-4, (10, 13)),
             (-4, (11, 10)), (-4, (11, 11)), (-4, (11, 12)), (-4, (10, 3)), (-4, (10, 5)), (-4, (10, 4)),
             (-4, (10, 12)), (-4, (10, 10)), (-4, (10, 11)),
             ],

            [(-1, (0, 5)), (-1, (0, 11)), (-1, (5, 0)), (-1, (11, 0)), (-1, (16, 5)), (-1, (16, 11)), (-1, (5, 16)),
             (-1, (11, 16)),
             (-4, (4, 4)), (-4, (4, 3)), (-3, (5, 4)), (-3, (6, 4)), (-3, (7, 4)), (-3, (8, 4)), (-3, (9, 4)),
             (-2, (7, 5)), (-2, (8, 5)), (-2, (9, 5)),
             (-2, (3, 12)), (-2, (3, 13)), (-2, (3, 14)), (-2, (4, 12)), (-2, (4, 13)), (-2, (4, 14)), (-4, (5, 12)),
             (-4, (5, 13)), (-4, (5, 14)),
             (-2, (12, 9)), (-2, (12, 10)), (-2, (12, 11)), (-2, (12, 12))
             ],

            [(-1, (0, 5)), (-1, (0, 11)), (-1, (16, 5)), (-1, (16, 11)),
             (-2, (11, 0)), (-2, (11, 1)), (-2, (11, 2)), (-2, (11, 3)), (-2, (11, 4)), (-2, (10, 4)), (-2, (9, 4)),
             (-2, (8, 4)), (-2, (7, 4)), (-2, (6, 4)), (-2, (5, 4)), (-2, (4, 4)), (-2, (4, 5)), (-2, (4, 6)),
             (-2, (4, 7)), (-2, (4, 8)),
             (-2, (5, 16)), (-2, (5, 15)), (-2, (5, 14)), (-2, (5, 13)), (-2, (5, 12)), (-2, (6, 12)), (-2, (7, 12)),
             (-2, (8, 12)), (-2, (9, 12)), (-2, (10, 12)), (-2, (11, 12)), (-2, (11, 11)), (-2, (11, 10)),
             (-2, (11, 9)), (-2, (11, 8)),
             ],

            [(-2, (3, 3)), (-2, (3, 4)), (-2, (3, 5)), (-2, (3, 6)), (-2, (4, 3)), (-2, (4, 4)), (-2, (4, 5)),
             (-2, (4, 6)),
             (-2, (10, 11)), (-2, (10, 12)), (-2, (11, 11)), (-2, (11, 12)), (-2, (12, 9)), (-2, (12, 10)),
             (-2, (12, 11)), (-2, (12, 12)), (-2, (13, 9)), (-2, (13, 10)), (-2, (13, 11)), (-2, (13, 12)),
             (-2, (9, 5)), (-2, (10, 5)), (-2, (11, 5)), (-2, (12, 5)), (-2, (13, 5)),
             (-4, (6, 9)), (-4, (6, 10)), (-4, (6, 11)), (-4, (7, 11)), (-4, (14, 4)), (-4, (15, 3)), (-4, (15, 4)),
             (-4, (15, 15)), (-4, (15, 16)), (-4, (16, 15)), (-4, (16, 16)),
             (-1, (0, 5)), (-1, (0, 11)), (-1, (5, 0)), (-1, (11, 0)), (-1, (16, 5)), (-1, (16, 11)), (-1, (5, 16)),
             (-1, (11, 16)),
             (-3, (11, 2)), (-3, (3, 10)), (-3, (4, 14))
             ],

        ]
    ]
    ROOM_MONSTERS=[
        [
            [2,(1,1)],[2,(7,4)],[5,(9,7)],[3,(2,15)],[1,(3,8)],[1,(9,12)],[3,(14,2)],[1,(13,10)],[4,(15,15)]
        ],[
            [5,(8,8)],[1,(3,6)],[2,(2,11)],[1,(9,14)],[3,(2,15)],[4,(3,1)],[1,(7,3)],[2,(12,1)],[1,(13,5)],[4,(15,15)],[2,(13,10)]
        ],[
            [1,(1,1)],[1,(15,15)],[2,(1,15)],[2,(15,1)],[3,(4,4)],[3,(12,12)],[4,(4,12)],[5,(12,4)]
        ],[
            [5,(1,1)],[4,(15,15)],[3,(1,15)],[3,(15,1)],[1,(2,6)],[2,(3,12)],[1,(5,14)],[1,(11,14)],[1,(14,9)],[2,(11,3)],[2,(13,12)]
        ],[
            [5,(8,8)],[2,(3,2)],[1,(4,7)],[3,(2,15)],[4,(14,2)],[1,(12,6)],[2,(12,14)]
        ],[
            [5,(8,8)],[1,(10,3)],[2,(4,2)],[3,(3,15)],[1,(3,7)],[1,(13,9)],[4,(15,2)],[2,(14,15)],[1,(9,13)]
        ],[
            [5,(10,9)],[3,(2,14)],[2,(4,2)],[1,(3,7)],[2,(5,12)],[4,(6,5)],[1,(10,4)],[3,(1,16)],[1,(15,9)],[2,(13,14)]
        ]
    ]
    SPAWN_ROOM_LENGTH = 15
    BOSS_ROOM_LENGTH = 25


class GameState(Enum):
    MAIN_MENU = 1
    GAME_STATE = 10
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_LEVEL0 = 6
    GAME_PLAY_LEVEL1 = 7
    GAME_PLAY_LEVEL2 = 8
    GAME_PLAY_BOSS = 9
    Game_SWITCH = 0


class SceneSettings:
    tileXnum = 33
    tileYnum = 19
    tileWidth = 41
    tileHeight = 41
    obstacleDensity = 0.1


class ObstacleSettings:
    obstacleWidth = 41
    obstacleHeight = 41


class PortalImagePath:
    portal = r".\Portal_Picture\portal.png"


class PortalSettings:
    portalWidth = 320
    portalHeight = 320


class MenuImagePaths:
    menu = r".\Portal_Picture\menu.png"


class MenuSettings:
    textSize = 36
    blinkInterval = 100


class MapImagePaths:
    GROUNDS = [
        [
            r".\assets\mapimages\level1\ground1.jpg",
            r".\assets\mapimages\level1\ground2.jpg",
            r".\assets\mapimages\level1\ground3.jpg",
            r".\assets\mapimages\level1\ground4.jpg",
            r".\assets\mapimages\level1\ground5.jpg",
            r".\assets\mapimages\level1\ground6.jpg"
        ], [
            r".\assets\mapimages\level2\ground1.png",
            r".\assets\mapimages\level2\ground2.png",
            r".\assets\mapimages\level2\ground3.png",
            r".\assets\mapimages\level2\ground4.png",
            r".\assets\mapimages\level2\ground5.png",
            r".\assets\mapimages\level2\ground6.png"
        ], [
            r".\assets\mapimages\level3\ground1.png",
            r".\assets\mapimages\level3\ground2.png",
            r".\assets\mapimages\level3\ground3.png",
            r".\assets\mapimages\level3\ground4.png",
            r".\assets\mapimages\level3\ground5.png",
            r".\assets\mapimages\level3\ground6.png"
        ]
    ]
    VOID = r".\assets\mapimages\level1\void.jpg"
    GATE = r".\assets\mapimages\level1\gate.png"
    ACTIVATED_GATE=r".\assets\mapimages\ActivatedGate.png"
    WALLS = [
        [
            r".\assets\mapimages\level1\wall1.png",
            r".\assets\mapimages\level1\wall2.png"
        ], [
            r".\assets\mapimages\level2\wall1.png",
            r".\assets\mapimages\level2\wall2.png"
        ], [
            r".\assets\mapimages\level3\wall1.png",
            r".\assets\mapimages\level3\wall2.png"
        ]
    ]
    BORDER_OBSTACLE = r".\assets\mapimages\BorderWall.png"
    OBSTACLES = [
        [
            r".\assets\mapimages\level1\obstacle0.png",
            r".\assets\mapimages\level1\obstacle1.png",
            r".\assets\mapimages\level1\obstacle2.png",
            r".\assets\mapimages\level1\obstacle3.png"
        ], [
            r".\assets\mapimages\level2\obstacle0.png",
            r".\assets\mapimages\level2\obstacle1.png",
            r".\assets\mapimages\level2\obstacle2.png",
            r".\assets\mapimages\level2\obstacle3.png"
        ], [
            r".\assets\mapimages\level3\obstacle0.png",
            r".\assets\mapimages\level3\obstacle1.png",
            r".\assets\mapimages\level3\obstacle2.png",
            r".\assets\mapimages\level3\obstacle3.png"
        ]
    ]


class UISettings:
    ui_border_color = "#111111"
    bar_height = 30
    blood_bar_width = 100
    mana_bar_width = 100
    item_box_size = 100
    ui_font = "./Images/font/joystix.ttf"
    ui_font_size = 18

    blood_color = "red"
    mana_color = "blue"
    ui_border_color_active = "gold"

    ui_bg_color = "#222222"
    text_color = "#EEEEEE"


class PlayerSettings:
    stats = {'HP': 200, 'MP': 600, 'speed': 0.3}
    playerSpeed = stats["speed"]
    playerHP = stats["HP"]
    playerMP = stats["MP"]
    playerWidth = 60
    playerHeight = 55
    playerPocketMoney = 10000


class PlayerImagePaths:
    PLAYER = [
        r".\assets\player\1.png",
        r".\assets\player\2.png",
        r".\assets\player\3.png",
        r".\assets\player\4.png"
    ]

class BossSettings:
    bossCount=3
    bossWidth=300
    bossHeight=300
    actionTime=30
    bossAttackDesire=[10000 for _ in range(3)]
    bossName=["0","1","2"]
    bossDamage=[3,3,3]
    bossHealth=[100,200,400]
    boss_Gold_Drop=[(30,30),(50,50),(100,100)]
    bossSpeed=[0,0,0]
    attackType=[4,4,4]

class MonsterSettings:
    monsterCount=15
    monsterWidth=50
    monsterHeight=45
    actionTime=80
    monsterAttackDesire=[2000 for _ in range(15)]
    monsterDirection=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]
    monsterName=[
        "Boar","Dire Boar","Goblin Guard","Goblin Priest","Goblin Shaman",
        "Battery","Knight(close)","Knight(Gun)","Slime","Wizard",
        "Alien","Battery","Tentacle","Varkolyn Guard(close)","Varkolyn Guard(Gun)"
    ]
    monsterDamage=[
        1,1,1,2,1,
        1,1,1,1,2,
        1,2,2,2,2
    ]
    monsterHealth=[
        5,5,8,15,20,
        10,10,15,10,30,
        15,20,30,40,50
    ]
    monster_Gold_drop=[
        (0,2),(0,2),(0,2),(3,3),(5,5),
        (0,5),(0,5),(3,5),(0,2),(3,5),
        (0,3),(0,3),(2,4),(0,4),(5,5)
    ]
    monsterSpeed=[
        4,5,3,3,3,
        3,3,3,4,4,
        3,3,3,5,4
    ]
    '''
    Attack Type:
    0 for close combat
    1 for each 1 bullet to ESWN
    2 for each 1 bullet to ESWN,SE,SW,NE,NW
    3 for each 1 bullet to 16 directions
    '''
    attackType=[
        0,0,0,1,2,
        1,0,2,0,3,
        0,2,2,0,3
    ]
    
class MonsterImagePaths:
    BOSS=[
        [
            r".\Images\Monster Image\0Tree\0.png",
            r".\Images\Monster Image\0Tree\1.png",
            r".\Images\Monster Image\0Tree\2.png",
            r".\Images\Monster Image\0Tree\3.png",
            r".\Images\Monster Image\0Tree\4.png",
            r".\Images\Monster Image\0Tree\5.png"
        ],[
            r".\Images\Monster Image\1Grand Knight\0.png",
            r".\Images\Monster Image\1Grand Knight\1.png",
            r".\Images\Monster Image\1Grand Knight\2.png",
            r".\Images\Monster Image\1Grand Knight\3.png",
            r".\Images\Monster Image\1Grand Knight\4.png",
            r".\Images\Monster Image\1Grand Knight\5.png",
            r".\Images\Monster Image\1Grand Knight\6.png",
            r".\Images\Monster Image\1Grand Knight\7.png",
            r".\Images\Monster Image\1Grand Knight\8.png",
            r".\Images\Monster Image\1Grand Knight\9.png"
        ],[
            r".\Images\Monster Image\2Varkolyn Guard Boss\0.png",
            r".\Images\Monster Image\2Varkolyn Guard Boss\1.png",
            r".\Images\Monster Image\2Varkolyn Guard Boss\2.png",
            r".\Images\Monster Image\2Varkolyn Guard Boss\3.png"
        ]
    ]
    MONSTER = [
        [
            r".\Images\Monster Image\0boar\0.png",
            r".\Images\Monster Image\0boar\1.png",
            r".\Images\Monster Image\0boar\2.png",
            r".\Images\Monster Image\0boar\3.png"
        ],[
            r".\Images\Monster Image\0Dire Boar\0.png",
            r".\Images\Monster Image\0Dire Boar\1.png",
            r".\Images\Monster Image\0Dire Boar\2.png",
            r".\Images\Monster Image\0Dire Boar\3.png"
        ],[
            r".\Images\Monster Image\0Goblin Guard\0.png",
            r".\Images\Monster Image\0Goblin Guard\1.png",
            r".\Images\Monster Image\0Goblin Guard\2.png",
            r".\Images\Monster Image\0Goblin Guard\3.png",
            r".\Images\Monster Image\0Goblin Guard\4.png"
        ],[
            r".\Images\Monster Image\0Goblin Priest\0.png",
            r".\Images\Monster Image\0Goblin Priest\1.png",
            r".\Images\Monster Image\0Goblin Priest\2.png",
            r".\Images\Monster Image\0Goblin Priest\3.png"
        ],[
            r".\Images\Monster Image\0Goblin Shaman\0.png",
            r".\Images\Monster Image\0Goblin Shaman\1.png",
            r".\Images\Monster Image\0Goblin Shaman\2.png",
            r".\Images\Monster Image\0Goblin Shaman\3.png"
        ],[
            r".\Images\Monster Image\1Battery\0.png",
            r".\Images\Monster Image\1Battery\1.png",
            r".\Images\Monster Image\1Battery\2.png"
        ],[
            r".\Images\Monster Image\1Knight\0.png",
            r".\Images\Monster Image\1Knight\1.png",
            r".\Images\Monster Image\1Knight\2.png",
            r".\Images\Monster Image\1Knight\3.png",
            r".\Images\Monster Image\1Knight\4.png",
            r".\Images\Monster Image\1Knight\5.png"
        ],[
            r".\Images\Monster Image\1Knight\0.png",
            r".\Images\Monster Image\1Knight\1.png",
            r".\Images\Monster Image\1Knight\2.png",
            r".\Images\Monster Image\1Knight\3.png",
            r".\Images\Monster Image\1Knight\4.png",
            r".\Images\Monster Image\1Knight\5.png"
        ],[
            r".\Images\Monster Image\1Slime\0.png",
            r".\Images\Monster Image\1Slime\1.png",
            r".\Images\Monster Image\1Slime\2.png",
            r".\Images\Monster Image\1Slime\3.png",
            r".\Images\Monster Image\1Slime\4.png"
        ],[
            r".\Images\Monster Image\1Wizard\0.png",
            r".\Images\Monster Image\1Wizard\1.png",
            r".\Images\Monster Image\1Wizard\2.png",
            r".\Images\Monster Image\1Wizard\3.png",
            r".\Images\Monster Image\1Wizard\4.png"
        ],[
            r".\Images\Monster Image\2Alien\0.png",
            r".\Images\Monster Image\2Alien\1.png",
            r".\Images\Monster Image\2Alien\2.png",
            r".\Images\Monster Image\2Alien\3.png",
            r".\Images\Monster Image\2Alien\4.png",
            r".\Images\Monster Image\2Alien\5.png",
            r".\Images\Monster Image\2Alien\6.png",
            r".\Images\Monster Image\2Alien\7.png"
        ],[
            r".\Images\Monster Image\2Battery\0.png",
            r".\Images\Monster Image\2Battery\1.png",
            r".\Images\Monster Image\2Battery\2.png"
        ],[
            r".\Images\Monster Image\2Tentacle\0.png",
            r".\Images\Monster Image\2Tentacle\1.png",
            r".\Images\Monster Image\2Tentacle\2.png",
            r".\Images\Monster Image\2Tentacle\3.png",
            r".\Images\Monster Image\2Tentacle\4.png",
            r".\Images\Monster Image\2Tentacle\5.png",
            r".\Images\Monster Image\2Tentacle\6.png",
            r".\Images\Monster Image\2Tentacle\7.png",
            r".\Images\Monster Image\2Tentacle\8.png",
            r".\Images\Monster Image\2Tentacle\9.png",
            r".\Images\Monster Image\2Tentacle\10.png",
            r".\Images\Monster Image\2Tentacle\11.png",
            r".\Images\Monster Image\2Tentacle\12.png"
        ],[
            r".\Images\Monster Image\2Varkolyn Guard\0.png",
            r".\Images\Monster Image\2Varkolyn Guard\1.png",
            r".\Images\Monster Image\2Varkolyn Guard\2.png",
            r".\Images\Monster Image\2Varkolyn Guard\3.png",
            r".\Images\Monster Image\2Varkolyn Guard\4.png",
            r".\Images\Monster Image\2Varkolyn Guard\5.png",
            r".\Images\Monster Image\2Varkolyn Guard\6.png"
        ],[
            r".\Images\Monster Image\2Varkolyn Guard\0.png",
            r".\Images\Monster Image\2Varkolyn Guard\1.png",
            r".\Images\Monster Image\2Varkolyn Guard\2.png",
            r".\Images\Monster Image\2Varkolyn Guard\3.png",
            r".\Images\Monster Image\2Varkolyn Guard\4.png",
            r".\Images\Monster Image\2Varkolyn Guard\5.png",
            r".\Images\Monster Image\2Varkolyn Guard\6.png"
        ]
    ]

class WeaponsSettings:
    weaponsName = ["Shield", "Sword", "Sniper Rifle", "shotgun", "Automatic rifles", "spear"]
    weaponsDamage = [[0, 4, 15, 6, 5, 3],[0, 8, 12, 10, 4, 6]]
    weaponImages=[
        r".\Images\Weapon Image\0.盾牌.png",
        r".\Images\Weapon Image\1.剑.png",
        r".\Images\Weapon Image\2.狙击枪.png",
        r".\Images\Weapon Image\3.霰弹枪.png",
        r".\Images\Weapon Image\4.自动步枪.png",
        r".\Images\Weapon Image\5.长矛.png"
    ]
    attackSpeed=[1,40,40,10,10,40]
    

class BulletSettings:
    bulletImage=r".\Images\Weapon Image\Bullet.png"
    bulletWidth=20
    bulletHeight=20
    bulletSpeed=30
    weaponsDamage_white = [0, 4, 15, 6, 5, 3]
    weaponsDamage_green = [0, 8, 30, 10, 15, 6]
    weaponsDollar_costed = [15, 6, 12, 15, 12, 13, 30, 12, 24, 30, 24, 26, 60, 24, 48, 60, 48, 52]


class WeaponsImagePaths:
    WEAPON = [
        r".\Images\Weapon Image\0.盾牌.png",
        r".\Images\Weapon Image\1.剑.png",
        r".\Images\Weapon Image\2.狙击枪.png",
        r".\Images\Weapon Image\3.霰弹枪.png",
        r".\Images\Weapon Image\4.自动步枪.png",
        r".\Images\Weapon Image\5.长矛.png",
        r".\Images\Weapon Image\子弹特效.png"
    ]

class SupplySettings:
    Image = [
        r".\Images\Supply Image\0.png",
        r".\Images\Supply Image\1.png",
        r".\Images\Supply Image\2.png"
    ]
    width=20
    height=30


class NPCSettings:
    npcWidth = 60
    npcHeight = 55
    talkCD = 30


class NPCImagePaths:
    NPC = [
        r".\Images\NPC Image\0.png",
        r".\Images\NPC Image\1.png"
    ]


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


class ShopSettings:
    boxWidth = WindowSettings.width*3//4
    boxHeight = WindowSettings.height*2//3
    boxStartX = WindowSettings.width//8   # Coordinate X of the box
    boxStartY = WindowSettings.height//6  # Coordinate Y of the box

    textSize = 56 # Default font size
    textStartX = boxStartX + 10         # Coordinate X of the first line of dialog
    textStartY = boxStartY + 25    # Coordinate Y of the first line of dialog

    # Merchant 0: 0:HP Portion; 1:MP Portion
    # Merchant 1: -1:Level UP; 2: Weapon_AWP
    goodList=[[[(0,40),(1,20),(-1,-20),(2,-2000)],[(0,50),(1,30),(-1,-30),(2,-50)],[(0,60),(1,40),(-1,-40),(2,-50)]],[[(3,-1)],[(3,-1)],[(3,-1)]]]
    operateCD=100
    goodDict={0:"HP Portion",1:"MP Portion",-1:"Level up",2:"Sniper Rifle",3:"Gamble"}


class MenuImagePaths:
    menu = r".\Images\PortalImage\menu.png"


class PortalSettings:
    portalWidth = 320
    portalHeight = 320


class PortalImagePath:
    portal = r".\Images\PortalImage\portal.png"

class Events:
    playerStop=pygame.USEREVENT+0
    monsterStop=pygame.USEREVENT+1
    monsterAttack=pygame.USEREVENT+2
    bulletEliminate=pygame.USEREVENT+3
    obstacleDestruction=pygame.USEREVENT+4
    playerHit=pygame.USEREVENT+5
    monsterHit=pygame.USEREVENT+6
    playerShoot=pygame.USEREVENT+7
    levelChange=pygame.USEREVENT+8
    monsterDeath=pygame.USEREVENT+9
    monsterGenerateBullet=pygame.USEREVENT+10
    hpPortionUse=pygame.USEREVENT+11
    mpPortionUse=pygame.USEREVENT+12
    shopActivate=pygame.USEREVENT+13
    shopAction=pygame.USEREVENT+14

class BackgroundMusic:
    levelBGM=[
        r".\music\level0.mp3",
        r".\music\level1.mp3",
        r".\music\level2.mp3"
    ]
    bossBGM=r".\music\boss.mp3"

class PortionSettings:
    hpPortion=5
    mpPortion=20
    useCD=40