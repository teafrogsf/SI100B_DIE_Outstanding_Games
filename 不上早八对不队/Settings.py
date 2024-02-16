# -*- coding:utf-8 -*-
from enum import Enum
import pygame

class WindowSettings:
    name = "你以为我想当勇者吗？"
    width = 1280
    height = 800
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class SceneSettings:
    tileXnum = 48 # 64
    tileYnum = 27 # 36
    tileWidth = 250
    tileHeight = 250
    House_height = 650
    House_width = 650


class PlayerSettings:
    # Initial Player Settings
    playerSpeed = 6
    playerWidth = 70
    playerHeight = 100
    playerHP = 20
    init_playerHP = 20
    playerAttack = 5
    playerDefence = 1
    playerMoney = 100

class NPCSettings:
    npcSpeed = 1
    npcWidth = 90
    npcHeight = 90
    dialogposX1,dialogposY1=WindowSettings.width*0.5//10,WindowSettings.height*2.5//10
    dialogposX2,dialogposY2=WindowSettings.width*4//10,WindowSettings.height*3//10
    dialogposX3,dialogposY3=WindowSettings.width*8.156//10,WindowSettings.height*1//2
class NPCType(Enum):
    DIALOG = 1
    MONSTER = 2
    SHOP = 3
class MonsterSettings:
    width = 200
    height = 200
    HP = 10
    Attack = 3
class BossSettings:
    width = 300
    height = 300
    coordX = (SceneSettings.tileXnum / 2) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2
    HP = 100
class SceneType(Enum):
    Village = 1
    WILD = 2
    BOSS = 3
    HOUSE = 4

class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxStartX = WindowSettings.width // 4           # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20 # Coordinate Y of the box

    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 -180        # Coordinate X of the first line of dialog
    textStartY = WindowSettings.height // 3 * 2 + 30    # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3  +15              # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20
    chooserectX,chooserectY=740,400
    chooserectWidth,chooserectHeight=200,70  
    dialognumber={1:{1:[0,2],2:[0,2]},2:{1:[0,8,6,6]},3:{1:[0,4]}}
    choosetextcontent={'merchant':['我不信','爆点金币'],'village_chief':['你很嚣张呀','6666666']}
    npcmeettextcontent={'merchant':[['你好呀小伙子，前面很危险的，你不要过去']]
                       , 'village_chief':[['你好！新来的勇者，欢迎来到我们"相亲相爱','和平美好"村！'],['新来的客人,我要好好招待你!'],['年轻人,又来了？']]
                                          ,'ghost':[['￥%￥#%……@!@']]}
    npctextcontent={'merchant':{1:{1:[['你要是非要去的话我这有点伤药','给你!']]},
                            2:{1:[['真是世风日下人心不古!','究竟是道德的沦丧还是人性的泯灭']]}},
                 'village_chief':{1:{1:[['这几天天气不好,在我们村子小住几天吧！','正好我们村子一年一度的祭祀就要开始了,','现在参与活动有机会享受人生八折套餐!']
                 ,['…现在的年轻人怎么这个年纪就开始耳背,','这种质量的可不行（小声嘀咕）']
                 ,['无论如何,请勇者一定要住下来！看你背着把剑,','我相信你一定能帮我们处理近期村庄的任务的!','请在这个房子暂住一会吧，全村最豪华的房子！']
                 ,['那你就随便看看吧.（获得木剑和地图）']
                 ],
                 2:[['来来来，尝尝我们村子的特产！我跟你讲,最近','附近不太太平,在祭祀活动完成之前千万不要','自己一个人去神社,很危险的！（获得泡面）',]
                    ,['神社附近的山林里常有熊出现','它们可吃了我们不少村民！']
                    ,['那你且在这里安心住下,我相信我们的保护神会','庇佑每一个虔诚的人,吾主保佑！'],
                    ['去吧，善良的年轻人.']],
                    3:[["什么？这里从来没有这号人，你怕是看错了."],
                       ['害，这个人是远近闻名的王老五啊.','做生意做的可大，这几年回来养老了.'],
                       ['这孩子说的什么傻话，那边已经荒废很久了','根本没人会去.']]}}
                       ,'ghost':{1:{1:[['￥%￥#%……@!@'],['@#%$!***','(获得木棍，尘封的真相)']]}}}
    playertextcontent={'merchant':{1:{1:[['或许我能得到什么神奇装备吗?','书上都是这么说的']]}
                                   ,2:{1:[['老登,爆点金币']]}},
                 'village_chief':{1:{1:[["相亲相爱和平美好村，多好听的名字啊!"]
                 ,['(从沉思中回过神)啊？你刚刚说什么？']
                 ,['奇怪，他在说什么呀?']
                 ,["我看出来了…"]
                 ],
                 2:[['感谢村长的招待!']
                    ,['为什么？']
                ,['好奇怪呀（吃饭吃饭，不理他）'],
                ['就算每天有吃有喝,也不能什么都不干吧','找机会看看有没有什么地方需要我帮忙好了']],
                3:[['村长爷爷,顺着那边路下去有一个神志不清的人','看着像这里的村民，你认识他吗？'],
                ["村长，这个人……是谁啊?",'(明明他刚被我“失手”打死了)'],
                ['我昨天在那条路的尽头分明见过他！']]}}
                 ,'ghost':{1:{1:[['啊啊啊啊啊尸体在说话！！！'],['（扭曲的蠕动）（阴暗的爬行）','（我已经是大学生了我可以发疯）','（慢慢挪到尸体前）']]}}}
