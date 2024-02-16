# -*- coding:utf-8 -*-

from enum import Enum
from Design import *


class BasicSettings:
    loginFps = 60
    gameFps = 60
    fontPathKai = r".\assets\fonts\simkai.ttf"
    fontPathSong = r".\assets\fonts\simsun.ttc"
    fontPathLucida = r".\assets\fonts\lucon.ttf"
    userfile = r".\users.json"


class LoginSettings:
    bg = r".\assets\login2.png"
    wordStartX = 220
    wordStartY = 190
    wordSize = 36
    wordDeltaY = wordSize * 1.5
    titleSize = 50
    titleDeltaY = titleSize * 2
    titleStartX = 200
    titleStartY = 150
    signX = 180
    tipsSize = 20
    tipsStartX = 200
    tipsStartY = 500
    tipsDeltaY = tipsSize * 1.5
    suffixSize = 40
    suffixDeltaX = 70
    suffixDeltaY = titleSize - suffixSize


class WindowSettings:
    name = "Wiuoto"
    width = 1280
    height = 720
    outdoorScale = 1.5
    # stayZoneWidthScale = 0.5 # (总宽-画面宽)/2 在这个区域里camera与人物同时移动，即人物相对静止 (愚蠢的参数，之后再来处理)
    # stayZoneHeightScale = 0.5


class SceneSettings:
    waterColor = (49, 131, 214)  # (112, 184, 240)


class PlayerSettings:
    width = 30
    height = 60
    legHeight = 15
    footHeight = 5
    rectWidth = 26
    path = [
        [r".\assets\player\walk\0\00.png", r".\assets\player\walk\0\01.png", r".\assets\player\walk\0\02.png",
            r".\assets\player\walk\0\03.png", r".\assets\player\walk\0\04.png", r".\assets\player\walk\0\05.png"],         # 上下左右方向的动作路径
        [r".\assets\player\walk\1\10.png", r".\assets\player\walk\1\11.png", r".\assets\player\walk\1\12.png",
         r".\assets\player\walk\1\13.png", r".\assets\player\walk\1\14.png", r".\assets\player\walk\1\15.png"],
        [r".\assets\player\walk\2\20.png", r".\assets\player\walk\2\21.png", r".\assets\player\walk\2\22.png",
         r".\assets\player\walk\2\23.png", r".\assets\player\walk\2\24.png", r".\assets\player\walk\2\25.png"],
        [r".\assets\player\walk\3\30.png", r".\assets\player\walk\3\31.png", r".\assets\player\walk\3\32.png",
         r".\assets\player\walk\3\33.png", r".\assets\player\walk\3\34.png", r".\assets\player\walk\3\35.png"]
    ]
    # test
    # speed = 9
    speed = 2.2
    runSpeed = 5
    walkPeriod = 10


class FigureSettings:
    width = 30
    height = 45
    rect_width = 30
    rect_height = 30


class ShopSettings:
    goldX = 50
    goldSize = 40
    goldY = 40
    hintX = 850
    startY = 105
    imgX = 50
    imgSize = 45
    caterX = 140
    descriptionX = 300
    priceX = 1100
    textColor = (255, 255, 255)
    textFont = BasicSettings.fontPathKai
    textSize = 26
    textShift = 0.7 * (imgSize - textSize)
    deltaY = imgSize + 10
    blockX = 0
    blockHeight = 60
    blockShift = (blockHeight - imgSize) // 2
    blockWidth = 1500
    blockColor = (66, 39, 49, 200)
    blockColor2 = (120, 60, 30, 200)


class CommandSettings:
    blockX = 0
    blockY = 660
    blockWidth = 650
    blockHeight = 50
    blockColor = (13, 29, 39, 128)
    wordX = 30
    wordY = 670
    wordSize = 30
    wordColor = (255, 255, 255)
    textLimit = 30


