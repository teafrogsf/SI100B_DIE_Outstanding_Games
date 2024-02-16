import pygame
import Map
import Player
import NPCs
import Portal
from Pokemon import *
from Settings import *


# generate every scene
class Scene():
    def __init__(self, window, Initial_X, Initial_Y):
        self.state = None
        self.map = None
        self.obstacles = None
        self.hospital = None
        self.gym = None
        self.shop = None
        self.citystation = None
        self.wildstation = None
        self.walls = None
        self.doors = None
        self.stones = None
        self.grasses = None
        self.background = None
        
        self.portal = pygame.sprite.Group()
        self.npcsNormal = pygame.sprite.Group()
        self.npcsTrader = pygame.sprite.Group()
        self.npcsTrainer = pygame.sprite.Group()

        self.window = window
        self.battle = None
        self.battleBox = None
        self.shoppingBox = None
        self.subMenuBox = None
        self.dialogBox = None
        self.talkWith = None
        self.tradeWith = None
        self.battleWith = None
        self.pressF = False

        self.cameraX = Initial_X
        self.cameraY = Initial_Y

    def check_draw(self, Obj):
        if Obj is not None:
            Obj.draw(self.window)

    # render for every scene
    def render(self):
        if self.state == GameState.GAME_PLAY_CITY:
            for i in range(SceneSettings.city_tileXnum):
                for j in range(SceneSettings.city_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        if self.state == GameState.GAME_PLAY_HOSPITAL:
            for i in range(SceneSettings.hospital_tileXnum):
                for j in range(SceneSettings.hospital_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        if self.state == GameState.GAME_PLAY_GYM:
            for i in range(SceneSettings.gym_tileXnum):
                for j in range(SceneSettings.gym_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        if self.state == GameState.GAME_PLAY_WILD:
            for i in range(SceneSettings.wild_tileXnum):
                for j in range(SceneSettings.wild_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        if self.state == GameState.GAME_PLAY_SHOP:
            for i in range(SceneSettings.shop_tileXnum):
                for j in range(SceneSettings.shop_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        
        self.check_draw(self.background)
        self.check_draw(self.gym)
        self.check_draw(self.hospital)
        self.check_draw(self.shop)
        self.check_draw(self.citystation)
        self.check_draw(self.wildstation)
        self.check_draw(self.obstacles)
        self.check_draw(self.grasses)
        self.check_draw(self.walls)
        self.check_draw(self.doors)
        self.check_draw(self.stones)
        self.check_draw(self.portal)
        self.check_draw(self.npcsNormal)
        self.check_draw(self.npcsTrader)
        self.check_draw(self.npcsTrainer)
    
    def CAMERA_spawn(self, x, y):
        self.cameraX = x
        self.cameraY = y

# particular settings for specific scene

class CityScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.GAME_PLAY_CITY
        self.map = Map.gen_city_map()
        self.obstacles = Map.gen_obstacles()
        self.hospital = Map.gen_hospital()
        self.gym = Map.gen_gym()
        self.shop = Map.gen_shop()
        self.citystation = Map.gen_citystation()
        self.background = Map.gen_city_road()
        
        texts = ["We can use computer and smartphone", "to do many things.", "", "How powerful the science is! [ENTER]"]
        self.npcsNormal.add(NPCs.NPCnormal(WindowSettings.width // 3, WindowSettings.height // 2, GamePath.npc, texts))
        
        self.portal.add(Portal.Portal(PortalSettings.Type[0][0] * SceneSettings.tileWidth, PortalSettings.Type[0][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[0][2],
                                      PortalSettings.Type[0][3] * SceneSettings.tileWidth, PortalSettings.Type[0][4] * SceneSettings.tileHeight))
        self.portal.add(Portal.Portal(PortalSettings.Type[2][0] * SceneSettings.tileWidth, PortalSettings.Type[2][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[2][2],
                                      PortalSettings.Type[2][3] * SceneSettings.tileWidth, PortalSettings.Type[2][4] * SceneSettings.tileHeight))
        self.portal.add(Portal.Portal(PortalSettings.Type[4][0] * SceneSettings.tileWidth, PortalSettings.Type[4][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[4][2],
                                      PortalSettings.Type[4][3] * SceneSettings.tileWidth, PortalSettings.Type[4][4] * SceneSettings.tileHeight))
        self.portal.add(Portal.Portal(PortalSettings.Type[6][0] * SceneSettings.tileWidth, PortalSettings.Type[6][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[6][2],
                                      PortalSettings.Type[6][3] * SceneSettings.tileWidth, PortalSettings.Type[6][4] * SceneSettings.tileHeight))

class WildScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.GAME_PLAY_WILD
        self.map = Map.gen_wild_map()
        self.wildstation = Map.gen_wildstation()
        self.obstacles = Map.gen_wild_trees()
        self.grasses = Map.gen_wild_grass()

        texts = ["Walking alone the road you will see tall grass.", "Be careful!", "There are wild Pokemons", "hiding in tall grass! [ENTER]"]
        self.npcsNormal.add(NPCs.NPCnormal(WindowSettings.width // 3, WindowSettings.height // 3 * 2, GamePath.npc, texts))

        self.portal.add(Portal.Portal(PortalSettings.Type[5][0] * SceneSettings.tileWidth, PortalSettings.Type[5][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[5][2],
                                      PortalSettings.Type[5][3] * SceneSettings.tileWidth, PortalSettings.Type[5][4] * SceneSettings.tileHeight))

class HospitalScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.GAME_PLAY_HOSPITAL
        self.map = Map.gen_hospital_map()
        self.obstacles = Map.gen_hospitaledge()
        self.walls = Map.gen_hospital_wall()
        self.doors = Map.gen_hospital_door()

        self.npcsNormal.add(NPCs.NPCnormal(WindowSettings.width // 2, WindowSettings.height // 5 * 2 + 30, GamePath.heal, ["Text"]))
              
        self.portal.add(Portal.Portal(PortalSettings.Type[1][0] * SceneSettings.tileWidth, PortalSettings.Type[1][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[1][2],
                                      PortalSettings.Type[1][3] * SceneSettings.tileWidth, PortalSettings.Type[1][4] * SceneSettings.tileHeight))

class GymScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.GAME_PLAY_GYM
        self.map = Map.gen_gym_map()
        self.obstacles = Map.gen_gymobstacles()
        self.walls = Map.gen_gym_wall()
        self.stones = Map.gen_gym_stone()
        self.background = Map.gen_gym_bg()

        self.npcsTrainer.add(NPCs.NPCtrainer(WindowSettings.width // 2 - 25, WindowSettings.height // 2 + 10, GamePath.npcTrainer1,
                                             0, WindowSettings.height // 6, NPCSettings.npcSpeed * 5, False, [Xatu(30), Claydol(33), Metang(35)]))
        self.npcsTrainer.add(NPCs.NPCtrainer(WindowSettings.width // 3 + 15, WindowSettings.height // 3 + 70, GamePath.npcTrainer2,
                                             0, WindowSettings.height // 12, NPCSettings.npcSpeed * 3, False, [Dusclops(30), Gengar(32)]))
        self.npcsTrainer.add(NPCs.NPCtrainer(WindowSettings.width // 3 * 2 - 30, WindowSettings.height // 3 * 2 - 55, GamePath.npcTrainer3,
                                             0, WindowSettings.height // 12, NPCSettings.npcSpeed * 2, False, [Hariyama(30), Blaziken(32)]))
        
        self.npcsTrainer.add(NPCs.NPCtrainer(WindowSettings.width // 2 - 30, WindowSettings.height // 4 - 70, GamePath.boss, 
                                             0, 0, 0, True, [Metagross(35), Salamence(36), Zapdos(38), Mewtwo(40)]))
        
        self.portal.add(Portal.Portal(PortalSettings.Type[3][0] * SceneSettings.tileWidth, PortalSettings.Type[3][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[3][2],
                                      PortalSettings.Type[3][3] * SceneSettings.tileWidth, PortalSettings.Type[3][4] * SceneSettings.tileHeight))      

class ShopScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.GAME_PLAY_SHOP
        self.map = Map.gen_shop_map()
        self.obstacles = Map.gen_shopedge()
        self.walls = Map.gen_shop_wall()

        self.npcsTrader.add(NPCs.NPCtrader(WindowSettings.width // 2, WindowSettings.height // 4 + 80, GamePath.trader))
        
        self.portal.add(Portal.Portal(PortalSettings.Type[7][0] * SceneSettings.tileWidth, PortalSettings.Type[7][1] * SceneSettings.tileHeight, 
                                      PortalSettings.Type[7][2],
                                      PortalSettings.Type[7][3] * SceneSettings.tileWidth, PortalSettings.Type[7][4] * SceneSettings.tileHeight))



class MainMenuScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.MAIN_MENU
        self.bg = pygame.image.load(GamePath.menu)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))

        self.font = pygame.font.Font(None, DialogSettings.textSize)
        self.text = self.font.render("Press ENTER to start", True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2, WindowSettings.height - 50))

        self.timeCounter = 0
    
    def render(self):
        self.window.blit(self.bg, (0, 0))
        self.timeCounter += 1
        if self.timeCounter >= DialogSettings.flashCD:
            self.window.blit(self.text, self.textRect)
            if self.timeCounter >= DialogSettings.flashCD * 2:
                self.timeCounter = 0
                
class OriginScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.GAME_PLAY_ORIGIN
        self.bg = pygame.image.load(GamePath.origin)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))

    
    def render(self):
        self.window.blit(self.bg, (0, 0))

class EndGameScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.MAIN_MENU
        self.bg = pygame.image.load(GamePath.endgame)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))

    def render(self):
        self.window.blit(self.bg, (0, 0))