class BattleSettings():
    boxWidth = WindowSettings.width * 3 // 4 
    boxHeight = WindowSettings.height * 3 // 4 
    boxStartX = WindowSettings.width // 8           # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 
    textPlayerStartX = WindowSettings.width // 4          # Coordinate X of the first line of dialog
    textMonsterStartX = WindowSettings.width // 2 +100   
    textStartY = WindowSettings.height // 3         # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3            # Vertical distance of two lines

    playerWidth = WindowSettings.width // 6
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8
    playerCoordY = WindowSettings.height // 2 

    monsterWidth = WindowSettings.width // 6
    monsterHeight = WindowSettings.height // 3
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 2 

    stepSize = 20
    rect = pygame.Rect((460,50),(600,600))
    Player_HP_pos_x = 110
    Player_HP_pos_y = 655
    Monster_HP_pos_x = WindowSettings.width*67/100
    Monster_HP_pos_y = WindowSettings.height*5/100
    Player_rect = pygame.Rect((WindowSettings.width*40/100,WindowSettings.height*50/100),(PlayerSettings.playerWidth*3,PlayerSettings.playerHeight*3))
    Monster_rect = pygame.Rect((WindowSettings.width*65/100,WindowSettings.height*14/100),(MonsterSettings.width,MonsterSettings.height))
    Player_rect_0 = pygame.Rect((WindowSettings.width*40/100,WindowSettings.height*50/100),(PlayerSettings.playerWidth*3,PlayerSettings.playerHeight*3))
    Monster_rect_0 = pygame.Rect((WindowSettings.width*65/100,WindowSettings.height*14/100),(MonsterSettings.width,MonsterSettings.height))

class ShopSettings:
    boxWidth = 800
    boxHeight = 200
    boxStartX = WindowSettings.width // 4   # Coordinate X of the box
    boxStartY = WindowSettings.height // 3  # Coordinate Y of the box

    textSize = 56 # Default font size
    textStartX = boxStartX + 10         # Coordinate X of the first line of dialog
    textStartY = boxStartY + 25    # Coordinate Y of the first line of dialog
class BackpackSettings:
    CD = 300
    backpack_rect = pygame.Rect((50,50),(400,600))
    backpack_rect2 = pygame.Rect((500,50),(400,300))
    item_size = 80
