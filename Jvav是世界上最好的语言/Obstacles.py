import pygame
from Settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,globalX,globalY,imgPath,destructibility,orderNum,width=ObstacleSettings.obstacleWidth,height=ObstacleSettings.obstacleHeight):
        super().__init__()
        self._globalX=globalX
        self._globalY=globalY
        self.image=pygame.transform.scale(pygame.image.load(imgPath),(width,height))
        self.rect=self.image.get_rect()
        self.rect.topleft=(self._globalX,self._globalY)
        self.isDestructible=destructibility
        self._isAlive=True
        self._order=orderNum
    
    def __repr__(self):
        return str(self._globalX)+' '+str(self._globalY)
    
    def GetSpriteType(self):
        return 0

    def GetGlobalCoor(self):
        return (self._globalX,self._globalY)
    
    def TryKill(self)->bool:# return True if successfully change self._is_alive
        if (self._is_destructible):
            self._is_alive=False
            return True
        else:
            return False

    def IsAlive(self)->bool:
        return self._isAlive

def GenerateObstacle(xPos,yPos,imagePath,isDestructible,orderNumber,obstacleWidth,obstacleHeight):
    return Obstacle(xPos,yPos,imagePath,isDestructible,orderNumber,width=obstacleWidth,height=obstacleHeight)