class MenuSettings:
    bgX = 0
    bgY = 0
    bgWidth = 1280
    bgHeight = 720
    bgColor = (17, 22, 22, 210)
    lbgX = 0
    lbgY = 0
    lbgWidth = 245
    lbgHeight = 720
    lbgColor = (130, 130, 130, 80)
    catergoryX = 35
    catergoryY = 140
    catergoryDeltaY = 80
    catergorySize = 30
    catergoryColor = (255, 255, 255)
    catergoryColor2 = (0, 0, 0)
    catergoryFont = BasicSettings.fontPathKai
    catergory = ["角色信息", "猫糕", "技能卡", "队伍配置", "传送点"]
    leftChooseBlockX = 23
    leftChooseBlockY = 128
    leftChooseBlockWidth = 195
    leftChooseBlockHeight = 55
    leftChooseBlockColor = (255, 255, 255, 200)
    profileY = 130
    titleX = 340
    titleDeltaY = 70
    titleColor = (255, 255, 255)
    titleSize = 35
    titleFont = BasicSettings.fontPathKai
    subtitleX = 400
    subtitleDeltaY = 50
    subtitleColor = (255, 255, 255)
    subtitleSize = 25
    subtitleFont = BasicSettings.fontPathKai
    skillPreviewSize = 150
    skillPreviewX = 300
    skillPreviewY = 115
    skillPreviewDeltaX = skillPreviewSize + 25
    skillPreviewDeltaY = skillPreviewSize + 50
    skillPreviewRowLimit = 5
    skillPreviewNameDistance = skillPreviewSize + 10
    skillPreviewNameColor = (255, 255, 255)
    skillPreviewNameSize = 20
    skillPreviewNameFont = BasicSettings.fontPathKai
    skillPreviewBlockColor = (255, 255, 255, 233)
    skillPreviewBlockDelta = 6
    skillPreviewBlockSize = skillPreviewSize + skillPreviewBlockDelta * 2
    skillX = 300
    skillY = 105
    skillWidth = 270
    skillHeight = 477
    skillDetailX = 640
    skillDetailY = 125
    skillDetailDeltaY = 75
    skillDescriptionSize = 26
    skillDescriptionLimit = 20
    skillDescriptionRowDistance = skillDescriptionSize + 3

    catPreviewSize = 150
    catPreviewX = 300
    catPreviewY = 115
    catPreviewDeltaX = catPreviewSize + 25
    catPreviewDeltaY = catPreviewSize + 50
    catPreviewRowLimit = 5
    catPreviewNameDistance = catPreviewSize + 10
    catPreviewNameColor = (255, 255, 255)
    catPreviewNameSize = 20
    catPreviewNameFont = BasicSettings.fontPathKai
    catPreviewBlockColor = (220, 220, 220, 150)
    catPreviewBlockDelta = 6
    catPreviewBlockSize = catPreviewSize + catPreviewBlockDelta * 2
    catX = 350
    catY = 105
    catWidth = 225
    catHeight = 230
    catDetailX = 720
    catDetailY = 115
    catTitleDeltaY = 60
    catTitleSize = 30
    catSubTitleSize = 25
    catSubTitleDeltaY = 40
    catNumX = 810
    catSkillPreviewX = 460
    catSkillPreviewY = 450
    catSkillPreviewSize = 170
    catSkillPreviewDeltaX = 410
    catSkillPreviewNoneColor = (200, 190, 190, 200)
    catSkillPreviewBlockDelta = 6
    catSkillPreviewBlockColor = (255, 255, 255, 255)

    replaceSkillX = 420
    replaceSkillY = 115
    replaceSkillSize = 50
    replaceSkillDeltaY = replaceSkillSize + 12
    replaceSkillIDX = 300
    replaceSkillIDSize = 30
    replaceSkillTextColor = (255, 255, 255)
    replaceSkillTextFont = BasicSettings.fontPathKai
    replaceSkillTextSize = 25
    replaceSkillTextDownShift = replaceSkillSize - replaceSkillTextSize - 10
    replaceSkillDescriptionX = 520
    replaceSkillBlockX = 280
    replaceSkillBlockY = 112
    replaceSkillBlockWidth = 1100
    replaceSkillBlockHeight = 58
    replaceSkillBlockColor = (120, 60, 30, 200)

    unitPreviewTextShiftX = 55
    unitPreviewTextY = 180
    unitPreviewTextSize = 35
    unitPreviewTextColor = (255, 255, 255)
    unitPreviewTextFont = BasicSettings.fontPathKai
    unitPreviewX = 310
    unitPreviewY = 270
    unitPreviewSize = 190
    unitPreviewDeltaX = unitPreviewSize * 1.25
    unitPreviewNoneColor = (190, 190, 190, 80)
    unitPreviewChooseDeltaSize = 10
    unitPreviewChooseColor = (255, 255, 255, 140)
    replaceCatX = 490
    replaceCatY = 170
    replaceCatSize = 50
    replaceCatDeltaY = replaceCatSize + 16
    replaceCatIDX = 290
    replaceCatIDSize = 30
    replaceCatTextColor = (255, 255, 255)
    replaceCatTextFont = BasicSettings.fontPathKai
    replaceCatTextSize = 28
    replaceCatTextDownShift = replaceCatSize - replaceCatTextSize - 10
    replaceCatAttributeX = 700
    replaceCatAttributeDeltaX = 130
    replaceCatBlockX = 280
    replaceCatBlockHeight = replaceCatSize + 5
    replaceCatBlockY = replaceCatY - \
        (replaceCatBlockHeight - replaceCatSize) / 2
    replaceCatBlockWidth = 1300
    replaceCatBlockColor = (66, 39, 49, 200)
    replaceCatBlockColor2 = (120, 60, 30, 200)
    replaceCatEntryY = 120

    anchorX = 340
    anchorY = 100
    anchorSize = 30
    anchorColor = (255, 255, 255)
    anchorFont = BasicSettings.fontPathKai
    anchorDeltaY = anchorSize + 20


