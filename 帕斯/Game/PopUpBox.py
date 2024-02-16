# -*- coding:utf-8 -*-

import pygame
from Card import Card
from typing import *
from Settings import *
from time import sleep

class DialogBox:
    def __init__(self, window, npc,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] =DialogSettings.fontcolor, 
                 bgColor: Tuple[int, int, int, int] =DialogSettings.bgcolor):
        self.image=pygame.transform.scale(pygame.image.load(GamePath.npc), 
                            (BattleSettings.playerWidth+10, BattleSettings.playerHeight+10))#needs to be fixed
        self.images=[pygame.transform.scale(pygame.image.load(GamePath.tree), (SceneSettings.tileWidth*2, SceneSettings.tileHeight*2)),
                     pygame.transform.scale(pygame.image.load(GamePath.fire[0]), (SceneSettings.tileWidth*1.5, SceneSettings.tileHeight*3)),
                     pygame.transform.scale(pygame.image.load(GamePath.vase), (SceneSettings.tileWidth*2, SceneSettings.tileHeight*2))]
        self.window = window
        self.index=0
        self.playerX = BattleSettings.playerCoordX
        self.playerY = BattleSettings.playerCoordY-70
        # 最基础的字体和背景图片设置
        self.font = pygame.font.Font(None,DialogSettings.fontsize)
        self.font2= pygame.font.Font(None,DialogSettings.font2size)
        self.font3=pygame.font.Font(None,DialogSettings.font3size)
        self.hpfont = pygame.font.Font(None,DialogSettings.hpfontsize)
        self.hpfontcolor=DialogSettings.fontcolor
        self.fontColor=DialogSettings.fontcolor
        self.selectedfontcolor=DialogSettings.selectedfontcolor
        self.donedialog=0
        self.bg = pygame.Surface((BattleSettings.boxWidth,
            BattleSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.firstchoice=0
        self.secondchoice=0
        self.contentx=BattleSettings.boxStartX+300
        self.contenty=BattleSettings.boxStartY+100
        self.selection=0
        self.hintindex=0
        self.pressing=0
        self.pressingw=0
        self.texts=None
        self.selectable=True
        self.title=None
        self.chosing=0
        self.hint=None
        self.example_card_list=pygame.sprite.Group()
        self.informationgetted=0

    def dialogboxdistribute(self):
        if self.firstchoice==0 and self.chosing==1:
            self.firstchoice=self.selection+1
            self.selectable=False
            self.chosing=0
            self.secondchoice=0
            
        if self.firstchoice in [2,3] and self.chosing==1:
            if self.secondchoice==1:
                self.donedialog=1
            else:
                self.secondchoice=1
                self.selectable=False
                self.choing=0
            
        if self.firstchoice==1 and self.chosing==1:
            self.choing=0
            self.donedialog=1
        
        if self.firstchoice==4 and self.chosing==1:
            self.chosing=0
            if self.secondchoice!=7:
                self.secondchoice+=1
            else:
                self.donedialog=1
        if self.firstchoice==5 and self.chosing==1:
            self.chosing=0
            if self.secondchoice==1:
                #print("restart detected")
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_RESTART))
                self.donedialog=1
            else:
                self.secondchoice=1

    def Information(self):
        if self.firstchoice==1:
            if self.secondchoice==0:
                self.dialogimg=self.images[0]
                self.title="Here are information about blocks:"
                self.texts=["BLOCKS:  Unable to go through",
                            "TORCHES: Unable to go through (decoration)",
                            "BOXES:   Attach and press SPACE to break it",
                            "   for example, if the box is on your right,",
                            "   press 'D'and SPACE to break it"
                                                         ]
        if self.firstchoice==2:
            if self.secondchoice==0:
                self.title=""
                self.texts=[
                            "Animals can improve your battle income.",
                            "More rare more gain.The only way to aquire animals",
                            "is buying eggs from merchants,and then you will find one ",
                            "animal of random type appears in your farm after one battle",
                          "                                                        NEXT...."]
            if self.secondchoice==1:
                self.title="ANIMALS' INFORMATION:"
                self.texts=["",
                            "Chicks and fishes are the most common: 10 coin per battle",
                            "Cats are more rare: 20 coin per battle",
                            "Goldenbirds are the most rare: 100 coin per battle",
                            "                                                                That's all"]
        if self.firstchoice==3:
                self.title=None
                self.texts=["AS THE TILTLE SAYS, the game is a simulation of ",
                            "the last days of high school,where your enemies are",
                            "quizs and exams,the further you wander inside the maze,",
                            "the stronger enemy you will meet.If you win the battle,",
                            "coins will be rewarded so that you can improve",
                            "your inital attribute from shopping Npc",
                            "there are 4 easy enemies,2 strong enemies and 1 boss",
                            "When the boss is defeated, the game ends",
                            "                                                                That's all"
                ]
        if self.firstchoice==4:
            if self.secondchoice==0:
                self.title=None
                self.texts=["Collide with monster and your battle begins." ,
                            "SPACE and CLICK are your major input during the game.",
                            "You can select a card by a click.",
                            "Press SPACE and then:",
                            "Check information if you selected just one card;",
                            "Merge two cards into higher level card if you select two same card;",
                            "Play card if you selected three cards",
                            "                                                               NEXT...."
                                ]
            if self.secondchoice==1:
                self.title=None
                self.texts=["",
                            "Regular cards are cards with level written on it,",
                            "LEVEL4 is the highest level",
                            "Special cards have no level and can't be merged",
                            "                                                               NEXT...."]
            if self.secondchoice==2:
                self.title="MAIN STRATAGY OF THE GAME   "                         
                self.texts=["The first GOOD STRATEGY is merge cards as MUCH you can,",
                            "so you will have MORE new cards next round,",
                            "The second one is to ACCUMULATE abundant buff cards",
                            "especially when it comes to harder enemies, ",
                            "their hp are extremely high, and can never be defeated ",
                            "by regular atk, but easily by massive buffs and then trigger",
                            "a huge shoot instantly",
                            "                                                               NEXT...."]
            if self.secondchoice==3:
                self.title="in this situation, you have 3 buff cards and 3 atk cards"
                self.texts=[
                            "the SMART way is play three buff cards in this round, ",
                            "so that your next atk will be extremely improved ",
                            "on the otherhand, you can merge atk cards, so your atk cards",
                            "are integrated, and there will be more new cards in next round"
                            "                                                               NEXT...."]
                self.example_card_list=[Card(0,1,1), Card(0,1,2),Card(0,2,3), Card(2,1,4),Card(2,1,5), Card(2,3,6)]
            if self.secondchoice==4:
                self.title=None
                self.texts=[ "","",
                            "So the suggestion is : ",
                            "merge two level1 atk cards into a level2 card",
                            "                                                               NEXT...."]
            if self.secondchoice==5:
                self.texts=[ "","",
                            "and then, merge the level2 atk and the new-merged level2 atk",
                            "into a level3 atk",
                            "                                                               NEXT...."]
                self.example_card_list=[Card(5,1,1), Card(0,2,2),Card(0,2,3), Card(2,1,4),Card(2,1,5), Card(2,3,6)]
            if self.secondchoice==6:
                self.texts=[ "","",
                            "Finally play 3 buff cards, while leave atk for next round","",
                            "                                                               NEXT...."]
                self.example_card_list=[Card(5,1,1), Card(5,1,2),Card(0,3,3), Card(2,1,4),Card(2,1,5), Card(2,3,6)]
            if self.secondchoice==7:
                self.texts=[ "",
                            "Hope you apply these strategy wisely,",
                            "and I sincerely wish you enjoy the game ",
                            "CREATOR : LijiaLong Xiaoyao",
                            "Good luck love you"
                     
                            "                                                                That's all"]
                self.example_card_list=None
        if self.firstchoice==5:
            self.title=None
            self.texts=["",
                        "Are you sure you want to retart?",
                        "If you just want to quit, the game data will",
                        "be stored in data.txt, but if you restart,",
                        "Game data will be initialize and can never be found!",
                        "press SPACE to restart, press 'n' to leave dialog"
                        ]
        self.informationgetted=1
    def Selection(self):
        if self.firstchoice==0:
            self.title= "WHAT INFORMATION DO YOU NEED?"
            self.texts=[ "About Blocks (DON'T MISS!)",
                        "About Animals",
                    "About Enemys",
                    "About Battle (MUST SEE!)",
                    "Restart the game"
                    ]

    def update_dialog(self):
        self.showbg()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_s]==False:
            self.pressing=0
        if keys[pygame.K_s] and self.pressing==0:
            if self.selection>=4:
                self.selection=0
            else:
                self.selection+=1
            self.pressing=1
        if keys[pygame.K_w]==False:
            self.pressingw=0
        if keys[pygame.K_w] and self.pressingw==0:
            if self.selection==0:
                self.selection=4
            else:
                self.selection-=1
            self.pressingw=1
        if keys[pygame.K_SPACE]==False:
            self.pressings=0
        if keys[pygame.K_SPACE] and self.pressings==0:
            self.chosing=1
            self.pressings=1
            self.informationgetted=0
            self.dialogboxdistribute()
        if keys[pygame.K_n]:
            self.donedialog=1



        #render texts
        if self.selectable:
            self.Selection()
            textbegin=self.contenty+60
            self.window.blit(self.font.render(self.title, True, self.fontColor),(self.contentx, textbegin))
            textbegin+=60
            for i in range(len(self.texts)):
                if i==self.selection:
                    self.window.blit(self.font.render(self.texts[i], True, self.selectedfontcolor),(self.contentx, textbegin)) 
                else:
                    self.window.blit(self.font2.render(self.texts[i], True, self.fontColor),(self.contentx, textbegin)) 
                textbegin+=50
            self.window.blit(self.font3.render(self.hint, True, self.fontColor),(self.contentx+40, textbegin))
        else:
            if self.informationgetted==0:
                self.Information()
            textbegin=self.contenty
            if self.firstchoice==1:
                self.window.blit(self.font.render(self.title, True, self.fontColor),(self.contentx, textbegin))
                textbegin-=80
                for i in range(len(self.texts)):
                    if i<3:
                        textbegin+=120
                        self.window.blit(self.font3.render(self.texts[i], True, self.fontColor),(self.contentx+20, textbegin+20))
                        self.window.blit(self.images[i],(self.contentx-80, textbegin))
                    else:
                        textbegin+=40
                        self.window.blit(self.font3.render(self.texts[i], True, self.fontColor),(self.contentx+120, textbegin+20))
                        
            elif self.firstchoice==4 and self.secondchoice in [3,4,5,6]:
                for cards in self.example_card_list:
                    cards.rendermycard(self.window,cards.rect.x,cards.rect.y)
                for text in self.texts:
                    self.window.blit(self.font3.render(text, True, self.fontColor),(self.contentx-80, textbegin))
                    textbegin+=50 
            else:
                if self.title!=None:
                    self.window.blit(self.font.render(self.title, True, self.fontColor),(self.contentx, textbegin))
                    textbegin+=40
                for text in self.texts:
                    self.window.blit(self.font3.render(text, True, self.fontColor),(self.contentx-80, textbegin))
                    textbegin+=50 

        #hint
        hint="PRESS SPACE"
        self.hintindex+=1
        if self.hintindex%25<16:
            self.window.blit(self.font3.render(hint, True, self.fontColor),(self.contentx-250, self.contenty+400)) 

    def showbg(self):

        #self.npcImg=self.npcimages[4*int((self.index//12)%4)]
        self.window.blit(self.bg, (BattleSettings.boxStartX,
                                   BattleSettings.boxStartY))
        transparent_rect = pygame.Surface((960, 250), pygame.SRCALPHA)
        transparent_rect.fill((0, 0,0, 140))
        self.window.blit(self.image, (self.playerX,
                                          self.playerY+100))

