from enum import Enum
import datetime

baseWidth = 1280 // 10
baseHeight = 720 // 10
fps = 60
collisionTolerance = 5

class WindowSettings:
    title = "上科大的魔法石"
    width = 1280
    height = 720
    
class TileSettings:
    tileLength = 32

class GameState(Enum):
    MAIN_MENU = 1
    GAME_OVER = 2
    GAME_WIN = 3
    GAME_PLAY = 4

class PlayerSettings:
    speed = 8
    universeSpeedX = 10
    universeSpeedY = 10
    initHP = 6666
    initDEF = 50
    initATK = 100
    initMoney = 100000
    width = TileSettings.tileLength * 2

class NPCSettings:
    npcWidth = TileSettings.tileLength
    npcHeight = TileSettings.tileLength

class EnemySettings:
    enemyStudentSetting = {'HP':996,'ATK':180,'DEF':3.3}
    enemySISTSetting = {'HP':3500,'ATK':600,'DEF':300}
    enemySLSTSetting = {'HP':3000,'ATK':350,'DEF':100}
    enemySPSTSetting = {'HP':2500,'ATK':350,'DEF':200}
    enemyBossSetting = {'HP':9999,'ATK':650,'DEF':400}


class GamePath:
    font = r".\assets\font\LXGWNeoXiHei.ttf"
    player = [
        r".\assets\player\1-1.png", 
        r".\assets\player\1-2.png", 
        r".\assets\player\1-3.png", 
        r".\assets\player\1-4.png",
        r".\assets\player\2-1.png", 
        r".\assets\player\2-2.png", 
        r".\assets\player\2-3.png", 
        r".\assets\player\2-4.png",
        r".\assets\player\3-1.png", 
        r".\assets\player\3-2.png", 
        r".\assets\player\3-3.png", 
        r".\assets\player\3-4.png",
        r".\assets\player\4-1.png", 
        r".\assets\player\4-2.png", 
        r".\assets\player\4-3.png", 
        r".\assets\player\4-4.png",
    ]
    deadEnemy = r".\assets\player\deadEnemy.png"
    spaceShipImg = r".\assets\spaceShip\spaceShip.png"

    # 地图
    sceneHomeMap = r".\assets\ground\homebackground.tmx"
    sceneSchoolMap = r".\assets\ground\schoolbackground.tmx"
    sceneSLSTMap = r".\assets\ground\SLSTbackground.tmx"
    sceneSPSTMap = r".\assets\ground\SPSTbackground.tmx"
    sceneSISTMap = r".\assets\ground\SISTbackground.tmx"
    sceneUndergroundMap = r".\assets\ground\Undergroundbackground.tmx"
    sceneKFCMap = r".\assets\ground\KFCbackground.tmx"
    sceneUniverseMap = r".\assets\ground\Universebackground.tmx"

    # BGM
    bgmHome = r".\assets\bgm\Home.mp3"
    bgmSchool = r".\assets\bgm\School.mp3"
    bgmSLST = r".\assets\bgm\SLST.mp3"
    bgmSPST = r".\assets\bgm\SPST.mp3"
    bgmSIST = r".\assets\bgm\SIST.mp3"
    bgmUnderground = r".\assets\bgm\Underground.mp3"
    bgmKFC = r".\assets\bgm\KFC.mp3"
    bgmUniverse = r".\assets\bgm\Universe.mp3"
    bgmMainMenu = r".\assets\bgm\MainMenu.mp3"
    bgmGameOver = r".\assets\bgm\GameOver.mp3"
    bgmGameWin = r".\assets\bgm\GameWin.mp3"

    MainMenu = r".\assets\Menu\MainMenu.png"
    GameOver = r".\assets\Menu\GameOver.png"
    GameWin = r".\assets\Menu\GameWin.png"

    # 武器
    weaponGun = r".\assets\weapon\Gun.png"
    weaponSword = r".\assets\weapon\Sword.png"
    weaponAxe = r".\assets\weapon\Axe.png"
    weaponHand = r".\assets\weapon\Hand.png"
    # 特效
    swordFrames = [r".\assets\effect\SwordEffect4.png",]
    axeFrames = [r".\assets\effect\AxeEffect1.png",
                 r'.\assets\effect\AxeEffect2.png',
                 r'.\assets\effect\AxeEffect3.png',]
    gunFrames = [r".\assets\effect\GunEffect1.png",
                 r'.\assets\effect\GunEffect2.png',
                 r'.\assets\effect\GunEffect3.png',]
    handFrames = [r".\assets\effect\Hand1.png",
                    r'.\assets\effect\Hand2.png',
                    r'.\assets\effect\Hand3.png',
                    r'.\assets\effect\Hand4.png',]
    shieldFrames = [r".\assets\effect\Shield1.png",
                    r'.\assets\effect\Shield2.png',
                    r'.\assets\effect\Shield3.png',
                    r'.\assets\effect\Shield4.png',
                    r'.\assets\effect\Shield5.png']
    chargeFrames = [r".\assets\effect\Charge1.png",
                    r'.\assets\effect\Charge2.png',
                    r'.\assets\effect\Charge3.png',
                    r'.\assets\effect\Charge4.png']
    poisonFrames = [r".\assets\effect\Poison1.png",
                    r".\assets\effect\Poison2.png",
                    r".\assets\effect\Poison3.png",
                    r".\assets\effect\Poison4.png",]
    enemyFrames = [r".\assets\effect\Enemy1.png",
                     r".\assets\effect\Enemy2.png",
                     r".\assets\effect\Enemy3.png",
                     r".\assets\effect\Enemy4.png",
                     r".\assets\effect\Enemy5.png",]
                   

class ShopGoodsList:
    homeShopList = [("Get Random Weapon",100000),("/Remake",0)] # 购买的选项
    if datetime.datetime.now().strftime("%A") == 'Thursday':
        KFCShopList = [("HP + 500",500,500),("[疯狂星期四套餐]HP + 1000",50,1000),("支持作者",50,0)]
    else:
        KFCShopList = [("HP + 500",500,500),("支持作者",50,0),("建议周四再来KFC看看",0,0)]

class Dialog:
    guide = ['我们的星球已经陷入能源危机, 我在地球上找到了可以为我们', '提供能量的神秘魔法石,它位于上海科技大学的物质塔下方的藏宝室,','你需要驾驶飞船安全到达地球,然后前往三大学院,','打败怪兽获得技能, 打败学生获得金币,','这将给予你应对BOSS的力量。在此之前,','去找我们的军火商人吧, 用给你的100000经费买一把趁手的武器...','至于地下藏宝室有什么...我也不清楚了', '(按X结束对话)']

class GoldReward:
    value = 250
