import pygame
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.wall_textures = self.load_wall_texture()
        if self.game.map.num:
            self.sky_texture = self.get_texture('resources/sky.png', (WIDTH, HALF_HEIGHT))
        else:
            self.sky_texture = self.get_texture('resources/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        
    def draw(self):
        self.render_background()
        self.render_game_object()
        
    def render_background(self):
        self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.game.screen.blit(self.sky_texture, (-self.sky_offset, 0))
        self.game.screen.blit(self.sky_texture, (-self.sky_offset + WIDTH, 0))
        if self.game.map.num:
            pygame.draw.rect(self.game.screen, (0,0,0), (0, HALF_HEIGHT, WIDTH, HEIGHT))
        else:
            pygame.draw.rect(self.game.screen, (0,0,0), (0, HALF_HEIGHT, WIDTH, HEIGHT))
            
    def render_filter(self):
        if 0.7 * Player_Initial_Health < self.game.player.health < Player_Initial_Health:
            self.player_hurt1()
        if 0.4 * Player_Initial_Health < self.game.player.health <= 0.7 * Player_Initial_Health:
            self.player_hurt2()
        if 0.4 * Player_Initial_Health < self.game.player.health <= 0.4 * Player_Initial_Health:
            self.player_hurt3()
        if -1 < self.game.player.health <= 0.4 * Player_Initial_Health:
            self.player_hurt3()
        
    def player_get_damage(self):
        blood_screen = self.get_texture('resources/blood_screen.png', RES)
        self.game.screen.blit(blood_screen, (0, 0))
        
    def player_get_over(self):
        game_over_image = self.get_texture('resources/game_over.png', RES)
        self.game.screen.blit(game_over_image, (0, 0))
        
    def player_win(self):
        win_image = self.get_texture('resources/win.png', RES)
        self.game.screen.blit(win_image, (0, 0))
       
    def player_hurt1(self):
        hurt_image = self.get_texture('resources/hurt/0.png', RES)
        self.game.screen.blit(hurt_image, (0, 0))
        
    def player_hurt2(self):
        hurt_image = self.get_texture('resources/hurt/1.png', RES)
        self.game.screen.blit(hurt_image, (0, 0))
        
    def player_hurt3(self):
        hurt_image = self.get_texture('resources/hurt/2.png', RES)
        self.game.screen.blit(hurt_image, (0, 0))
        
    def player_hurt4(self):
        hurt_image = self.get_texture('resources/hurt/3.png', RES)
        self.game.screen.blit(hurt_image, (0, 0))
        
    def render_game_object(self):
        list_object = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_object:
            self.game.screen.blit(image, pos)
        
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)
    
    def load_wall_texture(self):
        return{
            1:self.get_texture('resources/wall/wall.png'),
            2:self.get_texture('resources/wall/portal.png'),
            3:self.get_texture('resources/wall/brick.png'),
            4:self.get_texture('resources/wall/royal.png')
            }