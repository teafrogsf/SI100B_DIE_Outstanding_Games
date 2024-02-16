from Settings import *

import pygame

# setting portal
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, GOTO:GameState, xspawn, yspawn):
        super().__init__()
        self.image = pygame.image.load(GamePath.portal)
        self.image = pygame.transform.scale(self.image, (PortalSettings.portalWidth, PortalSettings.portalHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.GOTO = GOTO
        self.PortalCD = 0
        self.xspawn = xspawn
        self.yspawn = yspawn
        self.lastCameraX = 0
        self.lastCameraY = 0

    def update(self, cameraX, cameraY):
        self.rect.x -= (cameraX - self.lastCameraX)
        self.rect.y -= (cameraY - self.lastCameraY)
        self.lastCameraX = cameraX
        self.lastCameraY = cameraY
    
    def draw(self, window, dx=0, dy=0):
        window.blit(self.image, self.rect)
    