class BellSettings:
    img = r".\assets\map\bell.png"
    scale = (125, 154)
    safeZone = 74


class BoardSettings:
    blockX = 950
    blockY = 660
    blockWidth = 650
    blockHeight = 50
    blockColor = (13, 29, 39, 128)
    hintX = 960
    hintY = 670
    hintSize = 25
    hintColor = (255, 255, 255)
    hintFont = BasicSettings.fontPathKai


class DialogueSettings:
    bgWidth = 1280
    bgHeight = 500
    bgX = (WindowSettings.width - bgWidth) // 2
    bgY = (WindowSettings.height - bgHeight) // 2
    bgColor = (13, 22, 32, 190)
    textX = 450
    textY = 180
    textSize = 30
    textColor = (255, 255, 255)
    textColor2 = (0, 0, 0)
    textFont = BasicSettings.fontPathSong
    rowLimit = 21
    rowSpace = 38
    optionX = 950
    optionY = 390
    optionSpace = 48
    chooseColor = (255, 255, 255, 200)
    chooseX = 930
    chooseY = 273
    chooseWidth = 293
    chooseHeight = 45
    chooseSpace = 48


class UISettings:
    UIStartX = 0
    UIStartY = 0


class MapSettings:
    square = 30                                 # 不写明Width Height的默认为方形
    squareXnum = 90
    squareYnum = 50
    width = square * squareXnum
    height = square * squareYnum
    treeWidth = 2 * square
    treeHeight = 36 / 32 * treeWidth
    treeDeltaY = treeHeight - treeWidth
    treeDeltaRect = 0                           # 一个为了美观而增加的危险的参数，如果出现bug就把这里改成0
    # update: 把这个参数移动到人物footHeight里了
    treeXnum = 45
    treeYnum = 25
    ground = square
    groundXnum = 90
    groundYnum = 50


class MapPath:
    tree = r".\assets\map\tree.png"
    pillar = r".\assets\map\pillar.png"
    anchor = r".\assets\map\anchor.png"
    grass = r".\assets\map\grass.png"
    bush = r".\assets\map\bush.png"
    flower = r".\assets\map\flower.png"
    ground = ["",
              r".\assets\map\grass_ground.png",
              r".\assets\map\sand_ground.png",
              r".\assets\map\floor.png",
              r".\assets\map\playground.png"
              ]
    treeOnGround = r".\assets\map\tree_g.png"
    board = r".\assets\map\board.png"


