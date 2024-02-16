# -*- coding:utf-8 -*-

import sys
import pygame

from Player import Player
from Scene import *
from Settings import *
from PopUpBox import *

class GameManager:
    def __init__(self):
        
        ##### Your Code Here ↓ #####
        self.window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height),pygame.SRCALPHA)
        self.player = Player(init_player_pos.boss_x, init_player_pos.boss_y)#玩家初始位置
        self.clock = pygame.time.Clock()
        self.scene = IndexScene(self.window)#初始地图是游戏首页选择
        self.state = GameState.GAME_INDEX
        self.battle_box = BattleBox(Player,Monster)
        self.win = False
        ##### Your Code Here ↑ #####

    def game_reset(self):
        self.bgm = BgmPlayer()
        ##### Your Code Here ↓ #####
        pygame.display.set_caption(WindowSettings.name)
        self.bgm.play()
        self.tick(30)
        ##### Your Code Here ↑ #####

    # Necessary game components here ↓
    def tick(self, fps):
        ##### Your Code Here ↓ #####
        self.clock.tick(fps)
        ##### Your Code Here ↑ #####

    def get_time(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Scene-related update functions here ↓
    def flush_scene(self,map = None):
        ##### Your Code Here ↓ #####
        if self.state == GameState.GAME_PLAY_VILL and map == GameState.GAME_PLAY_HOUSE:
            self.scene = HouseScene(self.window)
            self.state = GameState.GAME_PLAY_HOUSE
            self.player.rect.x = init_player_pos.house_x
            self.player.rect.y = init_player_pos.house_y
        # 切换到野外（wild）场景
        elif self.state == GameState.GAME_PLAY_VILL and map == GameState.GAME_PLAY_WILD:
            self.scene = WildScene(self.window)
            self.state = GameState.GAME_PLAY_WILD
            self.player.rect.x = init_player_pos.wild_x
            self.player.rect.y = init_player_pos.wild_y
        # 切换到地牢（dungeon）场景
        elif self.state == GameState.GAME_PLAY_VILL and map == GameState.GAME_PLAY_DUNGEON:
            self.scene = DungeonScene(self.window)
            self.state = GameState.GAME_PLAY_DUNGEON
            self.player.rect.x = init_player_pos.dungeon_x
            self.player.rect.y = init_player_pos.dungeon_y
        # house返回到乡村（village）场景
        elif self.state == GameState.GAME_PLAY_HOUSE and map == GameState.GAME_PLAY_VILL:
            self.scene = VillageScene(self.window)
            self.state = GameState.GAME_PLAY_VILL
            self.player.rect.x = HouseTransmitVillageSettings.house_back_player_x
            self.player.rect.y = HouseTransmitVillageSettings.house_back_player_y
        # 地牢返回到乡村（village）场景
        elif self.state == GameState.GAME_PLAY_DUNGEON and map == GameState.GAME_PLAY_VILL:
            self.scene = VillageScene(self.window)
            self.state = GameState.GAME_PLAY_VILL
            self.player.rect.x = DungeonToVillageSettings.dungeon_back_player_x
            self.player.rect.y = DungeonToVillageSettings.dungeon_back_player_y
        # 野外切换到Boss场景
        elif self.state == GameState.GAME_PLAY_WILD and map == GameState.GAME_PLAY_BOSS:
            self.scene = BossScene(self.window)
            self.state = GameState.GAME_PLAY_BOSS
            self.player.rect.x = init_player_pos.boss_x
            self.player.rect.y = init_player_pos.boss_y
        elif self.state == GameState.GAME_INDEX and map == GameState.GAME_PLAY_VILL:
            self.scene = VillageScene(self.window)
            self.state = GameState.GAME_PLAY_VILL
            self.player.rect.x = init_player_pos.village_x
            self.player.rect.y = init_player_pos.village_y
        # 游戏失败
        elif  map == GameState.GAME_OVER:
            self.scene = GameOverScene(self.window)
            self.state = GameState.GAME_OVER
        # 游戏胜利
        elif self.state == GameState.GAME_PLAY_BOSS and map == GameState.GAME_VICTORY:
            self.scene = GameVictoryScene(self.window)
            self.state = GameState.GAME_VICTORY
        ##### Your Code Here ↑ #####

    def update(self):
        collisionFlag = False
        ##### Your Code Here ↓ #####
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.bgm.stop()
                pygame.quit()
                sys.exit()

            if event.type == GameEvent.EVENT_BATTLE:
                self.battle_happen()
            if event.type == GameEvent.EVENT_SWITCH:
                self.flush_scene(event.dict['map'])
            if event.type == GameEvent.EVENT_BACKPACK:
                self.unfold_backpack()
            if event.type == GameEvent.EVENT_BOSSBATTLE:
                self.battle_happen(True)

            if self.state == GameState.GAME_INDEX and event.type == pygame.MOUSEBUTTONDOWN:
                
                prev_x=pygame.mouse.get_pos()[0]
                prev_y=pygame.mouse.get_pos()[1]
                # 点击进入游戏
                if(prev_x >= IndexSettin.enter_X_min and prev_x <= IndexSettin.enter_x_max and prev_y >= IndexSettin.enter_y_min and prev_y <= IndexSettin.enter_y_max):
                    # print("prev_x :::  ",prev_x)
                    # event.dict['map'] = {'map':GameState.GAME_PLAY_VILL}
                    self.flush_scene(GameState.GAME_PLAY_VILL)
                # 点击退出游戏
                elif(prev_x >= IndexSettin.exit_X_min and prev_x <= IndexSettin.exit_x_max and prev_y >= IndexSettin.exit_y_min and prev_y <= IndexSettin.exit_y_max):
                    self.bgm.stop()
                    pygame.quit()
                    sys.exit()
                # # 其它情况停留当前页
        # self.scene.update_camera(self.player)
        self.update_collide()
        if self.scene.selfbox!=None:
            if  any(self.keys) and pygame.time.get_ticks() - self.scene.selfbox.last_time_pressed >= self.scene.selfbox.CD:
                    if any(self.keys):
                        self.scene.selfbox.last_time_pressed = pygame.time.get_ticks()
                    if self.scene.selfbox.state == True :
                        self.scene.selfbox.update(self.keys)
        # print("self.player.rect >> ",self.player.rect)
        # print("sprite :::: ",self.scene.obstacle)
        # print(displacement_settings.village_map_x,'  ',displacement_settings.village_map_y)
        # 地图上存在portals时检测碰撞 2024/01/17
        # if (self.scene.portals is not None):
            # print("portals ",pygame.sprite.spritecollide(self.player,self.scene.portals,False))
            # if pygame.sprite.spritecollide(self.player,self.scene.portals,False) and self.keys[pygame.K_e]:
        if(self.player.HP <= 0):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_OVER}))
        # Boss血量为零（在Boss场景），游戏胜利
        elif(self.state == GameState.GAME_PLAY_BOSS and  self.win == True ):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_VICTORY}))
        # 触发进入house
        if((self.player.rect[0] >= TransmitHouseSettings.X_min and self.player.rect[0] <= TransmitHouseSettings.x_max and
        self.player.rect[1] >= TransmitHouseSettings.y_min and self.player.rect[1] <= TransmitHouseSettings.y_max) and self.keys[pygame.K_e]):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_HOUSE}))
        # house触发返回乡村（village）地图
        if((self.player.rect[0] >= HouseTransmitVillageSettings.X_min and self.player.rect[0] <= HouseTransmitVillageSettings.x_max and
        self.player.rect[1] >= HouseTransmitVillageSettings.y_min and self.player.rect[1] <= HouseTransmitVillageSettings.y_max) and self.keys[pygame.K_e]):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_VILL}))
        if self.keys[pygame.K_q] or self.player.backpack.state == True:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_BACKPACK,{'map':GameState.GAME_PLAY_VILL}))
        # 地牢（dungeon）触发返回乡村（village）地图
        if((self.player.rect[0] >= DungeonToVillageSettings.X_min and self.player.rect[0] <= DungeonToVillageSettings.x_max and
        self.player.rect[1] >= DungeonToVillageSettings.y_min and self.player.rect[1] <= DungeonToVillageSettings.y_max)):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_VILL}))
        # 野外（wild）触发进入Boss地图
        if((self.player.rect[0] >= WildToBossSettins.X_min and self.player.rect[0] <= WildToBossSettins.x_max and
        self.player.rect[1] >= WildToBossSettins.y_min and self.player.rect[1] <= WildToBossSettins.y_max)):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_BOSS}))

        # # 存在障碍时检测 2024/01/17
        # if(self.scene.obstacle is not None):
        #     collide_list = pygame.sprite.spritecollide(self.player,self.scene.obstacle,False)
        #     # print("self.player.rect >>>>>>>> ",self.player.rect)
        #     # for item in self.scene.obstacle:
        #     #     print("item rect ::::::::: ",item.rect)
        #     # 有碰撞精灵
        #     if len(collide_list)>0 :
        #         print(len(collide_list))
                    # i = 0
        #         for item in self.scene.obstacle:
        #             # print("item ::: " ,item)
        #             if(i== 5):
        #                 dungeon_sprite = item
        #             if(i == 6):
        #                 Wild_sprite = item
        #             i += 1
                    
        #         # 判断是否触发地牢场景
        #         if dungeon_sprite in collide_list:
        #             pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_DUNGEON}))
        #         # 判断是否触发野外gif场景    
        #         if Wild_sprite in collide_list:
        #             pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_WILD}))
            
        # 判断是否触发地牢场景
        if (self.player.rect[0] >= TransmitDungeonSettings.X_min and self.player.rect[0] <= TransmitDungeonSettings.x_max and
            self.player.rect[1] >= TransmitDungeonSettings.y_min and self.player.rect[1] <= TransmitDungeonSettings.y_max):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_DUNGEON}))
        # 判断是否触发野外gif场景    
        if (self.player.rect[0] >= TransmitWildSettings.X_min and self.player.rect[0] <= TransmitWildSettings.x_max and
            self.player.rect[1] >= TransmitWildSettings.y_min and self.player.rect[1] <= TransmitWildSettings.y_max):
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_WILD}))
        self.update_collide()
        # 保证只有在未打开背包的时候才会更新玩家的行为,且未发生碰撞
        if self.player.backpack.state == False and self.keys.count(True)<2 and self.battle_box.state == False:
            self.player.update(self.keys, self.scene)
        if self.keys[pygame.K_q] or self.player.backpack.state == True:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_BACKPACK))
        if self.player.backpack.state == False and self .battle_box.state == False and self.keys.count(True)<2 and self.scene.selfbox == False:
            self.player.update(self.keys, self.scene)
        for each in self.scene.dialognpcs.sprites():
            each.update()  
        ##### Your Code Here ↑ #####

    def update_main_menu(self, events):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_vill(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        # for monster in self.scene.monsters:
        #     if pygame.sprite.collide_rect(self.player, monster):
        #         self.battle_box = BattleBox(self.window,self.player,monster)
        #         self.battle_box.state = True 
        pass
        ##### Your Code Here ↑ #####
        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        ##### Your Code Here ↑ #####
    def update_house(self,events):
        pass
    def update_wild(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
        
        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_boss(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
        
        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Collision-relate update funtions here ↓
    def update_collide(self):
        # Player -> Obstacles
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> NPCs; if multiple NPCs collided, only first is accepted and dealt with.
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> Monsters
        ##### Your Code Here ↓ #####
        if self.scene.monsters != None:
            for monster in self.scene.monsters:
                    if pygame.sprite.collide_rect(self.player,monster):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))
                        if self.battle_box.state == False:
                            self.battle_box = BattleBox(self.player,monster)
                            self.battle_box.state = True
        ##### Your Code Here ↑ #####
        
        # Player -> Portals
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
        
        # Player -> Boss
        ##### Your Code Here ↓ #####
        if self.state == GameState.GAME_PLAY_BOSS:
             pygame.event.post(pygame.event.Event(GameEvent.EVENT_BOSSBATTLE))
        ##### Your Code Here ↑ #####

    def update_NPCs(self):
        # This is not necessary. If you want to re-use your code you can realize this.
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    def update_backpack(self):
        pass

    # Render-relate update functions here ↓
    def render(self):
        ##### Your Code Here ↓ #####
        # self.keys = pygame.key.get_pressed()
        # self.window.fill((0, 0, 0))
        # self.scene.render_map()
        #  #  测试用，一会删
        # if self.scene.monsters != None:
        #     self.scene.monsters.draw(self.window)
        # for npc in self.scene.dialognpcs.sprites():
        #     npc.draw(self.window)
        # self.scene.trigger_dialog(self.player,self.keys)    
        # self.scene.end_dialog(self.player,self.keys)
        # self.scene.render_behind_obstacle()
        # self.player.draw(self.window)
        # self.scene.render_front_obstacle()
        # #分别渲染在主角前后方的障碍物以做出遮挡效果
        # if self.player.backpack.state==True:
        #     self.player.backpack.draw(self.window)
        # if self.battle_box.state == True:
        #     self.player.backpack.battle_draw(self.window)
        #     if  not self.battle_box.boss:
        #         self.battle_box.draw(self.window)
        #     else:
        #         self.render_boss()
        # if self.scene.selfbox!= None:
        #     if self.scene.selfbox.state and talkover[self.state.value] == False:
        #         self.scene.selfbox.draw(self.window)
        self.keys = pygame.key.get_pressed()
        self.window.fill((0, 0, 0))
        self.scene.render_map()
         #  测试用，一会删
        if self.scene.monsters != None:
            self.scene.monsters.draw(self.window)
        for npc in self.scene.dialognpcs.sprites():
            npc.draw(self.window)
        self.scene.trigger_dialog(self.player,self.keys)    
        self.scene.end_dialog(self.player,self.keys)
        self.scene.render_behind_obstacle()
        self.player.draw(self.window)
        self.scene.render_front_obstacle()
        #分别渲染在主角前后方的障碍物以做出遮挡效果
        if self.player.backpack.state==True:
            self.player.backpack.draw(self.window)
        if self.battle_box.state == True and self.state != GameState.GAME_OVER and self.state != GameState.GAME_VICTORY:
            self.player.backpack.battle_draw(self.window)
            if  not self.battle_box.boss:
                self.battle_box.draw(self.window)
            elif(self.state == GameState.GAME_PLAY_BOSS):
                self.render_boss()
        if self.scene.selfbox!= None:
            if self.scene.selfbox.state and talkover[self.state.value] == False:
                self.scene.selfbox.draw(self.window)
        ##### Your Code Here ↑ #####
    
    def render_main_menu(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
    def render_city(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def render_wild(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def render_boss(self):
        ##### Your Code Here ↓ #####
        self.battle_box.print_detail(self.window)
        self.battle_box.print_HP(self.player,110,655,self.window)
        self.battle_box.print_HP(self.battle_box.monster,600,10,self.window)
        ##### Your Code Here ↑ #####
    def unfold_backpack(self):
        if  any(self.keys) and pygame.time.get_ticks() - self.player.backpack.last_time_pressed >= self.player.backpack.CD:
            if self.keys[pygame.K_q]:
                self.player.backpack.state = not self.player.backpack.state
                self.player.backpack.last_time_pressed = pygame.time.get_ticks()
            if self.player.backpack.state == True :
                self.player.backpack.update(self.keys)
    def battle_happen(self,is_boss = False):
        if not is_boss:
            self.battle_box.update()
            if  any(self.keys) and pygame.time.get_ticks() - self.player.backpack.last_time_pressed >= self.player.backpack.CD:
                if any(self.keys):
                    self.player.backpack.last_time_pressed = pygame.time.get_ticks()
                if self.battle_box.monster.HP <= 0:
                    self.player.EX+=1
                    if self.player.EX==2:
                        self.player.backpack.remove_item(Items.wooden_sword)
                        self.player.backpack.add_item(Items.iron_sword,(type.weapon,4))
                    if self.player.EX==3:
                        self.player.backpack.remove_item(Items.iron_sword)
                        self.player.backpack.add_item(Items.goledn_sword,(type.weapon,6))
                        self.player.backpack.add_achieve('*上科大学习生活必备好物：获得泡面')
                    self.battle_box.monster.kill()
                    self.player.HP = 20
                    if self.battle_box.monster.is_mimic:
                        self.player.backpack.add_item(Items.lamp)
                        self.player.has_lamp = True
                        self.player.backpack.add_achieve('*神说要有光！：获得油灯')
                if self.battle_box.state == True :
                    self.player.backpack.battle_update(self.keys,self.battle_box)
        else:
            if self.state == GameState.GAME_PLAY_BOSS:
                if self.battle_box.state == False:
                                boss = Monster(pygame.image.load(GamePath.monsters[0]),0,0,30,5)
                                self.battle_box = BattleBox(self.player,boss)
                                self.battle_box.state = True
                                self.battle_box.boss = True
                if self.scene.selfbox.state == False:    
                    self.battle_box.update()
                    if  any(self.keys) and pygame.time.get_ticks() - self.player.backpack.last_time_pressed >= self.player.backpack.CD:
                        if any(self.keys):
                            self.player.backpack.last_time_pressed = pygame.time.get_ticks()
                        if self.battle_box.state == True :
                            self.player.backpack.battle_update(self.keys,self.battle_box)
                    if self.battle_box.monster.HP<=0:
                        self.win = True

    