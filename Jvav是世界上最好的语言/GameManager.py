import time
import pygame
import sys
from SceneManager import *
from Settings import *
from Functions import *
from Player import Player
from Collision import CollisionSystem
from ui import *
from Shoppingmall import *
from Resource import ResourceSystem
from random import randint
from math import ceil

class GameManager:
    def __init__(self):
        # Window Initialization
        self.window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
        pygame.display.set_caption(WindowSettings.name)

        self.orderNumber = 0
        self.levelID = 0
        self.sceneManager = SceneManager(self.window)
        self.clock = pygame.time.Clock()
        self.isActivated = False
        self.gateOrderL=-1
        self.gateOrderR=-1
        self.SpawnX, self.SpawnY = self.sceneManager.scene.GetSpawnpoint(self.levelID)
        self.player = Player(WindowSettings.width // 2, WindowSettings.height // 2, self.SpawnX, self.SpawnY)
        self.sceneManager.scene.SetSpawnCamera(self.levelID)
        self.sceneManager.state = GameState.MAIN_MENU
        self.roomArea = [] # it's used to judge which room the player is inside
        for level in range(3):
            self.orderNumber = self.sceneManager.scene.PlaceBorderObstacles(level, self.orderNumber) # The wall around the map
            self.orderNumber = self.sceneManager.FillRoomObstacles(self.orderNumber) # Obstacles inside the room
            self.roomArea.append(self.sceneManager.scene.GetRoomArea(level))
            self.orderNumber = self.sceneManager.scene.PlaceNPC(level,self.orderNumber)
        self.playerX, self.playerY = self.player.GetGlobalCoor()
        self.collisionSystem=CollisionSystem()
        self.UISystem=UI(self.window)
        self.resourceSystem=ResourceSystem()

    def update(self):
        self.clock.tick(60)
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == GameState.Game_SWITCH:
                self.sceneManager.flush_scene()

        # Game Menu
        keys = pygame.key.get_pressed()
        if (self.sceneManager.state == GameState.MAIN_MENU):
            self.sceneManager.MainMenuRender()
            pygame.display.flip()
            if (keys[pygame.K_RETURN]):
                self.beginTime=time.time()
                self.levelID = 0
                self.sceneManager.state = GameState.GAME_PLAY_LEVEL0
                self.SpawnX, self.SpawnY = self.sceneManager.scene.GetSpawnpoint(self.levelID)
                self.player.SetGlobalCoor(self.SpawnX * SceneSettings.tileWidth, self.SpawnY * SceneSettings.tileHeight)
                self.sceneManager.PlayMusic(self.levelID)
            else:
                return None
        
        # Activate the room
        self.roomID = self.player.GetRoomID(self.levelID, self.roomArea)
        if (not self.isActivated):
            self.sceneManager.scene.monsterList=[pygame.sprite.Group() for _ in range(3)]
            self.orderNumber,(self.gateOrderL,self.gateOrderR),monsterCnt=self.sceneManager.scene.ActivateRoom(self.levelID,self.roomID,self.orderNumber)
            self.sceneManager.monsterAliveCount=monsterCnt
            if (self.gateOrderL!=-1):
                self.isActivated=True
                if (self.roomID==self.sceneManager.scene._bossRoom[self.levelID]):
                    self.sceneManager.PlayMusic(-1)
        
        # Player change the weapon
        if (keys[pygame.K_c] and self.player.weapon_switch_time==0 and len(self.player.weapons)>1):
            self.player.weaponListIndex=(self.player.weaponListIndex+1)%len(self.player.weapons)
            self.player.weapon_index=self.player.weapons[self.player.weaponListIndex]
            self.player.weapon_switch_time=1

        # Player Movement and Monster Movement
        self.player.MoveUpdate(keys)
        self.player.Shoot()
        self.sceneManager.scene.monsterList[self.levelID].update(0, [])
        self.sceneManager.BulletUpdate(self.levelID)

        # Judge the portion
        isUsingPortion=self.resourceSystem.UsePortion(keys)
        if (isUsingPortion[0]):
            self.player.hp+=PortionSettings.hpPortion
        if (isUsingPortion[1]):
            self.player.mp=max(self.player.mp+PortionSettings.mpPortion,PlayerSettings.playerMP)

        # Collision System
        self.collisionSystem.GetSprites(self.sceneManager.GetObstacles(self.levelID)
                                   , self.sceneManager.GetMonsters(self.levelID)
                                   , self.player
                                   , self.sceneManager.GetBullets(self.levelID)
                                   , self.sceneManager.GetPortals(self.levelID)
                                   , self.sceneManager.GetMerchants(self.levelID)
                                   , self.levelID)
        self.collisionSystem.work()

        # Handle events from collision system
        eventList = pygame.event.get()
        monsterHitList = []
        monsterAttackList = []
        obstacleEliminateList = []
        for event in eventList:
            if (event.type == Events.playerStop):
                self.player.isMoving = False
            if (event.type == Events.monsterStop):
                self.sceneManager.scene.monsterList[self.levelID].update(1, [event.dict[0]])
            if (event.type == Events.monsterAttack):
                monsterAttackList.append(event.dict[0])
            if (event.type == Events.bulletEliminate):
                self.sceneManager.scene.DeleteBullet(self.levelID, [event.dict[0]])
            if (event.type == Events.obstacleDestruction):
                if self.isActivated:
                    obstacleEliminateList.append(event.dict[0])
            if (event.type==Events.playerHit):
                self.player.hp-=event.dict[0]
            if (event.type==Events.monsterHit):
                monsterHitList.append((event.dict[0],event.dict[1]))
            if (event.type==Events.playerShoot):
                dX=event.dict[0][0]-WindowSettings.width//2
                dY=event.dict[0][1]-WindowSettings.height//2
                startX=self.player._globalX+PlayerSettings.playerWidth//2+(PlayerSettings.playerWidth//2)*(dX/(dX**2+dY**2)**0.5)
                startY=self.player._globalY+PlayerSettings.playerHeight//2+(PlayerSettings.playerHeight//2)*(dY/(dX**2+dY**2)**0.5)
                sX=round(BulletSettings.bulletSpeed*dX/(dX**2+dY**2)**0.5) # SpeedX
                sY=round(BulletSettings.bulletSpeed*dY/(dX**2+dY**2)**0.5) # SpeedY
                self.orderNumber=self.sceneManager.scene.PlaceBullet(self.levelID,startX,startY,sX,sY
                                               ,WeaponsSettings.weaponsDamage[self.player.weaponLevel][self.player.weapon_index]*((self.player.weaponLevel+1)**2),1,self.orderNumber)
            if (event.type==Events.levelChange):
                if (keys[pygame.K_f]):
                    if (self.levelID<2):
                        self.levelID+=1
                        self.SpawnX, self.SpawnY = self.sceneManager.scene.GetSpawnpoint(self.levelID)
                        self.player.SetGlobalCoor(self.SpawnX * SceneSettings.tileWidth, self.SpawnY * SceneSettings.tileHeight)
                        self.sceneManager.PlayMusic(self.levelID)
                    else:
                        # Game Success
                        self.endTime=time.time()
                        self.duration=self.endTime-self.beginTime
                        self.UISystem.GameSuccess(int(self.duration*1000)/1000.0)
                        pygame.display.flip()
                        time.sleep(5)
                        sys.exit()
            if (event.type==Events.hpPortionUse):
                self.player.hp+=event.dict[0]
            if (event.type==Events.mpPortionUse):
                self.player.mp=min(self.player.mp+event.dict[0],PlayerSettings.playerMP)
            
            # Merchant and Gambler
            if (event.type==Events.shopActivate and keys[pygame.K_f]):
                shop=ShoppingMall(self.window)
                merchant=event.dict[2]
                shop.GetGoods(event.dict[0],event.dict[1])
                while True:
                    shop.GetMerchant(merchant)
                    shop.GetData(self.player,self.resourceSystem)
                    keys=pygame.key.get_pressed()
                    if (keys[pygame.K_ESCAPE]):
                        break
                    shop.ChangeChoice(keys)
                    shop.BuyItem(keys)
                    shopEventList=pygame.event.get()
                    for shopEvent in shopEventList:
                        if (shopEvent.type!=Events.shopAction):
                            continue
                        goodName=shopEvent.dict[1]
                        if (goodName=="HP Portion"):
                            self.resourceSystem.ChangeMoney(-shopEvent.dict[0])
                            self.resourceSystem.playerPortionCount[0]+=1
                        elif (goodName=="MP Portion"):
                            self.resourceSystem.ChangeMoney(-shopEvent.dict[0])
                            self.resourceSystem.playerPortionCount[1]+=1
                        elif (goodName=="Level up"):
                            self.resourceSystem.ChangeMoney(-shopEvent.dict[0])
                            self.player.weaponLevel+=1
                            self.player.weaponLevel=min(self.player.weaponLevel,1)
                        elif (goodName=="Sniper Rifle"):
                            self.resourceSystem.ChangeMoney(-shopEvent.dict[0])
                            self.player.can_switch_weapon=True
                            if (2 not in self.player.weapons):
                                self.player.weapons.append(2)
                        else:
                            gambleRes=randint(0,ceil(2*self.resourceSystem.playerMoney))
                            gambleRes=gambleRes-self.resourceSystem.playerMoney
                            self.resourceSystem.ChangeMoney(gambleRes)
                    shop.CDUpdate()
                    shop.render()
                    pygame.display.flip()
        
        # Monster move, attack, get hit, judge whether it's dead after handling events
        self.sceneManager.scene.monsterList[self.levelID].update(2, [])
        self.sceneManager.scene.monsterList[self.levelID].update(3, monsterAttackList)
        self.sceneManager.scene.monsterList[self.levelID].update(4, monsterHitList)
        self.sceneManager.scene.monsterList[self.levelID].update(5, [])
        self.sceneManager.scene.DeleteObstacle(self.levelID, obstacleEliminateList)
        
        # Update UI
        self.UISystem.GetPlayerStatus(self.player.hp,self.player.mp
                                      ,self.resourceSystem.playerMoney
                                      ,self.resourceSystem.playerPortionCount[0],self.resourceSystem.playerPortionCount[1])
        
        # Deactivate room
        if (self.sceneManager.monsterAliveCount==0):
            self.sceneManager.scene.DeactivateRoom(self.levelID,self.roomID,self.gateOrderL,self.gateOrderR)
            self.sceneManager.scene.monsterList=[pygame.sprite.Group() for _ in range(3)]
            self.isActivated=False
            if (self.roomID==self.sceneManager.scene._bossRoom[self.levelID]):
                self.sceneManager.StopMusic()
        
        # Change Level
        if (self.sceneManager.IsLevelFinished(self.levelID) and not self.sceneManager.isPortalPlaced[self.levelID]):
            self.sceneManager.isPortalPlaced[self.levelID] = True
            coorX, coorY = self.sceneManager.GetBossRoomCenter(self.levelID)
            self.sceneManager.scene.PlacePortal(self.levelID, coorX - PortalSettings.portalWidth // 2,
                                           coorY - PortalSettings.portalHeight // 2)

        # Player Status Update and Move
        eventList = pygame.event.get()
        for event in eventList:
            if (event.type==Events.monsterAttack):
                self.player.hp-=1
            if (event.type==Events.monsterDeath):
                self.sceneManager.monsterAliveCount-=1
                self.resourceSystem.ChangeMoney(event.dict[0])
            if (event.type==Events.monsterGenerateBullet):
                bulletArgs=event.dict
                self.orderNumber=self.sceneManager.scene.PlaceBullet(self.levelID
                                                                     ,bulletArgs[0],bulletArgs[1],bulletArgs[2],bulletArgs[3],bulletArgs[4],bulletArgs[5]
                                                                     ,self.orderNumber)
        self.player.Move()
        self.playerX, self.playerY = self.player.GetGlobalCoor()

        # Game Fail
        if (self.player.hp<=0):
            self.UISystem.GameFail()
            pygame.display.flip()
            time.sleep(5)
            sys.exit()

        # Render Everything
        self.sceneManager.UpdateCamera(self.playerX, self.playerY)
        self.sceneManager.BackgroundRender(self.levelID)
        self.sceneManager.ObstacleRender(self.levelID)
        self.sceneManager.MonsterRender(self.levelID)
        self.sceneManager.BulletRender(self.levelID)
        self.sceneManager.PortalRender(self.levelID)
        self.sceneManager.NPCRender(self.levelID)
        self.player.render(self.window)
        self.UISystem.display(self.player)

        # Update CDs
        self.player.CDcounter() 
        self.resourceSystem.CDUpdate()