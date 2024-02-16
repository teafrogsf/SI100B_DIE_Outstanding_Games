import pygame
import MapGenerator
import random
import time
from MapGenerator import GetRow,GetColumn
from Obstacles import *
from Settings import *
from Functions import *
from Monsters import *
from Weapons import *
from Portal import *
from Shoppingmall import *
from NPC import *

class Scene:
    def __init__(self,window)->None:
        self._mapShape=[None,None,None]
        self._roomTypes=[None,None,None]
        self._spawnRoom=[None,None,None]
        self._bossRoom=[None,None,None]
        self._roughShape=[None,None,None]
        self._mapObj=[None,None,None]
        self._border=[None,None,None]
        self.isRoomExplored=[]
        self.portal = None
        for i in range(3):
            self._mapShape[i],self._roomTypes[i],self._spawnRoom[i],self._bossRoom[i],self._roughShape[i]=MapGenerator.GenerateMapShape(i)
            self._mapObj[i],self._border[i]=MapGenerator.GenerateMap(self._mapShape[i],i)
            self.isRoomExplored.append([False for _ in range(MapSettings.MAX_MAP_LENGTH[i]**2)])
        self._window=window
        self.width=WindowSettings.width
        self.height=WindowSettings.height

        self.mainMenuImage = pygame.transform.scale(pygame.image.load(MenuImagePaths.menu),
                                                    (WindowSettings.width, WindowSettings.height))
        self.mainMenuFont = pygame.font.Font(None, MenuSettings.textSize)
        self.mainMenuText = self.mainMenuFont.render("Press ENTER to start", True, (255, 255, 255))
        self.mainMenuTextRect = self.mainMenuText.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height - 50))
        self.blinkTimer = 0

        self.obstacleList=[pygame.sprite.Group() for _ in range(3)]
        self.monsterList=[pygame.sprite.Group() for _ in range(3)]
        self.bulletsList=[pygame.sprite.Group() for _ in range(3)]
        self.portalList=[pygame.sprite.Group() for _ in range(3)]
        self.npcList=[pygame.sprite.Group() for _ in range(3)]

    def GetSpawnpoint(self,levelID:int)->(int,int):
        roomHash=0
        maxLength=MapSettings.MAX_SIDE_LENGTH
        maxSize=MapSettings.MAX_MAP_LENGTH[levelID]
        for i in range(len(self._roomTypes[levelID])):
            if (self._roomTypes[levelID][i]==-1):
                roomHash=self._roughShape[levelID][i]
                break
        spawnX=maxLength*GetRow(roomHash,maxSize)+maxLength//2
        spawnY=maxLength*GetColumn(roomHash,maxSize)+maxLength//2
        return (spawnX,spawnY)
    
    def GetRoomType(self,levelID,roomHash): # (-3,-1) means the roomHash doesn't mean a generated room
        roomType=-3
        roomLength=-1
        for i in range(len(self._roughShape[levelID])):
            if (self._roughShape[levelID][i]==roomHash):
                roomType=self._roomTypes[levelID][i]
                break
        if (roomType==-3):
            pass
        elif (roomType>0):
            roomLength=MapSettings.ROOM_LENGTH[roomType]
        elif (roomType==-2):
            roomLength=MapSettings.BOSS_ROOM_LENGTH
        else:
            roomLength=MapSettings.SPAWN_ROOM_LENGTH
        return (roomType,roomLength)
    
    def GetRoomArea(self,levelID):
        res=[((-1,-1),(-1,-1)) for _ in range(MapSettings.MAX_MAP_LENGTH[levelID]**2)]
        for i in range(MapSettings.MAX_MAP_LENGTH[levelID]):
            for j in range(MapSettings.MAX_MAP_LENGTH[levelID]):
                roomHash=Hash(i,j,MapSettings.MAX_MAP_LENGTH[levelID])
                roomType,roomLength=self.GetRoomType(levelID,roomHash)
                delTopL=MapSettings.MAX_SIDE_LENGTH//2-roomLength//2
                topLeft=((i*MapSettings.MAX_SIDE_LENGTH+delTopL)*SceneSettings.tileWidth
                         ,(j*MapSettings.MAX_SIDE_LENGTH+delTopL)*SceneSettings.tileHeight)
                bottomRight=((i*MapSettings.MAX_SIDE_LENGTH+delTopL+roomLength)*SceneSettings.tileWidth-1
                             ,(j*MapSettings.MAX_SIDE_LENGTH+delTopL+roomLength)*SceneSettings.tileHeight-1)
                res[roomHash]=(topLeft,bottomRight)
        return res

    def SetSpawnCamera(self,levelID)->None:
        spawnX,spawnY=self.GetSpawnpoint(levelID)
        self._cameraX=spawnX*SceneSettings.tileWidth
        self._cameraY=spawnY*SceneSettings.tileHeight
    
    def PlaceNPC(self,levelID,orderNum):
        roomType,roomLength=self.GetRoomType(levelID,self._spawnRoom[levelID])
        coorX=GetRow(self._spawnRoom[levelID],MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH
        coorY=GetColumn(self._spawnRoom[levelID],MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH
        coorX+=MapSettings.MAX_SIDE_LENGTH//2-roomLength//2
        coorY+=MapSettings.MAX_SIDE_LENGTH//2-roomLength//2
        coorX*=SceneSettings.tileWidth
        coorY*=SceneSettings.tileHeight
        self.npcList[levelID].add(Gambler(coorX,coorY,orderNum))
        orderNum+=1
        coorX+=roomLength*SceneSettings.tileWidth-NPCSettings.npcWidth
        coorY+=roomLength*SceneSettings.tileHeight-NPCSettings.npcHeight
        self.npcList[levelID].add(Merchant(coorX,coorY,orderNum))
        orderNum+=1
        return orderNum
    
    # Get/Place/Delete sprites(obstacle,monster,bullet,portal)

    def GetObstacles(self,level):
        return self.obstacleList[level]
    
    def GetMonsters(self,level):
        return self.monsterList[level]
    
    def GetBullets(self,level):
        return self.bulletsList[level]
    
    def GetPortals(self,level):
        return self.portalList[level]
    
    def GetMerchants(self,level):
        return self.npcList[level]
    
    # use this function like orderNumber=PlaceBorderObstacles(level,orderNumber)
    def PlaceBorderObstacles(self,levelID:int,orderNum:int)->int:
        for borderPos in self._border[levelID]:
            newObstacle=GenerateObstacle(borderPos[0]*SceneSettings.tileWidth,
                                         borderPos[1]*SceneSettings.tileHeight,
                                         MapImagePaths.BORDER_OBSTACLE,False,orderNum,
                                         ObstacleSettings.obstacleWidth,ObstacleSettings.obstacleHeight)
            self.obstacleList[levelID].add(newObstacle)
            orderNum+=1
        return orderNum
    
    # use this funcion like orderNumber=PlaceObstacle(level,...,orderNumber)
    def PlaceObstacle(self,levelID,globalX,globalY,imgPath,destructibility,orderNum:int,width=ObstacleSettings.obstacleWidth,height=ObstacleSettings.obstacleHeight)->int:
        newObstacle=GenerateObstacle(globalX,globalY,imgPath,destructibility,orderNum,width,height)
        self.obstacleList[levelID].add(newObstacle)
        orderNum+=1
        return orderNum
    
    def DeleteObstacle(self,level,orderNumList):
        deleteList=[]
        for obstacle in self.obstacleList[level]:
            if (obstacle._order in orderNumList):
                deleteList.append(obstacle)
        for obstacle in deleteList:
            self.obstacleList[level].remove(obstacle)

    # use this function like orderNumber=PlaceMonster(level,...,orderNumber)
    def PlaceMonster(self,level,globalX,globalY,monsterType,orderNum)->int:
        if (monsterType>=0):
            newMonster=Monster(globalX,globalY,monsterType,orderNum)
            self.monsterList[level].add(newMonster)
        else:
            newBoss=Boss(globalX,globalY,abs(monsterType+1),orderNum)
            self.monsterList[level].add(newBoss)
        orderNum+=1
        return orderNum
    
    def PlaceBullet(self,level,globalX,globalY,speedX,speedY,damage,origin,orderNum)->int:
        newBullet=Bullet(globalX,globalY,speedX,speedY,damage,origin,orderNum)
        self.bulletsList[level].add(newBullet)
        orderNum+=1
        return orderNum
    
    def DeleteBullet(self,level,orderNumList):
        for bullet in self.bulletsList[level]:
            if (bullet.orderNum in orderNumList):
                self.bulletsList[level].remove(bullet)
                break
    
    def PlacePortal(self,level,globalX,globalY):
        newPortal=Portal(globalX,globalY)
        self.portalList[level].add(newPortal)
    
    # use like orderNum=...
    # return a tuple with:
    # 0:orderNum
    # 1(closed,(-1,-1) if the room isn't activated):(gateOrderBegin,gateOrderEnd)
    # 2:monsterCnt
    def ActivateRoom(self,levelID,roomHash,orderNum):
        roomType,roomLength=self.GetRoomType(levelID,roomHash)
        if (roomHash==-1 or self.isRoomExplored[levelID][roomHash] or roomHash==self._spawnRoom[levelID]):
            return (orderNum,(-1,-1),0)
        # Place Monster
        if (roomType>=0):
            monsterList=MapSettings.ROOM_MONSTERS[roomType]
            monsterCnt=0
            topleftX=GetRow(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH
            topleftY=GetColumn(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH
            for monster in monsterList:
                monsterType=monster[0]+levelID*5-1
                globalX=(topleftX+(MapSettings.MAX_SIDE_LENGTH//2-MapSettings.ROOM_LENGTH[roomType]//2)+monster[1][0])*SceneSettings.tileWidth
                globalY=(topleftY+(MapSettings.MAX_SIDE_LENGTH//2-MapSettings.ROOM_LENGTH[roomType]//2)+monster[1][1])*SceneSettings.tileHeight
                orderNum=self.PlaceMonster(levelID,globalX,globalY,monsterType,orderNum)
                monsterCnt+=1
        elif (roomType==-2):
            topleftX=GetRow(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH+MapSettings.MAX_SIDE_LENGTH//2
            topleftY=GetColumn(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH+MapSettings.MAX_SIDE_LENGTH//2
            globalX=topleftX*SceneSettings.tileWidth-BossSettings.bossWidth//2
            globalY=topleftY*SceneSettings.tileHeight-BossSettings.bossHeight//2
            orderNum=self.PlaceMonster(levelID,globalX,globalY,-levelID-1,orderNum)
            monsterCnt=1
        else:
            return (orderNum,(-1,-1),0)
        # Place Gate
        centerX=GetRow(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH+MapSettings.MAX_SIDE_LENGTH//2
        centerY=GetColumn(roomHash,MapSettings.MAX_MAP_LENGTH[levelID])*MapSettings.MAX_SIDE_LENGTH+MapSettings.MAX_SIDE_LENGTH//2
        gateDirection=[((-roomLength//2,-roomLength//2),(-2,2)),((roomLength//2+1,roomLength//2+1),(-2,2))
                       ,((-2,2),(-roomLength//2,-roomLength//2)),((-2,2),(roomLength//2+1,roomLength//2+1))]
        gateOrderBegin=orderNum
        for direction in gateDirection:
            for x in range(centerX+direction[0][0],centerX+direction[0][1]+1):
                for y in range(centerY+direction[1][0],centerY+direction[1][1]+1):
                    orderNum=self.PlaceObstacle(levelID,x*SceneSettings.tileWidth,y*SceneSettings.tileHeight
                                                ,MapImagePaths.ACTIVATED_GATE,False,orderNum
                                                ,ObstacleSettings.obstacleWidth,ObstacleSettings.obstacleHeight)
        gateOrderEnd=orderNum-1
        return (orderNum,(gateOrderBegin,gateOrderEnd),monsterCnt)
    
    def DeactivateRoom(self,levelID,roomHash,gateOrderBegin,gateOrderEnd):
        self.isRoomExplored[levelID][roomHash]=True
        self.DeleteObstacle(levelID,[i for i in range(gateOrderBegin,gateOrderEnd+1)])
    
    # Renders are below

    def MainMenuRender(self):
        self._window.blit(self.mainMenuImage,(0,0))
        self.blinkTimer += 1
        if self.blinkTimer >= MenuSettings.blinkInterval:
            self._window.blit(self.mainMenuText, self.mainMenuTextRect)
            if self.blinkTimer >= MenuSettings.blinkInterval * 2:
                self.blinkTimer = 0

    def BackgroundRender(self,levelID,cameraX,cameraY):
        centerXCoor=cameraX//SceneSettings.tileWidth
        centerYCoor=cameraY//SceneSettings.tileHeight
        delX=cameraX%SceneSettings.tileWidth
        delY=cameraY%SceneSettings.tileWidth
        mapLen=len(self._mapObj[levelID])
        for i in range(max(0,int(centerXCoor-SceneSettings.tileXnum//2-1)),min(mapLen,int(centerXCoor+SceneSettings.tileXnum//2+2))):
            for j in range(max(0,int(centerYCoor-SceneSettings.tileYnum//2-1)),min(mapLen,int(centerYCoor+SceneSettings.tileYnum//2+2))):
                xDis=centerXCoor-i
                yDis=centerYCoor-j
                self._window.blit(self._mapObj[levelID][i][j], 
                                 (WindowSettings.width//2-SceneSettings.tileWidth*xDis-delX, 
                                WindowSettings.height//2-SceneSettings.tileHeight*yDis-delY))
    
    def ObstacleRender(self,levelID,cameraX,cameraY):
        for obstacle in self.obstacleList[levelID].sprites():
            xCoor=obstacle._globalX
            yCoor=obstacle._globalY
            if (abs(xCoor-cameraX)>WindowSettings.width//2+ObstacleSettings.obstacleWidth
                 or abs(yCoor-cameraY)>WindowSettings.height//2+ObstacleSettings.obstacleHeight):
                continue
            self._window.blit(obstacle.image,(xCoor-cameraX+WindowSettings.width//2,yCoor-cameraY+WindowSettings.height//2))
    
    def MonsterRender(self,levelID,cameraX,cameraY):
        for monster in self.monsterList[levelID].sprites():
            xCoor=monster.globalX
            yCoor=monster.globalY
            if (abs(xCoor-cameraX)>WindowSettings.width//2+MonsterSettings.monsterWidth
                 or abs(yCoor-cameraY)>WindowSettings.height//2+MonsterSettings.monsterHeight):
                continue
            self._window.blit(monster.image,(xCoor-cameraX+WindowSettings.width//2,yCoor-cameraY+WindowSettings.height//2))

    def BulletRender(self,levelID,cameraX,cameraY):
        for bullet in self.bulletsList[levelID].sprites():
            xCoor=bullet.globalX
            yCoor=bullet.globalY
            if (abs(xCoor-cameraX)>WindowSettings.width//2+BulletSettings.bulletWidth
                 or abs(yCoor-cameraY)>WindowSettings.height//2+BulletSettings.bulletHeight):
                continue
            self._window.blit(bullet.image,(xCoor-cameraX+WindowSettings.width//2,yCoor-cameraY+WindowSettings.height//2))
    
    def PortalRender(self,levelID,cameraX,cameraY):
        for portal in self.portalList[levelID].sprites():
            xCoor=portal.globalX
            yCoor=portal.globalY
            if (abs(xCoor-cameraX)>WindowSettings.width//2+PortalSettings.portalWidth
                 or abs(yCoor-cameraY)>WindowSettings.height//2+PortalSettings.portalHeight):
                continue
            self._window.blit(portal.image,(xCoor-cameraX+WindowSettings.width//2,yCoor-cameraY+WindowSettings.height//2))
    
    def NPCRender(self,levelID,cameraX,cameraY):
        for singleNPC in self.npcList[levelID].sprites():
            xCoor=singleNPC.globalX
            yCoor=singleNPC.globalY
            if (abs(xCoor-cameraX)>WindowSettings.width//2+NPCSettings.npcWidth
                 or abs(yCoor-cameraY)>WindowSettings.height//2+NPCSettings.npcWidth):
                continue
            self._window.blit(singleNPC.image,(xCoor-cameraX+WindowSettings.width//2,yCoor-cameraY+WindowSettings.height//2))