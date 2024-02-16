# -*- coding:utf-8 -*-
import sys
import pygame
import PopUpBox
import NPCs
import Maps
from random import randint
from enum import Enum
from Settings import *
from NPCs import *
from PopUpBox import *
from Portal import *
from BgmPlayer import *
# from Collision import *

class Scene():
    def __init__(self, window):
        ##### Your Code Here ↓ #####
        # 初始化
        self.type = SceneType
        self.map = None
        self.dialognpcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height
        self.obstacle = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.pos = (0,0)
        self.monsters = pygame.sprite.Group()
        self.selfbox = None
        ##### Your Code Here ↑ #####
    def trigger_dialog(self,player,keys):
        ##### Your Code Here ↓ #####
        for npc in self.dialognpcs.sprites():
            if pygame.sprite.collide_rect(npc,player):
                if npc.can_talk():
                    if player.EX>0:
                        player.talktovill=3
                    if self.meettext:
                        pass###只要遇见就渲染
                    if keys[pygame.K_e] or (npc.name.value==3 and player.has_lamp == True):
                        self.begindialog=True
                        self.meettext=False
                        player.talking=True
                        npc.talking=True
                    if self.begindialog and self.beginindex<1: 
                        if npc.name.value==2:
                            dialogBoxTemp =PopUpBox.DialogBox(self.window, npc.name.value,
                                      DialogSettings.npcmeettextcontent[npc.name.name][player.talktovill-1]
                                        )
                        else:
                            dialogBoxTemp =PopUpBox.DialogBox(self.window, npc.name.value,
                                      DialogSettings.npcmeettextcontent[npc.name.name][npc.firsttalk]
                                        )
                        dialogBoxTemp.render()
                            #接下来开始剧情选择
                        if npc.choose:
                            if npc.name.value==1:
                                self.choose_dialog(npc,player)
                    if keys[pygame.K_RETURN] and self.begindialog:
                        current_time=pygame.time.get_ticks()
                        if current_time-self.last_space_pressed_time>500:
                            self.beginindex+=1
                            self.last_space_pressed_time=current_time ##对话下标 
                    if npc.name.value==2:        
                        if self.begindialog and 1<=self.beginindex<=DialogSettings.dialognumber[npc.name.value][npc.talktwo][player.talktovill]:           
                            if self.beginindex%2==1:
                                dialogBoxTemp =PopUpBox.DialogBox(self.window, player.talkingindex,
                                        DialogSettings.playertextcontent[npc.name.name][npc.talktwo][player.talktovill][(self.beginindex+1)//2-1]
                                        )
                                dialogBoxTemp.render()
                            else:
                                dialogBoxTemp =PopUpBox.DialogBox(self.window, npc.name.value,
                                        DialogSettings.npctextcontent[npc.name.name][npc.talktwo][player.talktovill][self.beginindex//2-1]
                                        )
                                dialogBoxTemp.render() 
                    elif npc.name.value!=2:
                          if self.begindialog and 1<=self.beginindex<=DialogSettings.dialognumber[npc.name.value][npc.talktwo][npc.talktimes]:           
                            if self.beginindex%2==1:
                                dialogBoxTemp =PopUpBox.DialogBox(self.window, player.talkingindex,
                                        DialogSettings.playertextcontent[npc.name.name][npc.talktwo][npc.talktimes][(self.beginindex+1)//2-1]
                                        )
                                dialogBoxTemp.render()
                            else:
                                dialogBoxTemp =PopUpBox.DialogBox(self.window, npc.name.value,
                                        DialogSettings.npctextcontent[npc.name.name][npc.talktwo][npc.talktimes][self.beginindex//2-1]
                                        )
                                dialogBoxTemp.render()
        ##### Your Code Here ↑ #####
    def choose_dialog(self,npc,player):
        ##先渲染白色矩形
        pygame.draw.rect(self.window,(255,255,255),(DialogSettings.chooserectX,DialogSettings.chooserectY,
                    DialogSettings.chooserectWidth,DialogSettings.chooserectHeight))
        pygame.draw.rect(self.window,(255,255,255),(DialogSettings.chooserectX,DialogSettings.chooserectY+100,
                    DialogSettings.chooserectWidth,DialogSettings.chooserectHeight)) 
        ##再渲染文字                              
        theone=PopUpBox.DialogBox(self.window,GamePath.npc,[''])
        theonetext=theone.font1.render(DialogSettings.choosetextcontent[npc.name.name][0],True,theone.fontColor2)
        theonetext2=theone.font1.render(DialogSettings.choosetextcontent[npc.name.name][1],True,theone.fontColor2)
        tw1,th1=theonetext.get_size()
        tw2,th2=theonetext2.get_size()
        tx1=DialogSettings.chooserectX+DialogSettings.chooserectWidth/2-tw1/2
        ty1=DialogSettings.chooserectY+DialogSettings.chooserectHeight/2-th1/2
        tx2=DialogSettings.chooserectX+DialogSettings.chooserectWidth/2-tw2/2
        ty2=DialogSettings.chooserectY+100+DialogSettings.chooserectHeight/2-th2/2
        theone.window.blit(theonetext,(tx1,ty1))
        theone.window.blit(theonetext2,(tx2,ty2))
        ##检测鼠标位置
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            left_button,_,_=pygame.mouse.get_pressed()
            mouse_x,mouse_y=pygame.mouse.get_pos()
            if mouse_x<=DialogSettings.chooserectX+DialogSettings.chooserectWidth and mouse_x>=DialogSettings.chooserectX:
                if mouse_y<=DialogSettings.chooserectY+DialogSettings.chooserectHeight and mouse_y>DialogSettings.chooserectY:
                    if left_button:
                         npc.talktwo=1
                         npc.choose=False
                         self.beginindex+=1
                         player.backpack.add_item(Items.medicine_bottle,(type.healing,5))
            if mouse_x<=DialogSettings.chooserectX+DialogSettings.chooserectWidth and mouse_x>=DialogSettings.chooserectX:
                if mouse_y<=DialogSettings.chooserectY+100+DialogSettings.chooserectHeight and mouse_y>DialogSettings.chooserectY+100:
                    if left_button:
                        npc.talktwo=2
                        npc.choose=False
                        self.beginindex+=1
                        ##发金币
                        player.backpack.add_achieve('坏孩子：对大叔出言不逊')
                        if npc.talktwo>len(DialogSettings.npctextcontent[npc.name.name]):
                            npc.talktwo=1
    def end_dialog(self,player,keys):
        ##### Your Code Here ↓ #####
        for npc in self.dialognpcs.sprites():
            if pygame.sprite.collide_rect(npc,player):
                if npc.name.value==2:
                    if self.beginindex>DialogSettings.dialognumber[npc.name.value][npc.talktwo][player.talktovill]:
                        npc.talking = False
                        player.talking = False
                        self.begindialog=False
                        self.beginindex=0
                        self.meettext=True
                        npc.reset_talk_CD()
                        npc.firsttalk+=1 
                        player.talktovill+=1     
                        if player.talktovill==2:
                            player.backpack.add_item(Items.wooden_sword,(type.weapon,2))
                            player.backpack.add_item(Items.map)
                        if player.talktovill==3:
                            player.backpack.add_item(Items.cup_noodle)
                            player.backpack.add_achieve('*我吃吃吃：获得泡面')  
                            if player.EX>0:
                                pass
                            else:
                                player.talktovill=1
                else:            
                    if self.beginindex>DialogSettings.dialognumber[npc.name.value][npc.talktwo][npc.talktimes]:
                        npc.talking = False
                        player.talking = False
                        npc.talktimes+=1
                        if npc.name.value == 3:
                            player.backpack.add_item(Items.musty_truth)
                            player.backpack.add_item(Items.magic_wand,(type.magic_wand,1))      
                            player.backpack.add_achieve("*尸体在说话：发现会说话的尸体")  
                        self.begindialog=False
                        self.beginindex=0
                        self.meettext=True
                        npc.reset_talk_CD()
                        npc.firsttalk+=1  
                    if npc.talktimes>len(DialogSettings.npctextcontent[npc.name.name][npc.talktwo]):
                        npc.choose=True
        ##### Your Code Here ↑ #####

    def trigger_battle(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_battle(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def trigger_shop(self, npc, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_shop(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    def get_width(self):
        return WindowSettings.width * WindowSettings.outdoorScale

    def get_height(self):
        return WindowSettings.height * WindowSettings.outdoorScale
    # def update_camera(self, player):
    #     ##### Your Code Here ↓ #####
    #     if player.rect.x > WindowSettings.width /6 *5:
    #         self.cameraX += player.speed
    #         if self.cameraX <self.get_width() - WindowSettings.width:
    #             player.fix_to_middle(player.speed, 0)
    #         else:
    #             self.cameraX = self.get_width() - WindowSettings.width
    #     elif player.rect.x < WindowSettings.width/6 :
    #         self.cameraX -= player.speed
    #         if self.cameraX > 0:
    #             player.fix_to_middle(-player.speed, 0)
    #         else:
    #             self.cameraX = 0
    #     if player.rect.y > WindowSettings.height /4 *3:
    #         self.cameraY += player.speed
    #         if self.cameraY <self.get_height() - WindowSettings.height:
    #             player.fix_to_middle(0,player.speed)
    #         else:
    #             self.cameraY = self.get_height() - WindowSettings.height
    #     elif player.rect.y < WindowSettings.height/4 :
    #         self.cameraY -= player.speed
    #         if self.cameraY > 0:
    #             player.fix_to_middle(0,-player.speed)
    #         else:
    #             self.cameraY = 0
        ##### Your Code Here ↑ #####

    def render_map(self):
        ##### Your Code Here ↓ #####
        # map_x参数不为空时
        # 场景为village_map时，具有移动地图功能
        if(map_info_setting.map_info == 1):
            displacement_settings.village_map_x = max(0, min(displacement_settings.offset_x_max, displacement_settings.village_map_x))
            displacement_settings.village_map_y = max(0, min(displacement_settings.offset_y_max, displacement_settings.village_map_y))
            self.window.blit(self.map, (-displacement_settings.village_map_x,-displacement_settings.village_map_y))
            # self.portals.draw(self.window)
        else:
            # print('self.pos :::: ',self.pos)
            self.window.blit(self.map, self.pos)

    def render_front_obstacle(self):
        if(self.obstacle is not None):
            for obstacle in self.obstacle :
                if obstacle.pos == ObstaclesPos.front:
                    obstacle.draw(self.window)
    def render_behind_obstacle(self):
        if(self.obstacle is not None):
            for obstacle in self.obstacle :
                if obstacle.pos == ObstaclesPos.behind:
                    obstacle.draw(self.window)
            
class StartMenu():
    def __init__(self):
        ##### Your Code Here ↓ #####
        self.map = pygame.transform.scale(pygame.image.load(GamePath.start),(WindowSettings.width,WindowSettings.height))
        ##### Your Code Here ↑ #####

    def render(self,window):
        ##### Your Code Here ↓ #####
        window.blit(self.map,(0,0))
        ##### Your Code Here ↑ #####

class VillageScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        self.map = Maps.gen_village_map()
        self.obstacle = Maps.gen_village_obstacle()
        self.portals = Maps.gen_village_portals()
        self.monsters = self.gen_monsters()
        self.selfbox = SelfBox(selftalking.village,GameState.GAME_PLAY_VILL)
        ##### Your Code Here ↑ #####
    def gen_VILL(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    def gen_monsters(self):
        pass
    
class HouseScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        self.map = Maps.gen_house_map()
        self.obstacle = Maps.gen_house_obstacle()
        self.pos = (315,75)
        self.begindialog=False
        self.meettext=True
        self.beginindex=0
        self.last_space_pressed_time=0
        self.dialognpcs=pygame.sprite.Group()
        self.dialognpcs.add(NPCs.DialogNPC(NPCSettings.dialogposX2,NPCSettings.dialogposY2,dialognpc.village_chief))
        ##### Your Code Here ↑ #####

# 野外场景 2024/01/17
class WildScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.map = Maps.gen_wild_map()
        self.obstacle = Maps.gen_wild_obstacle()
        self.pos = (325,150)
        self.monsters = self.gen_monsters()
    def gen_WILD(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def gen_monsters(self):
        monsters = pygame.sprite.Group()
        return monsters

# boss 场景2024/01/17
class BossScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.map = Maps.gen_boss_map()
        self.obstacle = Maps.gen_boss_obstacle()
        self.pos = (0,0)
        self.selfbox = SelfBox(selftalking.boss,GameState.GAME_PLAY_BOSS)

        
    # Overwrite Scene's function
    def trigger_battle(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def gen_BOSS(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
# 地牢场景 2024/01/17
class DungeonScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.map = Maps.gen_dungeon_map()
        self.obstacle = Maps.gen_dungeon_obstacle()
        self.pos = (0,0)
        self.begindialog=False
        self.meettext=True
        self.beginindex=0
        self.last_space_pressed_time=0
        self.dialognpcs=pygame.sprite.Group()
        self.dialognpcs.add(NPCs.DialogNPC(NPCSettings.dialogposX1,NPCSettings.dialogposY1,dialognpc.merchant))
        self.dialognpcs.add(NPCs.DialogNPC(NPCSettings.dialogposX3,NPCSettings.dialogposY3,dialognpc.ghost))
        self.monsters = self.gen_monster()
    def gen_monster(self):
        monsters = pygame.sprite.Group()
        monsters.add(gen_monster(Monsters.villager))
        monsters.add(gen_monster(Monsters.mimic,10,8))
        monsters.add(gen_monster(Monsters.heretic,15,5))
        monsters.add(gen_monster(Monsters.villager2))
        return monsters
class IndexScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.map = Maps.gen_index_map()
        self.pos = (0,0)
class GameOverScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        self.map = Maps.gen_game_over_map()
        self.pos = (0,0)

class GameVictoryScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        self.map = Maps.gen_game_victory_map()
        self.pos = (0,0)

def gen_monster(monster:Monsters,HP=10,attack=3):
    tmp_monster= Monster(pygame.transform.scale(pygame.image.load(GamePath.monsters[monster.value]),Monster_size[monster.value]))
    tmp_monster.be_poisoned = pygame.image.load(GamePath.monsters_be_poisoned[monster.value])
    tmp_monster.rect.topleft =Monster_pos[monster.value]
    tmp_monster.HP =HP
    tmp_monster.attack = attack
    if monster == Monsters.mimic:
        tmp_monster.is_mimic = True
    return tmp_monster