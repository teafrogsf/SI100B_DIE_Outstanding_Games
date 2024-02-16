import pygame
from Pokemon import *
from Settings import *

# npc settings
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = 0
        self.initialPositionX = x
        self.initialPositionY = y
        self.direction = 1
        self.patrollingRangeX = 0
        self.patrollingRangeY = 0

        self.lastCameraX = 0
        self.lastCameraY = 0

        self.talking = False
        self.talkCD = 0
        self.battling = False

    def reset_talkCD(self):
        self.talkCD = NPCSettings.npcTalkCD
    def can_talk(self):
        return self.talkCD == 0

    def update(self, cameraX, cameraY):
        self.rect.x -= (cameraX - self.lastCameraX)
        self.rect.y -= (cameraY - self.lastCameraY)
        self.initialPositionX -= (cameraX - self.lastCameraX)
        self.initialPositionY -= (cameraY - self.lastCameraY)
        self.lastCameraX = cameraX
        self.lastCameraY = cameraY

        if not self.talking and not self.battling:
            if self.patrollingRangeX > 0:
                self.rect = self.rect.move(self.speed * self.direction, 0)
            if self.patrollingRangeY > 0:
                self.rect = self.rect.move(0, self.speed * self.direction)
            if abs(self.rect.x - self.initialPositionX) > self.patrollingRangeX:
                self.direction = -self.direction
                self.image = pygame.transform.flip(self.image, True, False)
            if abs(self.rect.y - self.initialPositionY) > self.patrollingRangeY:
                self.direction = -self.direction
            if self.talkCD > 0:
                self.talkCD -= 1

# player can battle with trainer
class NPCtrainer(NPC):
    def __init__(self, x, y, path, rangeX, rangeY, speed, BOSS:bool, pokemons:list[Pokemon]):
        super().__init__(x, y, path)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight * 1.2))
        self.pokemons = [None, None, None, None, None, None]
        self.pokemonNum = 0
        self.ableToBattle = True
        self.ableToBattlePokeNum = 0
        self.BOSSFlag = BOSS
        self.patrollingRangeX = rangeX
        self.patrollingRangeY = rangeY
        self.speed = speed
        for pokemon in pokemons:
            self.add_pokemon(pokemon)

    def add_pokemon(self, pokemon:Pokemon):
        self.pokemons[self.pokemonNum] = pokemon
        self.pokemonNum += 1
        self.ableToBattlePokeNum += 1

# player can shop at trader
class NPCtrader(NPC):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)
        self.patrollingRangeX = 0
        self.speed = 0

# player can talk with normal npc
class NPCnormal(NPC):
    def __init__(self, x, y, path, texts):
        super().__init__(x, y, path)
        self.patrollingRangeX = 0
        self.speed = 0
        self.texts = texts