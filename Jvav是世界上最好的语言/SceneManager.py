from Settings import *
from Functions import *
from Player import Player
from Portal import Portal
import pygame
import Scene

class SceneManager:
    def __init__(self,window):
        self.scene=Scene.Scene(window)
        self.state = GameState.MAIN_MENU
        self._window=window
        self._cameraX=0
        self._cameraY=0
        self.isPortalPlaced=[False,False,False]
        self.monsterAliveCount=0
        self.backgroundMusic=None

    def PlayMusic(self,levelID):
        if (levelID>=0):
            self.backgroundMusic=BackgroundMusic.levelBGM[levelID]
        else:
            self.backgroundMusic=BackgroundMusic.bossBGM
        pygame.mixer.music.load(self.backgroundMusic)
        pygame.mixer.music.play(1000000)
    
    def StopMusic(self):
        pygame.mixer.music.stop()

    def GetObstacles(self,level):
        return self.scene.GetObstacles(level)
    
    def GetMonsters(self,level):
        return self.scene.GetMonsters(level)
    
    def GetBullets(self,level):
        return self.scene.GetBullets(level)
    
    def GetPortals(self,level):
        return self.scene.GetPortals(level)
    
    def GetMerchants(self,level):
        return self.scene.GetMerchants(level)

    def testcamera(self):
        print(self._cameraX,self._cameraY)
    
    def UpdateCamera(self,playerX,playerY)->None:
        self._cameraX=playerX
        self._cameraY=playerY

    def check_event_shopping(self, player, keys):
        pass

    def flush_scene(self, levelID: int):
        self.scene = Scene.Scene(self._window, levelID)

    def flush_scenes(self):
        if levelID == 0:
            levelID=1
            self.state=GameState.GAME_PLAY_LEVEL1
            SpawnX, SpawnY = self.scene.GetSpawnpoint(levelID)
            Player.SetGlobalCoor(SpawnX * SceneSettings.tileWidth, SpawnY * SceneSettings.tileHeight)
            Portal.kill()
        if levelID == 1:
            levelID=2
            self.state=GameState.GAME_PLAY_LEVEL2
            SpawnX, SpawnY = self.scene.GetSpawnpoint(levelID)
            Player.SetGlobalCoor(SpawnX * SceneSettings.tileWidth, SpawnY * SceneSettings.tileHeight)
            Portal.kill()

    def BulletUpdate(self,levelID):
        self.scene.bulletsList[levelID].update()

    def MainMenuRender(self):
        self.scene.MainMenuRender()

    def BackgroundRender(self,levelID):
        self.scene.BackgroundRender(levelID,self._cameraX,self._cameraY)

    def ObstacleRender(self,levelID):
        self.scene.ObstacleRender(levelID,self._cameraX,self._cameraY)
    
    def MonsterRender(self,levelID):
        self.scene.MonsterRender(levelID,self._cameraX,self._cameraY)
    
    def BulletRender(self,levelID):
        self.scene.BulletRender(levelID,self._cameraX,self._cameraY)
    
    def PortalRender(self,levelID):
        self.scene.PortalRender(levelID,self._cameraX,self._cameraY)
    
    def NPCRender(self,levelID):
        self.scene.NPCRender(levelID,self._cameraX,self._cameraY)
    
    def IsLevelFinished(self,levelID):
        return self.scene.isRoomExplored[levelID][self.scene._bossRoom[levelID]]
    
    def GetBossRoomCenter(self,levelID):
        roomHash=self.scene._bossRoom[levelID]
        coorX=GetRow(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH+MapSettings.MAX_SIDE_LENGTH//2
        coorY=GetColumn(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH+MapSettings.MAX_SIDE_LENGTH//2
        return (coorX*SceneSettings.tileWidth,coorY*SceneSettings.tileHeight)

    def FillRoomObstacles(self,orderNum:int)->int:
        for level in range(3):
            for i in range(len(self.scene._roughShape[level])):
                roomType=self.scene._roomTypes[level][i]
                if (self.scene._roomTypes[level][i]<0):
                    continue
                room=self.scene._roughShape[level][i]
                topleftX=GetRow(room,MapSettings.MAX_MAP_LENGTH[level])*MapSettings.MAX_SIDE_LENGTH
                topleftY=GetColumn(room,MapSettings.MAX_MAP_LENGTH[level])*MapSettings.MAX_SIDE_LENGTH
                for obstacle in MapSettings.ROOM_OBSTACLES[0][roomType]: # origin <...>[level][roomType]:
                    image=MapImagePaths.OBSTACLES[level][-obstacle[0]-1]
                    globalX=(topleftX+(MapSettings.MAX_SIDE_LENGTH//2-MapSettings.ROOM_LENGTH[roomType]//2)+obstacle[1][0])*SceneSettings.tileWidth
                    globalY=(topleftY+(MapSettings.MAX_SIDE_LENGTH//2-MapSettings.ROOM_LENGTH[roomType]//2)+obstacle[1][1])*SceneSettings.tileHeight
                    destructibility=False
                    if (obstacle[0]==-4):
                        destructibility=True
                    orderNum=self.scene.PlaceObstacle(level,globalX,globalY,image,destructibility,orderNum
                                                      ,ObstacleSettings.obstacleWidth,ObstacleSettings.obstacleHeight)
        return orderNum