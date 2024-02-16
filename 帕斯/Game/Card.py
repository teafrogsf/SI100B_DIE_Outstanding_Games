import pygame
import sys
from Settings import *
import random
import copy
from typing import List
import pygame.gfxdraw
from pygame.locals import *
from Player import Player
from time import sleep

class Card:  #basic information of differernt cards
    def __init__(self,sort,level,order):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (CardSettings.cardWidth, CardSettings.cardHeight)) for img in GamePath.card_backround_list]
        self.sort=sort # It implies the sort of cards occurred in battlebox in the wild.
        self.level=level # It implies the level of cards occurred in battlebox in the wild.
        self.width=CardSettings.marginwidth # marginwidth
        self.order=order
        self.Accumulated_atk=CardSettings.Accumulated_atk
        self.Hp_change=CardSettings.Hp_change
        self.ATK_change=CardSettings.ATK_change
        self.image=self.images[self.sort]
        self.rect = self.image.get_rect()
        self.rect.topleft = (BattleSettings.boxStartX+BattleSettings.dertaX+(order)*BattleSettings.dertaXnum, 
                             BattleSettings.boxStartY+BattleSettings.dertaY)
        self.fontColor=BattleSettings.battlefontcolor   
        self.font = pygame.font.SysFont("impact",CardSettings.fontsize)
        self.font2=pygame.font.SysFont("impact",CardSettings.font2size)
        self.renderlevelcolor=None
        self.position=(self.rect.x+BattleSettings.dx,
                       self.rect.y+BattleSettings.dy,
                       self.rect.width+BattleSettings.dw,
                       self.rect.height+BattleSettings.dh)
        self.rendermodcolor=None
        self.roundtimes=0
        self.colorlist=BattleSettings.battlecolorlist
        self.colorindex=0
        self.level4atk=random.randint(1,10)
        self.level4cure=random.randint(1,10)
        self.level4buff=random.randint(1,10)
        self.text = None
        self.textdata=None
        self.textdatarect=None
        #LEVEL REPRESENTING COLOR 
          #APPEND MARGIN
        self.margin_color=CardSettings.margin_color
    def random_card(self,type):
        if self.sort==CardSettings.margin:
            a=random.randint(1,100) # It implies the possibility for a certain sort of cards to occur,"a,b" below is the same.
            b=random.randint(1,10)  # It implies the possibility for a certain level of cards to occur,"a,b" below is the same.
            sort=CardSettings.atk
            level=CardSettings.level_0
            if type==BattleSettings.type_0:
                if a<=50:#atk
                    sort=CardSettings.atk
                elif a>=40 and a<90:#buff
                    sort=CardSettings.buff
                else:#cure
                    sort=CardSettings.cure
                if b>=2:
                    level=CardSettings.level_1
                else:
                    level=CardSettings.level_2
            if type==BattleSettings.type_1:
                if a<=50:#atk
                    sort=CardSettings.atk
                elif a>=40 and a<90:#buff
                    sort=CardSettings.buff
                else:#cure
                    sort=CardSettings.cure
                if b>=5:
                    level=CardSettings.level_1
                elif b>=2 and b<5:
                    level=CardSettings.level_2
                else:
                    level=CardSettings.level_3
            if type==BattleSettings.type_2:
                if a<=40:#atk
                    sort=CardSettings.atk
                elif a>=40 and a<75:#buff
                    sort=CardSettings.buff
                else:#cure
                    sort=CardSettings.cure   
                if b>=6:
                    level=CardSettings.level_1
                elif b>=2 and b<6:
                    level=CardSettings.level_2
                else:
                    level=CardSettings.level_3      
            if type==BattleSettings.type_3:
                if a<=40:#atk
                    sort=CardSettings.atk
                elif a>=40 and a<70:#buff
                    sort=CardSettings.buff
                elif a>=70 and a<74:
                    sort=CardSettings.sacrifice
                else:#cure
                    sort=CardSettings.cure
                if b>=6:
                    level=CardSettings.level_1
                elif b>=2 and b<6:
                    level=CardSettings.level_2
                else:
                    level=CardSettings.level_3     
            if type==BattleSettings.type_4:
                if a<=40:#atk
                    sort=CardSettings.atk
                elif a>=40 and a<70:#buff
                    sort=CardSettings.buff
                elif a>=70 and a<74:
                    sort=CardSettings.sacrifice
                else:#cure
                    sort=CardSettings.cure
                if b>=6:
                    level=CardSettings.level_1
                elif b>4 and b<6:
                    level=CardSettings.level_2
                elif b>=2 and b<=4:
                    level=CardSettings.level_3  
                else:
                    level=CardSettings.level_4      
            return Card(sort,level,self.order) # The cards finally got.
    def random_card_enemy(self,type):
        if self.sort==5: #if card is empty
            a=random.randint(1,100)
            b=random.randint(1,10)
            sort=CardSettings.atk
            level=CardSettings.level_0
            if type==BattleSettings.type_0:
                if a<=50:#atk
                    sort=CardSettings.atk
                elif a>=40 and a<90:#buff
                    sort=CardSettings.buff
                else:#cure
                    sort=CardSettings.cure
                if b>=2:
                    level=CardSettings.level_1
                else:
                    level=CardSettings.level_2
            if type==BattleSettings.type_1:
                if a<=50:#atk
                    sort=CardSettings.atk
                elif a>=40 and a<90:#buff
                    sort=CardSettings.buff
                else:#cure
                    sort=CardSettings.cure
                if b>=5:
                    level=CardSettings.level_1
                elif b>2 and b<5:
                    level=CardSettings.level_2
                else:
                    level=CardSettings.level_3
            if type==BattleSettings.type_2:
                if a<=40:#atk
                    sort=CardSettings.atk
                else:
                    sort=CardSettings.buff
                if b>=5:
                    level=CardSettings.level_1
                elif b>2 and b<5:
                    level=CardSettings.level_2
                else:
                    level=CardSettings.level_3     
            if type==BattleSettings.type_3:
                if a<=40:#atk
                    sort=CardSettings.atk
                else:
                    sort=CardSettings.buff
                if b>=6:
                    level=CardSettings.level_1
                elif b>2 and b<6:
                    level=CardSettings.level_2
                else:
                    level=CardSettings.level_3     
            if type==BattleSettings.type_4:
                if a<=40:#atk
                    sort=CardSettings.atk
                else:#buff
                    sort=CardSettings.buff

                if b>=6:
                    level=CardSettings.level_1
                elif b>4 and b<6:
                    level=CardSettings.level_2
                elif b>2 and b<=4:
                    level=CardSettings.level_3  
                else:
                    level=CardSettings.level_4      
            return Card(sort,level,self.order) # The cards enemy finally got.
    def update_card(self):
            #color 
            if self.level<CardSettings.level_4:
                content_color =self.colorlist[self.level-1]
            if self.level==CardSettings.level_4:   # Changing color of level4 card
                if self.colorindex<CardSettings.card_level_4_depth*6-CardSettings.error:
                    self.colorindex+=CardSettings.derta_depth
                else:
                    self.colorindex=CardSettings.card_level_4_depth*0
                i=self.colorindex
                if i<CardSettings.card_level_4_depth: # Color changing
                    a=i
                    b=CardSettings.card_level_4_depth
                    c=CardSettings.card_level_4_depth*0
                elif CardSettings.card_level_4_depth<=i<CardSettings.card_level_4_depth*2: # Color changing
                    a=CardSettings.card_level_4_depth
                    b=CardSettings.card_level_4_depth*2-i
                    c=CardSettings.card_level_4_depth*0
                elif CardSettings.card_level_4_depth*2<=i<CardSettings.card_level_4_depth*3: # Color changing
                    a=CardSettings.card_level_4_depth
                    b=CardSettings.card_level_4_depth*0
                    c=i-CardSettings.card_level_4_depth*2
                elif CardSettings.card_level_4_depth*3<=i<CardSettings.card_level_4_depth*4: # Color changing
                    a=CardSettings.card_level_4_depth*4-i
                    b=CardSettings.card_level_4_depth*0
                    c=CardSettings.card_level_4_depth
                elif CardSettings.card_level_4_depth*4<=i<CardSettings.card_level_4_depth*5: # Color changing
                    a=CardSettings.card_level_4_depth*0
                    b=i-CardSettings.card_level_4_depth*4
                    c=CardSettings.card_level_4_depth
                elif CardSettings.card_level_4_depth*5<=i<CardSettings.card_level_4_depth*6: # Color changing
                    a=CardSettings.card_level_4_depth*0
                    b=CardSettings.card_level_4_depth
                    c=CardSettings.card_level_4_depth*6-i
                content_color=[a,b,c]

            self.renderlevelcolor = pygame.Surface(CardSettings.renderlevelsize, pygame.SRCALPHA)
            if self.sort in CardSettings.sort_tuple:
                self.renderlevelcolor.fill(content_color) # Color presented!

            #information 
                self.text = "Level"+str(self.level)
                if self.sort==CardSettings.atk:#atk
                    a=[CardSettings.atk_boost_1,
                       CardSettings.atk_boost_2,
                       CardSettings.atk_boost_3,
                       "???"]
                    self.textdata = self.font2.render(str(a[self.level-1]),True,CardSettings.font2color)
                if self.sort==CardSettings.cure:#cure
                    a=["5%",
                       "8%",
                       "10%",
                       "???"]
                    self.textdata = self.font2.render("+"+str(a[self.level-1]),True,CardSettings.font2color)
                if self.sort==CardSettings.buff:#buff
                    a=["120%",
                       "150%",
                       "200%",
                       "???"]
                    self.textdata = self.font2.render("x"+str(a[self.level-1]),True,CardSettings.font2color)
                self.textdatarect=self.textdata.get_rect()
                self.textdatarect.x=self.rect.x+(CardSettings.cardWidth-self.textdatarect.width)//2+5
                self.textdatarect.y=self.rect.y+138
        
            
            #light mod
            self.rendermodcolor = pygame.Surface(CardSettings.rendermodsize, pygame.SRCALPHA)
            self.rendermodcolor.fill(CardSettings.modcolor)
            self.image=self.images[self.sort]

            #position
            self.position=(self.rect.x+2,self.rect.y+2,self.rect.width+6,self.rect.height+5)

    def rendermycard(self,window,x,y):
        self.update_card()#update card's imformation
        #and then display them 

        window.blit(self.image,(x+self.width,y+self.width))
        window.blit(self.renderlevelcolor, (x+5,y+140))
        pygame.draw.rect(window,self.margin_color,(x+2,y+2,self.rect.width+6,self.rect.height+5),self.width,border_radius=9 )
        window.blit(self.rendermodcolor, (x,y)) 
        if self.sort in CardSettings.sort_tuple:
            self.textdatarect.x=x+(CardSettings.cardWidth-self.textdatarect.width)//2+5
            self.textdatarect.y=y+138
            window.blit(self.font.render(self.text, 
                                         True,
                                         CardSettings.fontcolor),
                                         (x+CardSettings.dx,
                                            y+CardSettings.dy,
                                            CardSettings.dw,
                                            CardSettings.dh))
            window.blit(self.textdata,
                        self.textdatarect)
    def renderenemycard(self,window):
        self.update_card()#update card's imformation
        #and then display them 
        self.rect.x=BattleSettings.boxStartX+400+110*self.order
        self.rect.y=BattleSettings.boxStartY+140
        window.blit(self.image,
                    (self.rect.x+self.width,
                     self.rect.y+self.width))
        window.blit(self.renderlevelcolor,
                     (self.rect.x+5,
                      self.rect.y+140))
        pygame.draw.rect(window,self.margin_color, 
                         self.position,
                         self.width,
                         border_radius=9 )
        window.blit(self.rendermodcolor, 
                    (self.rect.x,
                     self.rect.y)) 
        if self.sort in CardSettings.sort_tuple:
            window.blit(self.font.render(self.text, 
                                         True,
                                         CardSettings.fontcolor),
                        (self.rect.x+CardSettings.dx,
                         self.rect.y+CardSettings.dy,
                         CardSettings.dw,
                         CardSettings.dh))
            window.blit(self.textdata,
                        self.textdatarect)

