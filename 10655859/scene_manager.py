import pygame
from settings import *
from map import *

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.enable = False
        
        self.counter3 = 0
        self.counter7 = 0
        self.counter11 = 0
        self.counter19 = 0
        
        self.font = pygame.font.Font(None, 60)
        self.text1 = self.font.render('Press F to Enter the Portal', True, 'white')
        self.text2 = self.font.render('DO NOT RUN AWAY FROM A FIGHT', True, 'red')
        self.font1 = pygame.font.Font(None, 30)
        self.text3 = self.font1.render('Wow, didn\'t know we were playing hide and seek', True, 'white')
        self.text4 = self.font1.render('You\'re really good at hiding. Fighting? Not so much.', True, 'white')
        self.text5 = self.font1.render('Did you let your cat play that? That was purr-fectly hilarious!', True, 'white')
        self.text6 = self.font1.render('You\'re the real MVP... Most Valuable Punching bag', True, 'white')
        self.text7 = self.font1.render('You must be a great diplomat because you avoid conflict like a pro.', True, 'white')
        self.text8 = self.font1.render('Your gameplay is like a mystery novel - full of unexpected twists', True, 'white')
        self.text9 = self.font1.render('and nobody knows what you\'re doing. Not even you.', True, 'white')
        self.text10 = self.font1.render('Are you roleplaying as a pacifist, or is it your shooting style?', True, 'white')
        self.text11 = self.font1.render('Were you playing with your eyes closed?', True, 'white')
        self.text12 = self.font1.render('That aim was out of this world... literally.', True, 'white')
        self.text13 = self.font1.render('I guess you\'re playing on hard mode,', True, 'white')
        self.text14 = self.font1.render('where the goal is to miss every shot, right?', True, 'white')
        self.text15 = self.font1.render('Is your controller upside down? That would explain a lot.', True, 'white')
        self.text16 = self.font1.render('I think your character might be pacifist; they refuse to hit anyone.', True, 'white')
        self.text17 = self.font1.render('You\'ve really mastered the art of giving the enemy a false sense of skill.', True, 'white')
        self.text18 = self.font1.render('Your strategy is so secret, even you don\'t know what you\'re doing.', True, 'white')
        self.text19 = self.font1.render('You\'re not lagging, you\'re just on a \'strategic delay\', right?', True, 'white')
        
    def portal_detection(self):
        self.enable = False
        if self.game.player.map_pos == (1, 2) or self.game.player.map_pos == (self.game.map.map_width - 2, self.game.map.map_length - 2):
            if not self.game.map.object_list.victory_counter:
                self.game.screen.blit(self.text2, (500, 700))
            else:
                self.game.screen.blit(self.text1, (600, 700))
                self.enable = True
                
    def language(self):
        if self.game.player.key[pygame.K_s]:
            self.counter3 = 15
        if self.game.map.object_list.num_npc == 0:
            self.counter7 = 5
        if not self.game.player.key[pygame.K_w]:
            self.counter19 = 5
        if self.game.weapon.animation_trigger:
            if self.counter3 > 0:
                self.counter3 -= 1
            if self.counter7 > 0:
                self.counter7 -= 1
            if self.counter11 > 0:
                self.counter11 -= 1
            if self.counter19 > 0:
                self.counter19 -= 1
        if self.game.player.health < 80:
            self.game.screen.blit(self.text10, (100, 400))
            self.game.screen.blit(self.text5, (1000, 300))
        if self.game.player.health < 80 and self.counter19:
            self.game.screen.blit(self.text19, (25, 700))
        if self.game.player.health < 60:
            self.game.screen.blit(self.text6, (25, 650))
            self.game.screen.blit(self.text17, (875, 500))
        if self.game.player.health < 60 and self.counter7:
            self.game.screen.blit(self.text7, (950, 700))
        if self.game.player.health < 70:
            self.game.screen.blit(self.text8, (800, 775))
            self.game.screen.blit(self.text9, (800, 800))
            self.game.screen.blit(self.text18, (25, 500))
        if self.counter3:
            self.game.screen.blit(self.text3, (575, 575))
            self.game.screen.blit(self.text4, (575, 600))
            self.game.screen.blit(self.text15, (475, 250))
        if self.counter11:
            self.game.screen.blit(self.text11, (1100, 375))
            self.game.screen.blit(self.text12, (1100, 400))
            self.game.screen.blit(self.text13, (125, 750))
            self.game.screen.blit(self.text14, (125, 775))
            self.game.screen.blit(self.text16, (50, 325))