class AniamlgameBox:
    def __init__(self, window, npc,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = AniamlgameBoxSettings.fontcolor, 
                 bgColor: Tuple[int, int, int, int] = AniamlgameBoxSettings.bgcolor):
        self.image=pygame.transform.scale(pygame.image.load(GamePath.npc), 
                            (BattleSettings.playerWidth+10, BattleSettings.playerHeight+10))#needs to be fixed
        self.window = window
        self.index=0
        # 最基础的字体和背景图片设置
        self.npc=npc

        self.pressing=0
        self.selectable=1
        self.font2= pygame.font.Font(None,AniamlgameBoxSettings.font2size)
        self.font3=pygame.font.Font(None,AniamlgameBoxSettings.font3size)
        self.hpfont = pygame.font.Font(None,AniamlgameBoxSettings.hpfontsize)
        self.fontColor=AniamlgameBoxSettings.fontcolor
        self.selectedfontcolor=AniamlgameBoxSettings.selectedfontcolor
        self.donedialog=0
        self.contentx=self.npc.rect.x+50
        self.contenty=self.npc.rect.y
        self.bg = pygame.Surface((BattleSettings.boxWidth//2+50,
            int(BattleSettings.boxHeight//3)), pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.firstchoice=0
        self.secondchoice=0
        self.selection=2
        self.chosing=0
        self.title=None
        self.texts=None
        self.hardlevel=0
        self.pressings=0
        self.pressingw=0

    def dialogboxdistribute(self):
        if self.firstchoice==0 and self.chosing==1:
            if self.selection==0:
                self.firstchoice=1
                self.selectable=1
                self.chosing=0
            if self.selection==1:
                self.firstchoice=2
                self.selectable=0
                self.chosing=0
            if self.selection==2:
                self.donedialog=1
        if self.firstchoice==2 and self.chosing==1:
            self.firstchoice=0
            self.selection=0
            self.selectable=1
            self.chosing=0
        if self.firstchoice==1 and self.chosing==1:
            if self.selection==0:
                self.hardlevel=1
            elif self.selection==1:
                self.hardlevel=2
            elif self.selection==2:
                self.hardlevel=3
            self.donedialog=2
    def Information(self):
        if self.firstchoice==2:
            self.title=None
            self.texts=[
                        "CRAZY WILD ANIMALS IN YOUR GARDEN!",
                        "Follow the RED line BUT don't touch animals!",
                        "Reach torch and then you will get Rewards",
                        "Select difficulty to get even more rewards!",
                        "",
                        "                                        press SPACE to back"]

    def Selection(self):
        if self.firstchoice==0:
            self.title= "HOW  CAN  I  HELP?"
            self.texts=[ 
                        "Start game!",
                      "About this game",
                      "Leave"]
        if self.firstchoice==1:
            self.title="SELECT DIFFICULTY"
            self.texts=[ 
                    "WARM UP   REWARD:10 COINS",
                    "HARD      REWARD:50 COINS",
                    "IMPOSSIBLE REWARD:1000 COINS!"]

    def update_animalgame(self):
        self.window.blit(self.bg, (self.contentx,self.contenty))
        keys=pygame.key.get_pressed()
        if keys[pygame.K_s]==False:
            self.pressing=0
        if keys[pygame.K_s] and self.pressing==0:
            if self.selection>=2:
                self.selection=0
            else:
                self.selection+=1
            self.pressing=1
        if keys[pygame.K_w]==False:
            self.pressingw=0
        if keys[pygame.K_w] and self.pressingw==0:
            if self.selection==0:
                self.selection=2
            else:
                self.selection-=1
            self.pressingw=1
        if keys[pygame.K_SPACE]==False:
            self.pressings=0
        if keys[pygame.K_SPACE] and self.pressings==0:
            self.chosing=1
            self.pressings=1
            self.dialogboxdistribute()


        if self.selectable:
            self.Selection()
            textbegin=self.contenty+20
            self.window.blit(self.font2.render(self.title, True, self.fontColor),(self.contentx+40, textbegin))
            textbegin+=40
            for i in range(len(self.texts)):
                if i==self.selection:
                    self.window.blit(self.font2.render(self.texts[i], True, self.selectedfontcolor),(self.contentx+40, textbegin)) 
                else:
                    self.window.blit(self.font3.render(self.texts[i], True, self.fontColor),(self.contentx+40, textbegin)) 
                textbegin+=30

            
        else:
            self.Information()
            textbegin=self.contenty+20
            if self.title!=None:
                self.window.blit(self.font2.render(self.title, True, self.fontColor),(self.contentx+40, textbegin))
                textbegin+=25
            for text in self.texts:
                self.window.blit(self.font3.render(text, True, self.fontColor),(self.contentx+40, textbegin))
                textbegin+=25

class BattleBox:
    def __init__(self, window, player, monster, fontSize: int = BattleSettings.textSize, 
                 fontColor: Tuple[int, int, int] = BattleSettings.hpfontcolor, bgColor: Tuple[int, int, int, int] = BattleSettings.bgcolor) :
        self.window = window
        # 最基础的字体和背景图片设置
        self.font = pygame.font.Font(None,BattleSettings.fontsize)
        self.font2= pygame.font.Font(None,BattleSettings.font2size)
        self.font3=pygame.font.Font(None,BattleSettings.font3size)
        self.hpfont = pygame.font.Font(None,BattleSettings.hpfontsize)
        self.hpfontcolor=BattleSettings.hpfontcolor
        self.fontColor=BattleSettings.fontcolor
        bglist=[pygame.transform.scale(pygame.image.load(img), (BattleSettings.boxWidth, BattleSettings.boxHeight)) for img in GamePath.background]
        if monster.type<2:
            self.bg=bglist[0]
        elif monster.type==4:
            self.bg=bglist[2]
        else :
            self.bg=bglist[1]
        self.mod = pygame.Surface((BattleSettings.boxWidth, BattleSettings.boxHeight), pygame.SRCALPHA)
        self.mod.fill(BattleSettings.modcolor)
        self.databg = pygame.Surface(BattleSettings.datasize, pygame.SRCALPHA)
        self.databg.fill(BattleSettings.datacolor)
        # 初始化相关角色的参数，没有实际操作的权力
        self.player = player
        self.playeratk=player.ATK
        self.playerHP = player.HP
        self.playerinitialhp=player.HP

        
        self.playerX = BattleSettings.playerCoordX
        self.playerY = BattleSettings.playerCoordY
        
        self.monster = monster
        self.monsteratk=monster.ATK
        self.monsterHP = monster.HP
        self.monsterinitialhp=monster.HP

        
        self.monsterX = BattleSettings.monsterCoordX
        self.monsterY = BattleSettings.monsterCoordY

        #初始化玩家卡牌列表
        self.player_card_list=[Card(5,1,i) for i in range(6)]
        self.selected=[]
        self.monster_card_list=[Card(5,1,i) for i in range(3)]


        #动画，点击等图象变化的帧变量
        self.index=0
        self.images = [pygame.transform.scale(pygame.image.load(img), (BattleSettings.playerWidth, BattleSettings.playerHeight)) for img in GamePath.player]
        self.playerImg=self.images[self.index]
        self.playerImgrect=self.playerImg.get_rect()
        if monster.type<3:
            self.monsterimages = [pygame.transform.scale(pygame.image.load(img), (BattleSettings.monsterWidth, BattleSettings.monsterHeight)) for img in GamePath.monster2]
        else:
            self.monsterimages = [pygame.transform.scale(pygame.image.load(img), (BattleSettings.monsterWidth, BattleSettings.monsterHeight)) for img in GamePath.monster]
        self.monsterImg=self.monsterimages[self.index]
        self.monsterImgrect=self.monsterImg.get_rect()
        self.pressed=0#mouse press detect
        self.leftround=BattleSettings.leftround
        self.win=0
        self.ismyround=1
        self.atkgif=0
        self.actcuregif=0
        self.actlightninggif=0
        self.accumulateatkgifindex=0
        self.enemyactlightninggif=0
        self.roundchangeindex=0
        self.readytoleave=0
        self.retoreenergyindex=0
        self.actrainatkindex=0
        self.gettinginfo=False
        self.hintindex=0
        #战斗过程数据变量
        self.atktimes=0
        self.Accumulated_atk=1
        self.Hp_change=0
        self.real_ATK=0
        self.level4atk=0
        self.mergetimes=0
        self.bestshot=0
        self.sacrificethistime=0
        self.enemyatktimes=0
        self.enemy_Accumulated_atk=1
        self.enemy_realatk=0
        self.enemy_round_count=1
        self.sacrificeatkthistime=0
        self.coin0=0
        self.initialcoin=self.player.initialcoin()
        self.coin=0
    

    def DrawNewCard(self):
        for cards in self.player_card_list:
            if cards.sort==5:
                self.player_card_list=[cards.random_card(self.monster.type) if i==cards else i for i in self.player_card_list]
 
    def Seclect_Card(self):#detect mouse and append pointed cards into a list
        #get key events        
        mousepos=pygame.mouse.get_pos()
        #for trail: show mouse
        for cards in self.player_card_list:
        #select card by mouse
            if cards.sort!=5:
                if pygame.mouse.get_pressed()[0]==False:
                    self.pressed=1           
                if mousepos[0] >= cards.rect.x and mousepos[0]<cards.rect.x+120 and mousepos[1] >cards.rect.y  and mousepos[1]<620  :
                    if pygame.mouse.get_pressed()[0] and self.pressed==1:
                        if len(self.selected)<3 and cards not in self.selected:
                            self.selected.append(cards)
                            cards.rect.y=400

                            #print("choose")
                        elif cards in self.selected:
                            self.selected.remove(cards)

                            cards.rect.y=420
                            #print("dechoose")
                        self.pressed=0
                    else:
                        if len(self.selected)<3 and cards not in self.selected:
                            cards.rect.y=420
                elif cards not in self.selected:
                    cards.rect.y=440
                #cards.rendermycard(self.window)#second render for beauty

    def Mergecards(self):
        if self.mergetimes<3:
            keys=pygame.key.get_pressed()
            if len(self.selected)==2:
                if self.selected[0].sort==self.selected[1].sort and self.selected[0].level==self.selected[1].level and self.selected[0].level<4 and keys[pygame.K_SPACE]:
                    #for cards in self.player_card_list:
                        #print(cards.sort,cards.level,cards.order)
                    for cards in self.player_card_list:
                        if cards.order==self.selected[0].order:
                            cards.sort=5
                            cards.rect.y=440
                        elif cards.order==self.selected[1].order:
                            cards.level+=1
                            cards.rect.y=440
                    self.mergetimes+=1
                    del self.selected[1]
                    del self.selected[0]
                    #for cards in self.player_card_list:
                        #print(cards.sort,cards.level,cards.order)

    def curegif(self):#gif after player play cure cards
        images = [pygame.transform.scale(pygame.image.load(img), 
                        (BattleSettings.playerWidth, BattleSettings.playerHeight)) for img in GamePath.cure]
        image = images[int((self.actcuregif//2)%3)]
        text4 = "+ "+str(int((self.Hp_change)))
        self.window.blit(self.hpfont.render(text4, True, self.hpfontcolor),(BattleSettings.boxStartX+70+self.actcuregif//2,BattleSettings.boxStartY+10)) 
        self.window.blit(image, (BattleSettings.playerCoordX+10,BattleSettings.playerCoordY+10)) 
        if self.actcuregif>40:
            self.actcuregif=0
            self.Hp_change=0
        else:
            self.actcuregif+=1
            #render blood volume change

    def accumulategif(self):#gif of player's accumulate atk
        images = [pygame.transform.scale(pygame.image.load(img), 
                        (200,184)) for img in GamePath.lightshield]
        dizzy=30
        rotate=pygame.transform.rotate
        for i in range(int(self.Accumulated_atk//3)):
            imagee = images[(self.accumulateatkgifindex//2+1+i)%13]
            imagee=rotate(imagee,dizzy*i+10)
            self.window.blit(imagee, (BattleSettings.playerCoordX-30,BattleSettings.playerCoordY-30))
        if self.accumulateatkgifindex==16:
            self.accumulateatkgifindex=1
        else:
            self.accumulateatkgifindex+=1   

        if self.retoreenergyindex>0:
            text = "energy restored: "+str(int(self.Accumulated_atk*10))
            self.window.blit(self.font.render(text, True,BattleSettings.hpfontcolor),(BattleSettings.boxStartX+30,BattleSettings.boxStartY+300)) 
            if self.retoreenergyindex>30:
                self.retoreenergyindex=0
            else:
                self.retoreenergyindex+=1
    def enemyaccumulategif(self):
        images = [pygame.transform.scale(pygame.image.load(img), 
                        (200,184)) for img in GamePath.lightshield]
        dizzy=30
        rotate=pygame.transform.rotate
        for i in range(int(self.enemy_Accumulated_atk//3.2)):
            imagee = images[(self.accumulateatkgifindex//2+1+i)%13]
            imagee=rotate(imagee,dizzy*i+10)
            self.window.blit(imagee,(BattleSettings.monsterCoordX-25,BattleSettings.monsterCoordY-25))
        if self.accumulateatkgifindex==16:
            self.accumulateatkgifindex=1
        else:
            self.accumulateatkgifindex+=1   

    def atk_gif(self):#gif after player's atk
        #lightning gif
        if self.actlightninggif>0:
            images = [pygame.transform.scale(pygame.image.load(img), 
                            (200,184)) for img in GamePath.lightning]
            
            imagee = images[self.actlightninggif//4]
            
            self.window.blit(imagee, (BattleSettings.boxStartX+670,200))
            if self.actlightninggif==16:
                self.actlightninggif=0
            else:
                self.actlightninggif+=1
        # level4 unique: atk rain
        if self.level4atk>1:
            images = [pygame.transform.scale(pygame.image.load(img), 
                            (170,340)) for img in GamePath.rainatk]
            
            imagee = images[self.atkgif%14]
            self.window.blit(imagee, (BattleSettings.boxStartX+730,150))
            if self.atkgif<30:
                text3 = "LEVEL4 ATK : "+str(int(self.level4atk))
                self.window.blit(self.font.render(text3, True, (255,50,50)),(BattleSettings.boxStartX+220+self.atkgif*2,BattleSettings.boxStartY+100)) 

        if self.sacrificethistime==1:
            text = "SACRIFICE effect -20% hp"
            self.window.blit(self.font.render(text, True, (255,50,50)),(BattleSettings.boxStartX+170-self.atkgif,250)) 
        
        if self.sacrificeatkthistime==1:
            text3 = "SACRIFICE ATK -25% hp"
            self.window.blit(self.font.render(text3, True, (255,25,55)),(BattleSettings.boxStartX+540+self.atkgif//2,BattleSettings.boxStartY+150)) 
            #atk effect: enemy hp reduce gif
        

        for i in range(self.atktimes):
            text3 = "- "+str(int(self.real_ATK/(self.atktimes)))
            #print(self.real_ATK)
            self.window.blit(self.font.render(text3, True, (255,255,255)),(BattleSettings.boxStartX+640+self.atkgif+2*i,BattleSettings.boxStartY+250+40*i)) 


        if self.level4atk>1:
            if self.atkgif>80:
                self.real_ATK=0
                self.level4atk=0
                self.atkgif=0
                self.atktimes=0
            else:
                self.atkgif+=1
        else:
            if self.atkgif>40:
                self.real_ATK=0
                self.atkgif=0
                self.atktimes=0
            else:
                self.atkgif+=1
    def enemy_atk_gif(self):#gif after enemy's atk
        #player hp reduce gif
        for i in range(self.enemyatktimes):
            text3 = "- "+str(int(self.enemy_realatk//(self.enemyatktimes)))
            if self.atkgif>0:
                self.window.blit(self.font.render(text3, True, (255,255,255)),(BattleSettings.boxStartX+170+self.atkgif+2*i,250+40*i)) 
        if self.enemy_Accumulated_atk>1:
            #print("built enemy accumlate data change in enemyatkgif")
            text = "energy restored "+str(int(self.enemy_Accumulated_atk*10))
            self.window.blit(self.font.render(text, True, (255,255,255)),(BattleSettings.boxStartX+430,BattleSettings.boxStartY+370)) 
        if self.atkgif>40:
            self.atkgif=0
            self.enemy_realatk=0
            self.enemyatktimes=0
        else:
            self.atkgif+=1
    def Playcards(self):#trigger actchange fuction ,clean selected card list
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and len(self.selected)==3:
            self.act_my_changes()

            for card in self.player_card_list:
                for playedcards in self.selected:
                    if card.order==playedcards.order:
                        card.sort=5
                        card.image=card.images[card.sort]
                        card.rect.y+=40
                        self.selected.remove(card)    
       
    def act_my_changes(self):#change into stage 2        data adjust and trigger animate accordingly
        Hp_change=0
        real_ATK=0
        Accumulate_ATK=0
        #1 player data adjust

        for card in self.selected:
            if card.sort==CardSettings.atk:#card=atk
                enhancement=[CardSettings.atk_boost_1,
                             CardSettings.atk_boost_2,
                             CardSettings.atk_boost_3,
                             card.level4atk]
                real_ATK+=enhancement[card.level-1]
                self.atktimes+=1
                if card.level==CardSettings.level_4:
                    self.level4atk=card.level4atk
            if card.sort==CardSettings.cure:#card=cure
                enhancement=[CardSettings.cure_treat_1,
                             CardSettings.cure_treat_2,
                             CardSettings.cure_treat_3,
                             card.level4cure]
                Hp_change+=enhancement[card.level-1]
            if card.sort==CardSettings.buff:#card=buff-accumulate atk
                enhancement=[CardSettings.buff_enhancement_1,
                             CardSettings.buff_enhancement_2,
                             CardSettings.buff_enhancement_3,
                             card.level4buff]
                Accumulate_ATK+=enhancement[card.level-1]
            if card.sort==CardSettings.sacrifice:
                self.sacrificethistime+=4
                self.sacrificeatkthistime=1
                
        #print(f"hpchange:{Hp_change}  realatk:{int(real_ATK)}  accumulated:{Accumulate_ATK+self.Accumulated_atk}  player informationcheck")    
        if real_ATK!=0:#player atk number adjust and activate animate
            real_ATK=real_ATK*(self.Accumulated_atk+Accumulate_ATK)*self.playeratk          
            if real_ATK>20:
                self.actlightninggif=1
            self.Accumulated_atk=1
        else:
            self.Accumulated_atk+=Accumulate_ATK
            self.retoreenergyindex=1
        if Hp_change>0:#player hp number adjust and activate animate
            self.Hp_change=self.playerinitialhp*Hp_change
            if self.playerHP+self.Hp_change<self.playerinitialhp:
                self.playerHP+=self.Hp_change
            else:
                self.Hp_change=self.playerinitialhp-self.playerHP
                self.playerHP=self.playerinitialhp
        if self.sacrificethistime>0:
            if self.sacrificethistime==1:
                if self.playerHP-self.playerHP*0.2>0:
                    self.playerHP-=self.playerHP*0.2
                    self.atkgif=1
                else:
                    self.playerHP=0

        #print(f"sacrifice contdown{self.sacrificenextime}")
        if self.sacrificeatkthistime==1:   
            if self.monsterHP-self.monsterHP*0.3>0:    
                self.monsterHP-=self.monsterHP*0.3
                self.atkgif=1
            else:
                self.monsterHP=0
        
        self.real_ATK=int(real_ATK)

        #2 enemy hp number adjust

        if self.monsterHP-real_ATK>0:
            self.monsterHP-=int(real_ATK)
        else:
            self.monsterHP=0
        if self.bestshot<int(real_ATK):
            self.bestshot=int(real_ATK)
        self.mergetimes=0
        self.ismyround=0 #change into stage 2
    def act_enemy_change(self):#change into stage 4
        real_atk=0
        Accumulate_ATK=0
        #1 enemy data adjust

        for card in self.monster_card_list:
            if card.sort==CardSettings.margin:#initial enemy card list
                self.monster_card_list=[card.random_card_enemy(self.monster.type) if i==card else i for i in self.monster_card_list]
                                #cauculate card effect accordingly
        for card in self.monster_card_list:        
            if card.sort==CardSettings.atk:#atk
                enhancement=[CardSettings.atk_boost_1,
                             CardSettings.atk_boost_2,
                             CardSettings.atk_boost_3,
                             card.level4atk]
                real_atk+=enhancement[card.level-1]
                self.enemyatktimes+=1
            elif card.sort==CardSettings.buff:#buff
                enhancement=[CardSettings.buff_enhancement_enemy_1,
                             CardSettings.buff_enhancement_enemy_2,
                             CardSettings.buff_enhancement_enemy_3,
                             card.level4buff]
                Accumulate_ATK+=enhancement[card.level-1] 
        #print(f"realatk:{real_atk}  accumulatedatk:{Accumulate_ATK+self.enemy_Accumulated_atk}  in act enemy change")    
        if real_atk!=0:
            real_atk=real_atk*(Accumulate_ATK+self.enemy_Accumulated_atk)*self.monsteratk       
            self.enemy_Accumulated_atk=1#reset accumulate atk
        else:
            self.enemy_Accumulated_atk+=Accumulate_ATK#restore accumulated atk

        
        #2player hp number adjust and activate animate
            
        self.enemy_realatk=int(real_atk)
        #print(self.enemy_realatk)
        if self.playerHP-real_atk>0:#player hp number adjust
            self.playerHP-=int(real_atk)
            self.leftround-=1
        else:
            self.playerHP=0

        self.ismyround=1#change into stage 4

    def animatedonechecker(self):
        if self.actcuregif==0 and self.actlightninggif==0 and self.enemyactlightninggif==0 and self.atkgif==0:
            return True
        else:
            return False
    def gifrender(self):#render stage2 and stage4
        if self.ismyround==0 and self.enemy_round_count==0:
            if self.Hp_change>0:
                self.curegif()
            if self.real_ATK>0 or self.atkgif>0 :
                self.atk_gif()
            #trigger round change animate
            if self.animatedonechecker():
                self.roundchange()
                if self.roundchangeindex==0:
                    self.atktimes=0
                    self.enemy_round_count=1#change into stage 3
        if self.ismyround==1 and self.enemy_round_count==1:
            if self.enemy_realatk>0:
                self.enemy_atk_gif()
            #trigger round change animate
            if self.roundchangeindex>0:
                self.roundchange()
                if self.roundchangeindex==0:
                    self.enemyatktimes=0
                    self.enemy_round_count=0#change back into stage 1
    def roundchange(self):#change round animate
        bg=pygame.transform.scale(pygame.image.load(GamePath.dialog), (900, 200))
        b=pygame.font.SysFont("impact", 50)
        if self.ismyround==0:
            text = b.render("      Enemy round!",True,(20,0,0))
        if self.ismyround==1:
            text = b.render("      Your round!",True,(20,0,0))
        self.window.blit(bg, (BattleSettings.boxStartX+30,BattleSettings.boxStartY+170))
        self.window.blit(text,(BattleSettings.boxStartX+250,BattleSettings.boxStartY+240))
        if self.roundchangeindex<35:
            self.roundchangeindex+=1
        else:
            self.roundchangeindex=0

    def Win(self):
        
        self.player.hadbattle=1
        self.window.blit(self.bg, (BattleSettings.boxStartX,BattleSettings.boxStartY))
        bg=pygame.transform.scale(pygame.image.load(GamePath.winbg), (800, 390))
        b=pygame.font.SysFont("impact", 50)
        c=pygame.font.SysFont("impact", 30)
        self.window.blit(bg, (BattleSettings.boxStartX+80,BattleSettings.boxStartY))
        if self.monsterHP==0 and self.leftround>=0:
            
            self.coin0=int(self.bestshot*self.monster.money*(1+self.leftround/20))
            self.coin=self.coin0+self.initialcoin
            text = b.render("You win! by " + str(20-self.leftround)+"rounds",True,(20,0,0))
            self.window.blit(text,(BattleSettings.boxStartX+300,BattleSettings.boxStartY+200))
            text2 = c.render(f"Your strongest shot : {self.bestshot}" ,False,(20,0,0))
            self.window.blit(text2,(BattleSettings.boxStartX+420,BattleSettings.boxStartY+250))
            text3 = c.render(f"Earned Coin : {self.coin0} + {self.initialcoin}" ,False,(20,0,0))
            self.window.blit(text3,(BattleSettings.boxStartX+420,BattleSettings.boxStartY+280))
        elif self.monsterHP>0 or self.leftround<=0:
            self.coin0=int((self.bestshot*self.monster.money*(1+self.leftround/20))/10)
            self.coin=self.coin0
            text = b.render("You Lose by "+ str(20-self.leftround)+"rounds",True,(20,0,0))
            self.window.blit(text,(BattleSettings.boxStartX+300,BattleSettings.boxStartY+200))
            text2 = c.render(f"Your strongest shot : {self.bestshot}" ,False,(20,0,0))
            self.window.blit(text2,(BattleSettings.boxStartX+440,BattleSettings.boxStartY+250))
            text3 = c.render(f"Earned Coin : {self.coin0}" ,False,(20,0,0))
            self.window.blit(text3,(BattleSettings.boxStartX+440,BattleSettings.boxStartY+280))
            
    def Getinfo(self):

        keys=pygame.key.get_pressed()


        if keys[pygame.K_SPACE] and len(self.selected)==1 :
            self.gettinginfo=True

        if self.gettinginfo==True and pygame.mouse.get_pressed()[0] :
            self.hintindex=0
            self.gettinginfo=False


        if self.gettinginfo==True:
            boxbeginx=BattleSettings.boxStartX
            boxbeginy= BattleSettings.boxStartY+150
            databg = pygame.Surface((960,300), pygame.SRCALPHA)
            databg.fill((100,100,100,250))
            self.window.blit(databg,(boxbeginx, boxbeginy))
            self.selected[0].rendermycard(self.window,boxbeginx+50, boxbeginy+50)
            if self.selected[0].sort==CardSettings.atk:
                enhancement=[CardSettings.atk_boost_1,
                             CardSettings.atk_boost_2,
                             CardSettings.atk_boost_3,
                             self.selected[0].level4atk]
                enhancement2=[CardSettings.atk_boost_1,
                              CardSettings.atk_boost_2,
                              CardSettings.atk_boost_3,
                              "1~10"]
                realatk=self.playeratk*enhancement[self.selected[0].level-1]        
                titles=[ "Card Level:",
                        "Enhancement:" ,
                        "Initial ATK:" ,
                        "Brief:" ,
                        "Special:" ]
                contents=[str(self.selected[0].level),
                          str(enhancement2[self.selected[0].level-1]),
                          str(int(realatk)),
                          str("Reduce EnemyHp "),
                          str("None")]
            if self.selected[0].sort==CardSettings.cure:
                enhancement=[CardSettings.cure_treat_1*10,
                             CardSettings.cure_treat_2*10,
                             CardSettings.cure_treat_3*10,
                             self.selected[0].level4atk]
                enhancement2=["5%","8%","10%","10%~100%"]
                titles=[ "Card Level:",
                        "Brief:" ,
                        "Special:" ]
                contents=[str(self.selected[0].level),
                          str(f"Recover {enhancement2[self.selected[0].level-1]} Hp"),
                          str("None")]

            if self.selected[0].sort==CardSettings.buff:
                enhancement=[CardSettings.buff_enhancement_1,
                             CardSettings.buff_enhancement_2,
                             CardSettings.buff_enhancement_3,
                             self.selected[0].level4atk]
                enhancement2=["120%","150%","200%","100%~1000%"]
                titles=[ "Card Level:",
                        "Buff Effect:" ,
                        "Brief:" ,
                        "Special:" ]
                contents=[str(self.selected[0].level),
                          str(enhancement2[self.selected[0].level-1]),
                          str("Store energy and can greatly improve next Atk "),
                          str("You can kept adding buff cards to accumulate"),
                          str("a huge shot")]
            if self.selected[0].sort==CardSettings.sacrifice:

                titles=["Brief:" ,
                        "",
                        "Special:" ]
                contents=[str("Immediately reduce '25%' of enemy's hp"),
                        str("With a cost of losing 20% hp 3rounds later"),
                        str("Sacrifice is one of the rarest card ,"),
                        str("its attack is strong and regardless of" ),
                        str("player's initial atk, if you are lucky enough to "),
                        str("have more than one sacrifice card, you can play"),
                        str("them in sequence rounds to postpone sacrifice"),
                        "because you can only play one SACRIFICE in a round"]
 
 
            textbegin=boxbeginy+60
            for text in titles:
                self.window.blit(self.font2.render(text, True, self.fontColor),(boxbeginx+200, textbegin)) 
                textbegin+=30
            textbegin=boxbeginy+60
            for text in contents:
                self.window.blit(self.font2.render(text, True, self.fontColor),(boxbeginx+400, textbegin)) 
                textbegin+=30
            hint="Click to back battle"
            self.hintindex+=1
            if self.hintindex%25<16:
                self.window.blit(self.font3.render(hint, True, self.fontColor),(boxbeginx+750, boxbeginy+270)) 
    def Update_card(self):
        self.showbg()
        
        #render player's card
        for cards in self.player_card_list:
            cards.rendermycard(self.window,cards.rect.x,cards.rect.y)
        #render enemy's card
        if self.enemy_round_count==1:
            for cards in self.monster_card_list: #display cards
                cards.renderenemycard(self.window)
        #render accumulate gif
        if self.Accumulated_atk>1:
            self.accumulategif()
        if self.enemy_Accumulated_atk>1:
            self.enemyaccumulategif()
        if self.win==0 :#as long as no winner:
            #STAGE1 player selection and act effect
            if self.ismyround==1 and self.enemy_round_count==0 :
                #draw new card
                if self.gettinginfo==False:
                    self.Seclect_Card() # 1 select card in list by mouse
                    self.Getinfo()      # 2 get card information by "space"
                    self.Mergecards()   # 3 merge 2 cards by "space"
                    self.Playcards()    # 4 play 3 cards selceted by "space"
                else:
                    self.Getinfo()
            #STAGE2 player's animations
            if self.ismyround==0 and self.enemy_round_count==0:
                self.gifrender()
            #STAGE3 enemy's selection and act effect
            if self.ismyround==0 and self.enemy_round_count==1:
                self.act_enemy_change()
                self.sacrificeatkthistime=0
                if self.sacrificethistime==1:
                    self.sacrificethistime=0
            #STAGE4 enemy's animations
            if self.ismyround==1 and self.enemy_round_count==1 :
                self.gifrender()
                #two ways to enter next round
                mousepress=pygame.mouse.get_pressed()#detect change from enemy round to my round
                keys=pygame.key.get_pressed()
                if self.animatedonechecker():
                    if mousepress[0] or keys[pygame.K_SPACE]:
                        #print("detected stage4-stage1 in updatecard")                           
                        self.monster_card_list=[Card(5,1,i) for i in range(3)]
                        self.roundchangeindex=1
                        self.DrawNewCard()
                        if self.sacrificethistime>0:
                            self.sacrificethistime-=1
            #STAGE: one round finished

        if self.monsterHP==0 or self.playerHP==0 or self.leftround==0:#determin whether win
            self.win=1
            self.Win()
            mousepress=pygame.mouse.get_pressed()#detect change from enemy round to my round
            keys=pygame.key.get_pressed()
            if mousepress[0] or keys[pygame.K_SPACE]:
                self.readytoleave=1
                #print("readytoleft")

        if self.index==119:
            self.index=0
        else:
            self.index+=1


        #display mouse to see whether the program working correctly

        #mousepos=pygame.mouse.get_pos()
        #pygame.draw.circle(self.window, (100,0,0), (mousepos[0],mousepos[1]),5, width=0)

    def showbg(self):

        self.playerImg=self.images[self.index]
        self.monsterImg=self.monsterimages[4*int((self.index//12)%4)]
        self.window.blit(self.bg, (BattleSettings.boxStartX,
                                   BattleSettings.boxStartY))
        self.window.blit(self.mod,(BattleSettings.boxStartX, BattleSettings.boxStartY))
        self.window.blit(self.databg,(BattleSettings.boxStartX, BattleSettings.boxStartY))
        self.window.blit(self.playerImg, (self.playerX,
                                          self.playerY))
        self.window.blit(self.monsterImg, (self.monsterX,
                                           self.monsterY))
        #render general information:
        #1 render player hp
        pygame.draw.rect(self.window,(120,20,20), (BattleSettings.boxStartX+20,BattleSettings.boxStartY+10,300,10),0,border_radius=3 )
        pygame.draw.rect(self.window,(240,60,60), (BattleSettings.boxStartX+20,BattleSettings.boxStartY+10,self.playerHP/self.playerinitialhp*300,10),0,border_radius=3 )
        #2 render enmey hp
        pygame.draw.rect(self.window,(120,20,20), (BattleSettings.boxStartX+500,BattleSettings.boxStartY+10,400,10),0,border_radius=3)
        pygame.draw.rect(self.window,(240,60,60), (BattleSettings.boxStartX+500,BattleSettings.boxStartY+10,self.monsterHP/self.monsterinitialhp*400,10),0,border_radius=3)
        text1 = str(int(self.monsterHP))
        self.window.blit(self.hpfont.render(text1, True, self.hpfontcolor),(BattleSettings.boxStartX+530,BattleSettings.boxStartY+10)) 
        text2 = str(int(self.playerHP))
        self.window.blit(self.hpfont.render(text2, True, self.hpfontcolor),(BattleSettings.boxStartX+50,BattleSettings.boxStartY+10))
        #3 render left rounds and atk accumulation:


        text = "Accumulated ATK: " + str(int(self.Accumulated_atk*10))+"0%"
        self.window.blit(self.font2.render(text, True, self.fontColor),
        (BattleSettings.boxStartX+20, BattleSettings.boxStartY+30)) 

        text = "Left round: " + str(self.leftround)
        if self.leftround>3:
            self.window.blit(self.font2.render(text, True, self.fontColor),
            (BattleSettings.boxStartX+250, BattleSettings.boxStartY+60))
        else:
            self.window.blit(self.font2.render(text, True, (255,20,20)),
            (BattleSettings.boxStartX+250, BattleSettings.boxStartY+60))

        text = "My Origin ATK: " + str(int(self.playeratk))
        self.window.blit(self.font2.render(text, True, self.fontColor),
        (BattleSettings.boxStartX+20, BattleSettings.boxStartY+60)) 
        if self.sacrificethistime>0:
            text = "SACRIFICE effect in " + str(self.sacrificethistime-1)+"rounds"
            self.window.blit(self.font2.render(text, True, (230,40,40)),(BattleSettings.boxStartX+20, BattleSettings.boxStartY+110)) 

        text = "Accumulated ATK: " + str(int(self.enemy_Accumulated_atk*10))+"0%"
        self.window.blit(self.font2.render(text, True, self.fontColor),
        (BattleSettings.boxStartX+520, BattleSettings.boxStartY+30)) 

        text = "Enemy Origin ATK: " + str(int(self.monsteratk))
        self.window.blit(self.font2.render(text, True, self.fontColor),
        (BattleSettings.boxStartX+520, BattleSettings.boxStartY+60)) 
class ShoppingBox:
    def __init__(self, window,player,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (20,20,20,200)):
        self.image=[pygame.transform.scale(pygame.image.load(img), (220,220)) for img in GamePath.npcgif]
        self.index3=0
        pygame.transform.flip(self.image[self.index3], True, False)#needs to be fixed
        self.window = window
        self.transparent_rect = pygame.Surface((960, 80), pygame.SRCALPHA)
        self.transparent_rect.fill((200, 200,200, 140))
        self.images=[pygame.transform.scale(pygame.image.load(img), (180,180)) for img in GamePath.store]
        self.eggimg=[pygame.transform.scale(pygame.image.load(img), (56,106)) for img in GamePath.egg]
        self.index=0
        self.hintindex=0
        self.player=player
        self.playerX = BattleSettings.playerCoordX
        self.playerY = BattleSettings.playerCoordY-70
        # 最基础的字体和背景图片设置
        self.font = pygame.font.Font(None, 50)
        self.font2= pygame.font.Font(None, 33)
        self.font3=pygame.font.Font(None,25)
        self.hpfont = pygame.font.Font(None, 15)
        self.hpfontcolor=(255,255,255)
        self.fontColor=(255,255,255)
        self.selectedfontcolor=(255,100,100)
        self.doneshopping=0
        self.bg = pygame.Surface((BattleSettings.boxWidth,
            BattleSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.selection=0
        self.hintindex=0
        self.pressing=0
        self.pressingw=0
        self.index2=-20
        self.title= "WHAT DO YOU NEED?"
        self.text1=["INITIAL ATK +1","INITIAL HP +20","ANIMAL EGG +1","       LEAVE"]
        self.text2=[f"{self.player.price1}$",f"{self.player.price2}$",f"{self.player.price3}$",""]
        self.imgx=BattleSettings.boxStartX+320
        self.imgy=BattleSettings.boxStartY+180
        self.selectionrect = pygame.Surface((160,350), pygame.SRCALPHA)
        self.selectionrect.fill((160,160,160,200))
        self.start=[BattleSettings.boxStartX+230,BattleSettings.boxStartX+410,BattleSettings.boxStartX+590,BattleSettings.boxStartX+760]

    def buy(self):
        if self.selection==0:
            if self.player.money-self.player.price1>0:
                self.player.money-=self.player.price1
                self.player.price1+=80
                self.player.ATK+=1
        if self.selection==1:
            if self.player.money-self.player.price2>0:
                self.player.money-=self.player.price2
                self.player.price2+=50
                self.player.HP+=20
                self.player.OriginHP+=20
        if self.selection==2:
            if self.player.money-self.player.price3>0:
                self.player.money-=self.player.price3
                self.player.price3+=5
                self.player.egg+=1
        if self.selection==3:
            self.doneshopping=1

        self.text1=["INITIAL ATK +1","INITIAL HP +20","ANIMAL EGG +1","     LEAVE"]
        self.text2=[f"{self.player.price1}$",f"{self.player.price2}$",f"{self.player.price3}$",""]

    def update_dialog(self):
        self.showbg()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_d]==False:
            self.pressing=0
        if keys[pygame.K_d] and self.pressing==0:
            if self.selection>=3:
                self.selection=0
            else:
                self.selection+=1
            self.pressing=1
        if keys[pygame.K_a]==False:
            self.pressingw=0
        if keys[pygame.K_a] and self.pressingw==0:
            if self.selection==0:
                self.selection=3
            else:
                self.selection-=1
            self.pressingw=1
        if keys[pygame.K_SPACE]==False:
            self.pressings=0
        if keys[pygame.K_SPACE] and self.pressings==0:
            self.chosing=1
            self.pressings=1
            self.buy()

        #leave dialog
        if pygame.mouse.get_pressed()[0]:
            self.doneshopping=1

    def showbg(self):
        if self.index3==236:
            self.index3=0
        else:
            self.index3+=1
        if self.index==29:
            self.index=0
        else:
            self.index+=1
        if self.index2==20:
            self.index2=-20
        else:
            self.index2+=1
        self.window.blit(self.bg, (BattleSettings.boxStartX,
                                   BattleSettings.boxStartY))

        self.window.blit(self.transparent_rect, (BattleSettings.boxStartX,
                                   BattleSettings.boxStartY))
        
        b=abs(self.index2*10)
        self.selectionrect.fill((160,160,160,b))
        self.window.blit(self.selectionrect,(self.start[self.selection]+20,self.imgy-10))
        #pygame.transform.flip(self.image[self.index3//4], True, False)
        self.window.blit(self.image[self.index3//4], (self.playerX,
                                          self.playerY+150))
        self.window.blit(self.images[0], (
                                          self.start[0],self.imgy))
        self.window.blit(self.images[1], (
                                          self.start[1],self.imgy))
        self.window.blit(self.eggimg[self.index//3], (
                                          self.start[2]+65,self.imgy+70))

        self.window.blit(self.font.render(self.title, True, self.fontColor),(self.imgx-20, self.imgy-80))
        for i in range(len(self.text1)):
            self.window.blit(self.font3.render(self.text1[i], True, self.fontColor),(self.start[i]+30,self.imgy+250)) 
            self.window.blit(self.font3.render(self.text2[i], True, self.fontColor),(self.start[i]+85,self.imgy+275)) 
        
        
        
        
        text = "Coin: " + str(self.player.money)
        self.window.blit(self.font2.render(text, True, (255,255,0)),
        (BattleSettings.boxStartX+20, BattleSettings.boxStartY+30)) 

        text = "My initial ATK: " + str(self.player.ATK)
        self.window.blit(self.font2.render(text, True, (230,230,230)),
        (BattleSettings.boxStartX+270, BattleSettings.boxStartY+30)) 

        text = "My initial HP: " + str(int(self.player.HP))
        self.window.blit(self.font2.render(text, True, (230,230,230)),
        (BattleSettings.boxStartX+520, BattleSettings.boxStartY+30)) 

        text = "My egg: " + str(int(self.player.egg))
        self.window.blit(self.font2.render(text, True, self.fontColor),
        (BattleSettings.boxStartX+770, BattleSettings.boxStartY+30)) 

        hint="Press SPACE "
        self.hintindex+=1
        if self.hintindex%25<16:
            self.window.blit(self.font3.render(hint, True, self.fontColor),(BattleSettings.boxStartX+760, BattleSettings.boxStartY+515)) 