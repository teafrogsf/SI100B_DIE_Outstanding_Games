from Settings import *
import pygame

class Merchant(pygame.sprite.Sprite):
    def __init__(self, globalX, globalY, orderNum):
        super().__init__()
        self.typeID=0
        self.image = pygame.image.load(NPCImagePaths.NPC[0])
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.rect = self.image.get_rect()
        self.globalX=globalX
        self.globalY=globalY
        self.rect.topleft = (globalX, globalY)
        self.orderNum=orderNum

class Gambler(pygame.sprite.Sprite):
    def __init__(self, globalX, globalY, orderNum):
        super().__init__()
        self.typeID=1
        self.image = pygame.image.load(NPCImagePaths.NPC[1])
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.rect = self.image.get_rect()
        self.globalX=globalX
        self.globalY=globalY
        self.rect.topleft = (globalX, globalY)
        self.orderNum=orderNum