import sys
import pygame

from Player import Player
# from Scene import *
from Settings import *
from PopUpBox import *
from Maps import *
def collision ( a: Player,b : pygame.sprite.Group):
    for sprite in b:
        if a.rect.colliderect(sprite.rect):
            if type(b) == Block :
                return True
            # if type(b) == Monster :
            #     pygame.event.post(GameEvent.EVENT_BATTLE)
            #     return True
            # if type(b) == NPC :
            #     pygame.event.post(GameEvent.EVENT_DIALOG)
            #     return True
    return False


