# -*- coding:utf-8 -*-

from enum import Enum
import pygame


class WindowSettings:
    name = "O.o"
    width = 1280
    height = 720
    outdoorScale = 1.5  # A necessary scale to allow camera movement in outdoor scenes
    fps = 30


class SceneSettings:
    tileXnum = 48  # 64
    tileYnum = 27  # 36
    tileWidth = tileHeight = 40
    obstacleDensity = 0.1


class ManuSettings:
    textSize = 30
    blinkInterval = 30


class PlayerSettings:
    # Initial Player Settings
    playerSpeed = 5
    playerWidth = 80
    playerHeight = 70
    playerHP = 20
    playerAttack = 5
    playerDefence = 1
    playerMoney = 30
    heartWidth = heartHeight = 50
    heartGap = 50
    fireWidth = fireHeight = 50
    cardswidth = 90
    cardsheight = 126
    backwidth = 90
    backheight = 126


class PlayerDirection(Enum):
    Right = 2
    Left = 1
    Up = 3
    Down = 0


class NPCSettings:
    npcSpeed = 1
    npcWidth = 60
    npcHeight = 60
    talkCD = 4 * WindowSettings.fps  # 4秒


class NPCType(Enum):
    DIALOG = 1
    MONSTER = 2
    SHOP = 3


class Action(Enum):
    SITTING = 1
    STANDING = 2
    DIE = 3


class BossSettings:
    width = 300
    height = 300
    coordX = (SceneSettings.tileXnum / 2) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2


class SceneType(Enum):
    CITY = 1
    WILD = 2
    BOSS = 3
    VICTORY = 4
    DEFEAT = 5


class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxStartX = WindowSettings.width // 4  # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20  # Coordinate Y of the box

    textSize = 48  # Default font size
    textStartX = WindowSettings.width // 4 + 10  # Coordinate X of the first line of dialog
    textStartY = WindowSettings.height // 3 * 2 + 30  # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3  # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20


class BattleSettings:
    boxWidth = WindowSettings.width * 3 // 4
    boxHeight = WindowSettings.height * 3 // 4
    boxStartX = WindowSettings.width // 8  # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 48  # Default font size
    textStartX = WindowSettings.width // 4
    textPlayerStartX = boxStartX + 80  # Coordinate X of the first line of dialog
    textMonsterStartX = boxStartX + boxWidth - 130
    textStartY = boxStartY + 30  # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3  # Vertical distance of two lines

    playerWidth = WindowSettings.width // 6
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8 + 150
    playerCoordY = WindowSettings.height // 2

    monsterWidth = WindowSettings.width // 6
    monsterHeight = WindowSettings.height // 3
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 2

    stepSize = 14
    animationFrameCount = 15

    flashWidth = 75
    flashHeight = 200

    specialWidth = 144
    specialHeight = 75


class ShopSettings:
    shopWidth = 180
    shopHeight = 180
    boxWidth = 800
    boxHeight = 250
    boxStartX = WindowSettings.width // 4  # Coordinate X of the box
    boxStartY = WindowSettings.height // 3  # Coordinate Y of the box
    itemWidth = 90
    itemHeight = 120
    itemStartX = boxStartX + 100
    itemStartY = boxStartY + 70
    itemGap = 175

    textSize = 56  # Default font size
    textStartX = boxStartX + 40  # Coordinate X of the first line of dialog
    textStartY = boxStartY + 55  # Coordinate Y of the first line of dialog