class GamePath:
    # Window related path
    menu     = r".\assets\background\menu.png"
    index    = r".\assets\background\index.png"
    village  = r".\assets\background\village.png"
    mapBlock = r".\assets\background\map.png"
    house    = r".\assets\background\house.png"
    dungeon  = r".\assets\background\dungeon.png"
    wild     = r".\assets\background\wild.gif"
    boss     = r".\assets\background\boss_fight.png"
    start    = r".\assets\background\start.png"
    game_over     = r".\assets\background\game_over.png"
    game_victory  = r".\assets\background\game_victory.png"
    # player/npc related path
    npc = [r".\assets\npc\merchant.png",
           r".\assets\npc\village_chief.png",
           r".\assets\npc\ghost.png"]
    player = {
        'front' :[
        r".\assets\player\front\1.png", 
        r".\assets\player\front\1.png",
        r".\assets\player\front\2.png", 
        r".\assets\player\front\2.png", 
        r".\assets\player\front\3.png", 
        r".\assets\player\front\3.png", 
        r".\assets\player\front\4.png", 
        r".\assets\player\front\4.png", 
        # 8 frames for a single loop of animation looks much better.
        ],
        'back': [
        r".\assets\player\back\1.png", 
        r".\assets\player\back\1.png",
        r".\assets\player\back\2.png", 
        r".\assets\player\back\2.png", 
        r".\assets\player\back\3.png", 
        r".\assets\player\back\3.png", 
        r".\assets\player\back\4.png", 
        r".\assets\player\back\4.png", 
        # 8 frames for a single loop of animation looks much better.
        ],
        'left': [
        r".\assets\player\left\1.png", 
        r".\assets\player\left\1.png",
        r".\assets\player\left\2.png", 
        r".\assets\player\left\2.png", 
        r".\assets\player\left\3.png", 
        r".\assets\player\left\3.png", 
        r".\assets\player\left\4.png", 
        r".\assets\player\left\4.png", 
        # 8 frames for a single loop of animation looks much better.
        ],
        'right' :[
        r".\assets\player\right\1.png", 
        r".\assets\player\right\1.png",
        r".\assets\player\right\2.png", 
        r".\assets\player\right\2.png", 
        r".\assets\player\right\3.png", 
        r".\assets\player\right\3.png", 
        r".\assets\player\right\4.png", 
        r".\assets\player\right\4.png", 
        # 8 frames for a single loop of animation looks much better.
        ]

    }
    dialog_box=[r".\assets\dialog_box\protagonist.png",
                r".\assets\dialog_box\merchant.png",
                r".\assets\dialog_box\village_chief.png",
                r".\assets\dialog_box\box.png"]
    bgm = r".\assets\bgm\main.mp3"
    village_obstacle = [r".\assets\obstacle\0.png",
                        r".\assets\obstacle\1.png",
                        r".\assets\obstacle\2.png",
                        r".\assets\obstacle\3.png",
                        r".\assets\obstacle\4.png" ,
                        r".\assets\obstacle\transmit_dungeon.png",
                        r".\assets\obstacle\transmit_wild.png",
                        r".\assets\obstacle\transmit_house.png"
                        ]
   
    village_portal = r".\assets\portal\door.png"

    house_obstacle = [r".\assets\obstacle\house\house_obstacle01.png",
                      r".\assets\obstacle\house\house_obstacle02.png",
                      r".\assets\obstacle\house\house_obstacle03.png",
                      r".\assets\obstacle\house\house_obstacle04.png",
                      r".\assets\obstacle\house\house_obstacle05.png",
                      r".\assets\obstacle\house\house_obstacle06.png",
                      r".\assets\obstacle\house\house_obstacle07.png",
                      r".\assets\obstacle\house\house_obstacle08.png" ,
                      r".\assets\obstacle\house\house_obstacle09.png" ,
                      r".\assets\obstacle\house\house_obstacle10.png",
                      r".\assets\obstacle\house\house_obstacle11.png"
                    ]
    dungeon_obstacle = [r".\assets\obstacle\dungeon\dungeon_obstacle01.png" ,
                      r".\assets\obstacle\dungeon\dungeon_obstacle02.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle03.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle04.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle05.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle06.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle07.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle08.png" ,
                      r".\assets\obstacle\dungeon\dungeon_obstacle09.png" ,
                      r".\assets\obstacle\dungeon\dungeon_obstacle10.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle11.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle12.png",
                      r".\assets\obstacle\dungeon\dungeon_obstacle13.png"

                    ]
    wild_obstacle = [r".\assets\obstacle\wild\wild_obstacle01.png" ,
                      r".\assets\obstacle\wild\wild_obstacle02.png",
                      r".\assets\obstacle\wild\wild_obstacle03.png",
                      r".\assets\obstacle\wild\wild_obstacle04.png",
                      r".\assets\obstacle\wild\wild_obstacle05.png",
                      r".\assets\obstacle\wild\神庙门.png"

                    ]
    # # 传送地牢 2024/01/17
    # village_transmit_dungeon = r".\assets\portal\transmit_dungeon.png"
    # # 传送地牢 2024/01/17
    # village_transmit_wild = r".\assets\portal\transmit_wild.png"

    items = [r".\assets\items\empty_bottle.png",
             r".\assets\items\letter.png",
             r".\assets\items\map.png",
             r".\assets\items\medicine_bottle.png",
             r".\assets\items\musty_truth.png",
             r".\assets\items\wooden_sword.png",
             r".\assets\items\iron_sword.png",
             r".\assets\items\golden_sword.png",
             r".\assets\items\poison.png",
             r".\assets\items\magic_wand.png",
             r".\assets\items\achieve_list.png",
             r".\assets\items\cup_noodle.png",
             r".\assets\items\lamp.png"
            ]
    select = r".\assets\items\select.png"
    monsters =[r".\assets\monster\villager.png",
               r".\assets\monster\mimic.png",
               r".\assets\monster\heretic.png",
               r".\assets\monster\villager.png"
               ] 
    mimic =  r".\assets\monster\mimic_battle.png"
    monsters_be_poisoned = [r".\assets\monster\villager_be_poisoned.png",
                            r".\assets\monster\mimic_battle_be_poisoned.png",
                            r".\assets\monster\heretic_be_poisoned.png",
                            r".\assets\monster\villager_be_poisoned.png"
                            ]
    UI = r".\assets\UI\box.png" 
    battle_detail = r".\assets\UI\battle_detail.png" 
    backpack = r".\assets\UI\backpack.png" 
    HP = [r".\assets\UI\HP_left.png",
          r".\assets\UI\HP_middle.png",
          r".\assets\UI\HP_right.png",
          r".\assets\UI\HP_left_empty.png",
          r".\assets\UI\HP_middle_empty.png",
          r".\assets\UI\HP_right_empty.png"
        ]