class Music:
    login = r".\assets\music\Tabiji.mp3"
    map = [
        r".\assets\music\map\NewBarkTown.mp3",
        r".\assets\music\map\TheFirstTown.mp3",
        r".\assets\music\map\Gymnopedies1.mp3"
    ]
    volume = [
        0.5,
        0.5,
        1.0
    ]
    battle = r".\assets\music\battle\Zoltraak.mp3"


class GameState(Enum):
    pass

# 属性信息


class FlavorInfo(Enum):
    STRANGE = (0, "奇")
    SWEET = (1, "甜")
    SPICY = (2, "辣")
    SOUR = (3, "酸")
    SALTY = (4, "咸")
    COLD = (5, "冰")
    BITTER = (6, "苦")
    STICKY = (7, "粘")


# # 对上面info的反映射
# class FlavorMap:
#     map = [
#         "奇",
#         "甜",
#         "辣",
#         "酸",
#         "咸",
#         "冰",
#         "苦"
#     ]

# 属性克制
class FlavorAdvan:
    pass


class UISettings:
    pass


class CakeSettings:
    Hp = 100
    Atk = 5
    Pp = 10
    Def = 5
    Skill1 = None  # q
    Skill2 = None  # w


class SkillSettings:
    pp = 0  # 蓝耗
    pow = 0
    skilltype = 0
    r = 0  # 技能半径

    AttackPath = []
    for i in range(1, 62):
        AttackPath.append('./assets/particle/attack/'+str(i)+".png")

    HealPath = []
    for i in range(1, 92):
        HealPath.append('./assets/particle/heal/'+str(i)+".png")

    EnhancePath = []
    for i in range(1, 62):
        EnhancePath.append('./assets/particle/enhance/'+str(i)+".png")


class BattleSettings:
    background = r".\assets\map\battle_background.png"

    cakeStartX = 430
    cakeStartY = 240
    cakeIconX = 80
    cakeIconY = 80

    enemyStartX = 800
    enemyStartY = 240
    enemyIconX = 80
    enemyIconY = 80

    iconGap = 30

    skillStartX = 215
    skillStartY = 480
    skillIconX = 150
    skillIconY = 150

    skillGap = 200

    skillSize = 30
    skillColor = (0, 0, 0)
    skillFont = BasicSettings.fontPathSong

    attributeSize = 25
    attributeColor = (0, 0, 0)
    attributeFont = BasicSettings.fontPathSong

    hpSize = 20
    hpColor = (0, 0, 0)
    hpFont = BasicSettings.fontPathSong

    hpRiseDelatY = hpSize+60
    hpRiseSpeed = 4

    hpRiseSize = 40
    hpRiseFont = BasicSettings.fontPathSong
    hpRiseColor = {'+': (0, 255, 0), '-': (255, 0, 0)}

    hpBarPath = r".\assets\ui\hp_bar.png"
    hpBrickPath = r".\assets\ui\hp_brick.png"
    hpBarX = 85
    hpBarY = 25
    hpBrickX = 80
    hpBrickY = 20

    ppPath = {
        2: r".\assets\skill\pp_2.png",
        4: r".\assets\skill\pp_4.png"
    }
    ppX = 50
    ppY = 50

    energyBarPath = r".\assets\ui\energy_bar.png"
    energyBrickPath = r".\assets\ui\energy_brick.png"
    energyBarX = 504
    energyBarY = 52
    energyBrickX = 40
    energyBrickY = 20
    energyBarStartX = 388
    energyBarStartY = 80
    energyBrickStartX = 404
    energyBrickStartY = 96
    energyBrickGap = 8

    emptySkill = r".\assets\skill\empty.png"
    emptyAlpha = 128

    effectAnimateTime = 7

    hintStartX = 492
    hintStartY = 40
    hintSize = 40
    hintFont = BasicSettings.fontPathSong
    hintColor = (255, 255, 255)

    trashKing = r".\assets\catcake\preview\cake_01_special.png"
    trashKingIconX = 80
    trashKingIconY = 200
