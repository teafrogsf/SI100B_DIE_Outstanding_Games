import pygame
from Battle import Battle
from Pokemon import *
from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pokemons=[], x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        super().__init__()

        # update image of player depending on moving orders
        self.images_left = [pygame.image.load(player) for player in GamePath.player_left]
        self.images_left = [pygame.transform.scale(image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for image in self.images_left]
        self.images_right = [pygame.image.load(player) for player in GamePath.player_right]
        self.images_right = [pygame.transform.scale(image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for image in self.images_right]
        self.images_up = [pygame.image.load(player) for player in GamePath.player_up]
        self.images_up = [pygame.transform.scale(image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for image in self.images_up]
        self.images_down = [pygame.image.load(player) for player in GamePath.player_down]
        self.images_down = [pygame.transform.scale(image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for image in self.images_down]
        self.index = 0
        self.images = None
        self.image = self.images_right[self.index]

        self.talking = False
        self.battling = False
        self.encounter = False
        self.encounterCD = 0
        self.battleFailCD = 0
        self.battle = Battle()
        self.colliSys = None
        self.GOTO = None

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.GOTO = None
        self.PortalCD = 0
        self.xspawn = None
        self.yspawn = None

        self.direction = 1
        self.speed = PlayerSettings.playerSpeed
        self.dx = 0
        self.dy = 0

        self.money = 3000
        self.bag = {
            ItemID.pokeBall:10,
            ItemID.posion:1,
        }

        self.pokemons = [None, None, None, None, None, None]
        self.pokemonNum = 0
        self.ableToBattlePokeNum = 0
        self.computer = []
        for pokemon in pokemons:
            self.add_pokemon(pokemon)

    # Pokemon settings
    def add_pokemon(self, pokemon:Pokemon):
        if self.pokemonNum < 6:
            self.pokemons[self.pokemonNum] = pokemon
            self.pokemonNum += 1
            self.ableToBattlePokeNum += 1
        else:
            self.computer.append(pokemon)
            self.pokemonNum += 1

    def release_pokemon(self, ID):
        for i in range(ID + 1, self.pokemonNum):
            if self.pokemons[i] is not None:
                self.pokemons[i - 1], self.pokemons[i] = self.pokemons[i], self.pokemons[i - 1]
        self.pokemons[self.pokemonNum - 1] = None
        self.pokemonNum -= 1
        self.ableToBattlePokeNum -= 1

    def check_able_to_battle(self):
        for pokemon in self.pokemons:
            if pokemon is not None:
                if pokemon.HP > 0:
                    return True
        return False


    # moving update
    def fix_middle(self, dx, dy):
            self.rect = self.rect.move(-dx, -dy)
    def update(self, keys, scene):
        self.encounterCD = max(0, self.encounterCD - 1)
        self.battleFailCD = max(0, self.battleFailCD - 1)

        if self.talking or self.battling:
            self.index = 0
            self.image = self.images[self.index]
            return

        self.dx = 0
        self.dy = 0
        if keys[pygame.K_w] and self.rect.top > 0:
            self.dy -= self.speed
            if not self.direction == "up":
                self.direction = "up"
                self.images = self.images_up
        if keys[pygame.K_s] and self.rect.bottom < WindowSettings.height:
            self.dy += self.speed
            if not self.direction == "down":
                self.direction = "down"
                self.images = self.images_down
        if keys[pygame.K_a] and self.rect.left > 0:
            self.dx -= self.speed
            if not self.direction == "left":
                self.direction = "left"
                self.images = self.images_left
        if keys[pygame.K_d] and self.rect.right < WindowSettings.width:
            self.dx += self.speed
            if not self.direction == "right":
                self.direction = "right"
                self.images = self.images_right

        self.rect = self.rect.move(self.dx, self.dy)
        
        if self.colliSys is not None:
            if self.colliSys.is_colliding_not_move(self):
                self.rect = self.rect.move(-self.dx, -self.dy)
            if self.colliSys.is_colliding_grass(self):
                if self.encounterCD == 0:
                    if self.battle.encounter_wildpoke():
                        self.encounter = True

            if scene.portal is not None:
                for portal in scene.portal:
                    if self.colliSys.is_colliding_portal(self, portal):
                        if self.can_Portal() and keys[pygame.K_f]:
                            self.reset_PortalCD()
                            self.GOTO = portal.GOTO
                            self.xspawn = portal.xspawn
                            self.yspawn = portal.yspawn
                            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH))

        if not any(keys):
            self.index = 0
            self.image = self.images[self.index]
        if keys[pygame.K_SPACE]:
            self.index = 0
            self.images = self.images_right
            self.image = self.images[self.index]
        if any(keys) and not keys[pygame.K_SPACE]:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        self.PortalCD = max(0, self.PortalCD - 1)


    def draw(self, window):
        window.blit(self.image, self.rect)

    def spawn(self):
        self.rect.topleft = (self.xspawn, self.yspawn)
        
    # portal settings
    def reset_PortalCD(self):
        self.PortalCD = PortalSettings.portalCD
    def can_Portal(self):
        return self.PortalCD == 0