class GamePath:
    # Window related path
    menu = r".\assets\background\menu.png"
    victory_menu = r".\assets\background\VICTORY.png"
    defeat_menu = r".\assets\background\DEFEAT.png"
    wild = r".\assets\background\wild.png"
    mapBlock = r".\assets\background\map.png"
    shopBackground = r".\assets\background\shop.png"

    # player/npc related path
    npc = r".\assets\npc\npc.png"
    shop = r".\assets\npc\shop.png"
    shopNpc = r".\assets\npc\shopnpc.png"
    player = [
        [r".\assets\player\11.png",
         r".\assets\player\12.png",
         r".\assets\player\13.png",
         r".\assets\player\14.png",
         r".\assets\player\15.png",
         r".\assets\player\16.png",
         r".\assets\player\17.png",
         r".\assets\player\18.png",
         r".\assets\player\19.png",
         r".\assets\player\110.png"],
        [r".\assets\player\21.png",
         r".\assets\player\22.png",
         r".\assets\player\23.png",
         r".\assets\player\24.png",
         r".\assets\player\25.png",
         r".\assets\player\26.png",
         r".\assets\player\27.png",
         r".\assets\player\28.png",
         r".\assets\player\29.png",
         r".\assets\player\210.png"],
        [r".\assets\player\31.png",
         r".\assets\player\32.png",
         r".\assets\player\33.png",
         r".\assets\player\34.png",
         r".\assets\player\35.png",
         r".\assets\player\36.png",
         r".\assets\player\37.png",
         r".\assets\player\38.png",
         r".\assets\player\39.png",
         r".\assets\player\310.png"],
        [r".\assets\player\41.png",
         r".\assets\player\42.png",
         r".\assets\player\43.png",
         r".\assets\player\44.png",
         r".\assets\player\45.png",
         r".\assets\player\46.png",
         r".\assets\player\47.png",
         r".\assets\player\48.png",
         r".\assets\player\49.png",
         r".\assets\player\410.png"],
    ]

    monster = [[r".\assets\npc\monster\1\1.png",
                r".\assets\npc\monster\1\2.png",
                r".\assets\npc\monster\1\3.png",
                r".\assets\npc\monster\1\4.png",
                r".\assets\npc\monster\1\5.png",
                r".\assets\npc\monster\1\6.png"],
               [r".\assets\npc\monster\2\1.png",
                r".\assets\npc\monster\2\2.png",
                r".\assets\npc\monster\2\3.png",
                r".\assets\npc\monster\2\4.png",
                r".\assets\npc\monster\2\5.png",
                r".\assets\npc\monster\2\6.png"],
               [r".\assets\npc\monster\3\1.png",
                r".\assets\npc\monster\3\2.png",
                r".\assets\npc\monster\3\3.png",
                r".\assets\npc\monster\3\4.png",
                r".\assets\npc\monster\3\5.png",
                r".\assets\npc\monster\3\6.png"]
               ]
    boss = r".\assets\npc\boss.png"

    battleBox = r".\assets\background\battlebox.png"

    player_died = r".\assets\player\DIED.png"
    player_win = r".\assets\player\WIN.png"
    player_HP = r".\assets\player\heart.png"
    player_Attack = r".\assets\player\attack.png"
    player_Defence = r".\assets\player\defence.png"
    player_Money = r".\assets\player\money.png"
    fireImage = [r".\assets\player\fire 1.png",
                 r".\assets\player\fire 2.png",
                 r".\assets\player\fire 3.png",
                 r".\assets\player\fire 4.png",
                 r".\assets\player\fire 5.png"]

    groundTiles = [
        r".\assets\tiles\ground1.jpg",
        r".\assets\tiles\ground2.jpg",
        r".\assets\tiles\ground3.jpg",
        r".\assets\tiles\ground4.jpg",
        r".\assets\tiles\ground5.jpg",
        r".\assets\tiles\ground6.jpg",
    ]

    cityTiles = [
        r".\assets\tiles\city1.jpg",
        r".\assets\tiles\city2.jpg",
        r".\assets\tiles\city3.jpg",
        r".\assets\tiles\city4.jpg",
        r".\assets\tiles\city5.jpg",
        r".\assets\tiles\city6.jpg",
    ]

    cityWall = r".\assets\tiles\cityWall.png"

    bossTiles = [
        r".\assets\tiles\boss1.jpg",
        r".\assets\tiles\boss2.jpg",
        r".\assets\tiles\boss3.jpg",
        r".\assets\tiles\boss4.jpg",
        r".\assets\tiles\boss5.jpg",
        r".\assets\tiles\boss6.jpg",
    ]

    bossWall = r".\assets\tiles\bossWall.png"

    portal = r".\assets\background\portal.png"

    tree = r".\assets\tiles\tree.png"

    bgm = [r".\assets\bgm\city.mp3",
           r".\assets\bgm\wild.mp3",
           r".\assets\bgm\boss.mp3",
           r".\assets\bgm\main menu.mp3",
           r".\assets\bgm\victory.mp3",
           r".\assets\bgm\defeat.mp3",
           ]

    animated_tree = [[r".\assets\tiles\animated_tree\leftbottom1.png",
                      r".\assets\tiles\animated_tree\leftbottom2.png",
                      r".\assets\tiles\animated_tree\leftbottom3.png",
                      r".\assets\tiles\animated_tree\leftbottom4.png",
                      r".\assets\tiles\animated_tree\leftbottom5.png",
                      r".\assets\tiles\animated_tree\leftbottom6.png",
                      r".\assets\tiles\animated_tree\leftbottom7.png",
                      r".\assets\tiles\animated_tree\leftbottom8.png"],
                     [r".\assets\tiles\animated_tree\lefttop1.png",
                      r".\assets\tiles\animated_tree\lefttop2.png",
                      r".\assets\tiles\animated_tree\lefttop3.png",
                      r".\assets\tiles\animated_tree\lefttop4.png",
                      r".\assets\tiles\animated_tree\lefttop5.png",
                      r".\assets\tiles\animated_tree\lefttop6.png",
                      r".\assets\tiles\animated_tree\lefttop7.png",
                      r".\assets\tiles\animated_tree\lefttop8.png"],
                     [r".\assets\tiles\animated_tree\rightbottom1.png",
                      r".\assets\tiles\animated_tree\rightbottom2.png",
                      r".\assets\tiles\animated_tree\rightbottom3.png",
                      r".\assets\tiles\animated_tree\rightbottom4.png",
                      r".\assets\tiles\animated_tree\rightbottom5.png",
                      r".\assets\tiles\animated_tree\rightbottom6.png",
                      r".\assets\tiles\animated_tree\rightbottom7.png",
                      r".\assets\tiles\animated_tree\rightbottom8.png"],
                     [r".\assets\tiles\animated_tree\righttop1.png",
                      r".\assets\tiles\animated_tree\righttop2.png",
                      r".\assets\tiles\animated_tree\righttop3.png",
                      r".\assets\tiles\animated_tree\righttop4.png",
                      r".\assets\tiles\animated_tree\righttop5.png",
                      r".\assets\tiles\animated_tree\righttop6.png",
                      r".\assets\tiles\animated_tree\righttop7.png",
                      r".\assets\tiles\animated_tree\righttop8.png"],
                     ]

    fire = [r".\assets\tiles\fire1.png",
            r".\assets\tiles\fire2.png",
            r".\assets\tiles\fire3.png",
            r".\assets\tiles\fire4.png",
            ]

    shopItem = [r".\assets\shop\shop HP.png",
                r".\assets\shop\shop attack.png",
                r".\assets\shop\shop defence.png",
                r".\assets\shop\shop level.png",
                ]
    shopExit = r".\assets\shop\shop exit.png"
    mouse = r".\assets\shop\mouse.png"

    card_images = [r".\assets\cards\1.png",
                   r".\assets\cards\2.png",
                   r".\assets\cards\3.png",
                   r".\assets\cards\4.png",
                   r".\assets\cards\5.png",
                   r".\assets\cards\6.png",
                   r".\assets\cards\7.png",
                   r".\assets\cards\8.png",
                   r".\assets\cards\9.png",
                   r".\assets\cards\10.png",
                   r".\assets\cards\11.png",
                   r".\assets\cards\12.png",
                   r".\assets\cards\13.png",
                   r".\assets\cards\14.png",
                   r".\assets\cards\15.png",
                   r".\assets\cards\16.png",
                   r".\assets\cards\17.png",
                   r".\assets\cards\18.png",
                   r".\assets\cards\19.png",
                   r".\assets\cards\20.png",
                   r".\assets\cards\21.png",
                   r".\assets\cards\22.png",
                   r".\assets\cards\23.png",
                   r".\assets\cards\24.png",
                   r".\assets\cards\25.png",
                   r".\assets\cards\26.png",
                   r".\assets\cards\27.png",
                   r".\assets\cards\28.png",
                   r".\assets\cards\29.png",
                   r".\assets\cards\30.png",
                   r".\assets\cards\31.png",
                   r".\assets\cards\32.png",
                   r".\assets\cards\33.png",
                   r".\assets\cards\34.png",
                   r".\assets\cards\35.png",
                   r".\assets\cards\36.png",
                   r".\assets\cards\37.png",
                   r".\assets\cards\38.png",
                   r".\assets\cards\39.png",
                   r".\assets\cards\40.png",
                   r".\assets\cards\41.png",
                   r".\assets\cards\42.png",
                   r".\assets\cards\43.png",
                   r".\assets\cards\44.png",
                   r".\assets\cards\45.png",
                   r".\assets\cards\46.png",
                   r".\assets\cards\47.png",
                   r".\assets\cards\48.png",
                   r".\assets\cards\49.png",
                   r".\assets\cards\50.png",
                   r".\assets\cards\51.png",
                   r".\assets\cards\52.png",
                   ]
    flash = [[r".\assets\flash\1.png",
              r".\assets\flash\2.png",
              r".\assets\flash\3.png",
              r".\assets\flash\4.png"],
             [r".\assets\thunder\1.png",
              r".\assets\thunder\2.png",
              r".\assets\thunder\3.png",
              r".\assets\thunder\4.png",
              r".\assets\thunder\5.png",
              r".\assets\thunder\6.png",
              r".\assets\thunder\7.png",
              r".\assets\thunder\8.png",
              r".\assets\thunder\9.png",
              r".\assets\thunder\10.png"],
             [r".\assets\crash\1.png",
              r".\assets\crash\2.png",
              r".\assets\crash\3.png",
              r".\assets\crash\4.png",
              r".\assets\crash\5.png",
              r".\assets\crash\6.png",
              r".\assets\crash\7.png",
              r".\assets\crash\8.png",
              r".\assets\crash\9.png",
              r".\assets\crash\10.png"]
             ]
    specialEffect = [[r".\assets\arrow\1.png",
                      r".\assets\arrow\2.png",
                      r".\assets\arrow\3.png",
                      r".\assets\arrow\4.png",
                      r".\assets\arrow\5.png", ],
                     [r".\assets\tornado\1.png",
                      r".\assets\tornado\2.png",
                      r".\assets\tornado\3.png",
                      r".\assets\tornado\4.png", ],
                     [r".\assets\splash\1.png",
                      r".\assets\splash\2.png",
                      r".\assets\splash\3.png",
                      r".\assets\splash\4.png",
                      r".\assets\splash\5.png",
                      r".\assets\splash\6.png",
                      r".\assets\splash\7.png",
                      r".\assets\splash\8.png",
                      r".\assets\splash\9.png",
                      r".\assets\splash\10.png"]
                     ]
    nail = r".\assets\npc\nail.png"
    waterSound = r".\assets\sound\water.mp3"
    tornadoSound = r".\assets\sound\tornado.mp3"
    windSound = r".\assets\sound\wind.mp3"
    playerSound = [r".\assets\sound\electric.mp3",
                   r".\assets\sound\thunder.mp3",
                   r".\assets\sound\fire.mp3"
                   ]

class PortalSettings:
    width = 320
    height = 320
    coordX = (SceneSettings.tileXnum - 10) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2


class GameState(Enum):
    MAIN_MENU = 1
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_WILD = 6
    GAME_PLAY_CITY = 7
    GAME_PLAY_BOSS = 8


class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_SWITCH = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5
    EVENT_END = pygame.USEREVENT + 6
    EVENT_FIRE = pygame.USEREVENT + 7