class ObstacleSize:
    img_width = [
                350,330,270,370,425 ,150,150,150
                ]
    img_height = [
                330,330,330,300,350 ,150,150,150
                ]
class House_ObstacleSize:
    img_width = [
                795,485,370,60,60,65,180,495 ,50,370,50
                ]
    img_height =[
                300,340,700,415,300,225,225,555 ,105,230,25
                ]
class Dungeon_ObstacleSize:
    img_width = [
                90,880,95,260,190,295,195,250,285,190,80,90,100
                ]
    img_height =[
                200,130,295,120,260,435,335,495,325,185,185,105,20
                ]
class Wild_ObstacleSize:
    img_width = [
                375,300,1280,1280,60,190
                ]
    img_height =[
                800,800,380,145,20,113
                ]
    # hitbox_width = [
    #             250
    #         ]
    # hitbox_height =[
    #             83
    #         ] 
        
class ObstaclesLoc:
    img_x = [
            1540,1590,940,390,354,0,0,1680
            ]
    img_y = [
            750,320,780,550,7,905,395,620
            ] 
class House_ObstaclesLoc:
    img_x = [
            0,795,0,370,420,480,615,785,740,910,520
            ]
    img_y = [
            0,0,200,485,600,675,675,355,420,240,545
            ] 
class Dungeon_ObstaclesLoc:
    img_x = [
            0,195,1185,1020,1090,985,785,525,205,205,310,495,90
            ]
    img_y = [
            0,0,0,195,300,465,565,405,405,305,210,200,0
            ] 
class Wild_ObstaclesLoc:
    img_x = [
            0,490,0,0,420,325
            ]
    img_y = [
            0,0,0,655,380,480
            ] 
    # hitbox_x = [0,0
    #             # WindowSettings.width*63/10
    #             ]
    # hitbox_y = [0,0
    #             # WindowSettings.height*70/100
    #             ]
    

class PortalSettings:
    width = 100
    height = 75
    # coordX = (SceneSettings.tileXnum - 10) * SceneSettings.tileWidth - width / 2
    # coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2

class GameState(Enum):
    MAIN_MENU = 1
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_WILD = 6
    GAME_PLAY_VILL = 7
    GAME_PLAY_BOSS = 8
    GAME_PLAY_HOUSE = 9
    GAME_BACKPACK = 10
    GAME_PLAY_DUNGEON = 11
    GAME_INDEX = 12
    GAME_VICTORY = 13
class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_SWITCH = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5
    EVENT_BACKPACK = pygame.USEREVENT + 6
    EVENT_BOSSBATTLE = pygame.USEREVENT + 7
directions =[
    'front', 'back', 'left', 'right'
]
itemtext = [
    '喝药剩下的的空瓶子',
    '你的高数试卷，可以让你的敌人头痛',
    '你需要知道这个村子都有些什么东西，你也\n不想莫名其妙丢了性命吧，小鬼\n地图上似乎在村庄尽头左手边的小路上有一\n处模糊的标记',
    '实用的回血道具，及时使用就感觉不到疼痛\n战斗中使用：恢复五点生命值',
    '或许，这个世界，一切的礼物，都在暗中标\n好了价格所谓的保护神，是一条条人命堆积\n出来的邪神；所谓的保护，也只不过是一场\n长时间的交易。消失后又出现的村民，他们\n的灵魂早已不在他的躯壳之中，和蔼的村长，\n是知道一切后沉默的帮凶。谁是真凶，是过\n分的欲望，亦或者是腐烂的人心？无从知晓。\n所以，少年，你的下一步，要往哪里走呢',
    '一把不知道什么时候出现的东西，你会需要\n它的\n战斗中使用：造成两点伤害',
    '一件更趁手的武器\n战斗中使用： 造成四点伤害',
    '正规途径下你能得到的杀伤力最大的武器，\n好好利用它，少年\n战斗中使用：造成六点伤害',
    '一瓶你一直忘记喝的冰红茶，变成了绿色\n你不会想尝尝它的味道的\n战斗中使用：向敌人扔出，使其中毒，每个\n回合结束时受到一点伤害',
    '恭喜你！不走寻常路的少年！有了它，你可\n以称霸整个游戏!\n战斗中使用：释放阿瓦达啃大瓜，秒杀敌人！ ',
    '记录着勇敢的勇者做出的所有决策，而是好\n是坏，或许只有勇者本人清楚',
    '有时候会很有用，平时只是一个画风很不一\n样但平平无奇的泡面，唯一值得欣慰的是不\n需要找开水泡开，它可以自己泡自己',
    '一个散发着诡异气氛的手提灯，能照亮小范\n围的路，有传说说油灯是沟通阴阳两界的桥梁'
    
]
class dialognpc(Enum):
    merchant=1
    village_chief=2
    ghost=3
class PlayerState(Enum):
    front = 1
    left = 2
    right = 3
    back = 4
class ObstaclesPos(Enum):
    front = 1
    behind = 2
class Items(Enum):
    empty_bottle = 0
    letter = 1
    map = 2
    medicine_bottle = 3
    musty_truth = 4
    wooden_sword = 5
    iron_sword = 6
    goledn_sword = 7
    poison = 8
    magic_wand = 9
    achieve_list = 10
    cup_noodle = 11
    lamp = 12
class Monsters(Enum):
    villager = 0
    mimic = 1
    heretic = 2
    villager2 = 3
Monster_pos = [
    (800,400),
    (1100,10),
    (1000,50),
    (100,600),
]
Monster_size = [
    (70,100),
    (70,70),
    (70,100),
    (70,100)
]
class type(Enum):
    weapon = 0
    healing = 1
    poison = 2
    magic_wand = 3
    achieve_list = 4
class init_player_pos:
    village_x = WindowSettings.width *9/10
    village_y = WindowSettings.height *5.5/10
    house_x   = 545 
    house_y   = 630
    wild_x    = 385
    wild_y    = 530
    dungeon_x = 105
    dungeon_y = 25
    # 进入boss地图不显示主角
    boss_x = -300
    boss_y = -300
# lst add begin 2024/01/15
# 位移信息
class displacement_settings:
    offset_x = 0        #x坐标移动量
    offset_y = 0        #y坐标移动量
    offset_x_max = 0    #最大可移动横坐标偏移量（在Scene 中render_map 方法完成设置）
    offset_y_max = 0    #最大可移动纵坐标偏移量（在Scene 中render_map 方法完成设置）
    village_map_x = 0           #地图当前所在横坐标
    village_map_y = 0           #地图当前所在纵坐标
    zone = PlayerSettings.playerSpeed            #区域大小
    # 中心区域位置
    central_zone_x_min = WindowSettings.width // 2 - zone
    central_zone_x_max = WindowSettings.width // 2 + zone
    central_zone_y_min = WindowSettings.height // 2 - zone
    central_zone_y_max = WindowSettings.height // 2 + zone
class map_info_setting:
    map_info = 1    #地图信息，1：village_map; 2：house_map; 3:地牢; 4:野外动图; 5:boss map
class transmit_setting:
    # 地牢
    transmit_dungeon_x_min = 0
    transmit_dungeon_x_max = 300
    transmit_dungeon_y_min = 810
    transmit_dungeon_y_max = 1010
    # 野外 gif
    transmit_wild_x_min = 0
    transmit_wild_x_max = 300
    transmit_wild_y_min = 260
    transmit_wild_y_max = 560
# lst add end 2024/01/15
    
# 传送地牢设置 2024/01/17
class TransmitDungeonSettings:
    y_min = 400
    y_max = 520
    X_min = 0
    x_max = 20
# 传送野外设置 2024/01/17
class TransmitWildSettings:
    y_min = 326
    y_max = 345
    X_min = 0
    x_max = 30
# 进入house 设置 2024/01/18
class TransmitHouseSettings:
    y_min = 340
    y_max = 360
    X_min = 600
    x_max = 624
# 野外传送至Boss
class WildToBossSettins:
    X_min = 385
    x_max = 420
    y_min = 380
    y_max = 400
# village map 设置 2024/01/18
class HouseTransmitVillageSettings:
    y_min = 545
    y_max = 570
    X_min = 520
    x_max = 570
    house_back_player_x = 612
    house_back_player_y = 440
# village map 设置 2024/01/18
class DungeonToVillageSettings:
    X_min = 90
    x_max = 185
    y_min = 0
    y_max = 20
    dungeon_back_player_x = 80
    dungeon_back_player_y = 480
    # dungeon_back_player_x = WindowSettings.width *9/10
    # dungeon_back_player_y = WindowSettings.height *5.5/10
# class WildToBossSettins:
#     X_min = 90
#     x_max = 185
#     y_min = 0
#     y_max = 20
class HPbox:
    size = 20
class IndexSettin:
    index_state = 1 #点击开始进入游戏的值，游戏中，该值被修改为非1值，用于判断乡村地图是否需要计算初始位置
    # 进入游戏，鼠标点击范围
    enter_X_min = 820
    enter_x_max = 1000
    enter_y_min = 455
    enter_y_max = 520
    # 退出游戏，鼠标点击范围
    exit_X_min = 820
    exit_x_max = 1000
    exit_y_min = 585
    exit_y_max = 650
class dialognpc(Enum):
    merchant=1
    village_chief=2
    ghost=3
talkover=[False,False,False,False,False,False,False,False,False,False,False,False,False]
class selftalking:
    village = ['在社会实践的路上，你由于种种原因和大家走散了\n在试图与大部队汇合的途中，你意外的走进了这样\n一个村子',
               '（这里是什么地方啊，画风怎么这么草率.....',
               '*低头 啊啊啊啊啊啊啊我变像素块了,还有这个白毛\n的设定到底是什么鬼啊！',
               '那里有个屋子，先去屋子里找人问问什么情况吧',
               'WASD移动，Q打开背包E交互ENTER选择']
    boss = ['这似乎是一张力量悬殊的战斗，你的选择也将决定整个事情的发展走向',
            '啊啊啊啊啊这又是什么奇怪的设定啊！哪里来的实体\n对话框！！能看见这种东西,我真是要疯了',
            '我真的要跟他战斗吗？']