# -*- coding:utf-8 -*-

import pygame
from Settings import *
from Attributes import *
from Scene import *
import GameManager

class Player(pygame.sprite.Sprite, Collidable):
    
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        ##### Your Code Here ↓ #####
        # 存角色状态图的字典
        self.images = {'Front': None,'Back': None,'Left' :None ,'Right': None}
        for direction in directions:
            self.images[direction]=[pygame.transform.scale(pygame.image.load(img).convert_alpha(), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for img in GamePath.player[direction]]
        self.index = 0 #玩家行动动画用
        self.state = PlayerState.front #玩家朝向
        self.image = self.images[self.state.name][self.index] #导入图片
        self.rect = self.image.get_rect(topleft=(x, y)) #获取rect
        self.speed = PlayerSettings.playerSpeed #玩家速度
        self.talking = False #交谈
        self.talktovill=1
        self.talkingindex=0
        self.backpack = BackpackBox()
        self.HP = PlayerSettings.playerHP
        self.init_HP = PlayerSettings.init_playerHP
        self.EX = 0
        self.has_lamp = False
        ##### Your Code Here ↑ #####
    def fix_to_middle(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy
    def attr_update(self, addCoins = 0, addHP = 0, addAttack = 0, addDefence = 0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def try_move(self, width, height):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def move(self, dx, dy):
        self.rect = self.rect.move(dx,dy)
  
    
    # 人物、背景地图移动 2024/01/15
    def movePlayer(self,keys,scene: Scene):
        # 更新位置
        dx = 0
        dy = 0
        # 移动任何物体都先将位移量清零，该处为最佳置初始值位置
        displacement_settings.offset_x = 0
        displacement_settings.offset_y = 0
        movePlayerFlag = False
        # 人物未到边界
        if keys[pygame.K_w] and self.rect.top > 0 :
            # 地图移动到边或者人未在中心区域
            if(displacement_settings.village_map_y - self.speed <= 0 or 
            #    (map_info_setting.map_info != 1 or abs(self.rect.centery) > displacement_settings.central_zone_y_max or abs(self.rect.centery)<displacement_settings.central_zone_y_min)):
               (map_info_setting.map_info != 1 or abs(self.rect.centery) > displacement_settings.central_zone_y_min )):
                dy -= self.speed
                movePlayerFlag = True
            else:
                displacement_settings.village_map_y -= self.speed
                displacement_settings.offset_y -= self.speed
            self.state=PlayerState.back
        # 人物未到边界
        if keys[pygame.K_s] and self.rect.bottom < WindowSettings.height :
            # 地图移动到边或者人未在中心区域
            if(displacement_settings.village_map_y +self.speed >= displacement_settings.offset_y_max or
            #  (map_info_setting.map_info != 1 or abs(self.rect.centery) > displacement_settings.central_zone_y_max or abs(self.rect.centery)<displacement_settings.central_zone_y_min)):
               (map_info_setting.map_info != 1 or abs(self.rect.centery) < displacement_settings.central_zone_y_max )):
                dy += self.speed
                movePlayerFlag = True
            else:
                displacement_settings.village_map_y += self.speed
                displacement_settings.offset_y += self.speed
            self.state=PlayerState.front
        # 人物未到边界
        if keys[pygame.K_a] and self.rect.left > 0 :
            # 地图移动到边或者人未在中心区域
            if(displacement_settings.village_map_x - self.speed <= 0 or
            #    (map_info_setting.map_info != 1 or abs(self.rect.centerx) > displacement_settings.central_zone_x_max or abs(self.rect.centerx)<displacement_settings.central_zone_x_min)):
               (map_info_setting.map_info != 1 or abs(self.rect.centerx) > displacement_settings.central_zone_x_min )):
                dx -= self.speed
                movePlayerFlag = True
            else:
                displacement_settings.village_map_x -= self.speed
                displacement_settings.offset_x -= self.speed
            self.state=PlayerState.left
        # 人物未到边界
        if keys[pygame.K_d] and self.rect.right < WindowSettings.width :
            # 地图移动到边或者人未在中心区域
            if(displacement_settings.village_map_x + self.speed >= displacement_settings.offset_x_max or 
            #    (map_info_setting.map_info != 1 or abs(self.rect.centerx) > displacement_settings.central_zone_x_max or abs(self.rect.centerx)<displacement_settings.central_zone_x_min)):
               (map_info_setting.map_info != 1 or abs(self.rect.centerx) < displacement_settings.central_zone_x_max )):
                dx += self.speed
                movePlayerFlag = True
            else:
                displacement_settings.village_map_x += self.speed
                displacement_settings.offset_x += self.speed
            self.state=PlayerState.right

        # 是否需要处理人物移动
        if(movePlayerFlag == True) :
            # print("displacement_settings.offset_x ::: ",displacement_settings.offset_x)
            # print("displacement_settings.offset_y ::: ",displacement_settings.offset_y)
            movePlayerFlag = False
            self.move(dx,dy)
            if scene.obstacle is not None and pygame.sprite.spritecollide(self, scene.obstacle, False):
                # 遇到障碍物，取消移动
                self.move(-dx,-dy)
        # 移动地图时碰撞检测，是否取消移动
        if(self.checkObstacleCollide(scene)):
            # 左，取消坐标值改变
            if self.state == PlayerState.left:
                displacement_settings.village_map_x += self.speed
                displacement_settings.offset_x += self.speed
            # 上，取消坐标值改变
            elif self.state == PlayerState.back:
                displacement_settings.village_map_y += self.speed
                displacement_settings.offset_y += self.speed
            # 右，取消坐标值改变
            elif self.state == PlayerState.right:
                displacement_settings.village_map_x -= self.speed
                displacement_settings.offset_x -= self.speed
            # 下，取消坐标值改变
            elif self.state == PlayerState.front:
                displacement_settings.village_map_y -= self.speed
                displacement_settings.offset_y -= self.speed
        # 更新角色动画
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.state.name][self.index]
        if scene.obstacle is not None:
            for i in scene.obstacle:
                # if i.rect.top >= self.rect.bottom :
                #     i.pos = ObstaclesPos.front
                # if i.rect.bottom <= self.rect.top :
                #     i.pos = ObstaclesPos.behind
                # 神奇的是不知道为什么他识别i.rect为tuple（待优化
                # 气死我了明明在player里面声明的就是rect
                if i.rect[1] >= self.rect.bottom :
                    i.pos = ObstaclesPos.front
                elif i.rect[1]-i.rect[3] <= self.rect.top :
                    i.pos = ObstaclesPos.behind
                    #遮挡待优化
    
    # 移动village_map上的全部障碍物 2024/01/16
    def moveObstacle(self,scene: Scene):
        # 碰撞检测在player 的moveBgMap 中做了检测
        for obstacle_sprite in scene.obstacle:
            obstacle_sprite.img_rect.x -= displacement_settings.offset_x
            obstacle_sprite.img_rect.y -= displacement_settings.offset_y

    # 移动门 2024/01/16
    def movePortals(self,scene: Scene):
        for portals_sprite in scene.portals:
            portals_sprite.rect.x -= displacement_settings.offset_x
            portals_sprite.rect.y -= displacement_settings.offset_y
    # lst add end 2024/01/15
    
    def update(self, keys, scene: Scene):
        ##### Your Code Here ↓ #####
        if self.talking:
            # 如果不移动，显示静态图像
            self.index = 0
            self.image = self.images[self.state.name][self.index]
        else:
            self.image = self.images[self.state.name][self.index]
            self.movePlayer(keys,scene)
            # 人物不能移动情况，判断背景图移动，并且在village_map地图中
            # if(movePlayerFlag == False and map_info_setting.map_info == 1):
            #     self.moveBgMap(movePlayerFlag,keys, scene)
            # else:
            #     movePlayerFlag = self.movePlayer(keys, scene)
        if self.talktovill>len(DialogSettings.npctextcontent['village_chief'][1]):
            self.talktovill=1      
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        window.blit(self.image, self.rect)
        ##### Your Code Here ↑ #####

    # village map 上物体碰撞检测 2024/01/17
    def checkObstacleCollide(self,scene:Scene):
        
        retValue = False
         # 检测是否发生碰撞
        if(scene.obstacle is not None):
            i = 0 
            # 先移动碰撞位置
            for obstacle_sprite in scene.obstacle:
                lstRect = list(obstacle_sprite.rect)            # 将元组转换为列表
                lstRect[0] -= displacement_settings.offset_x    # 修改列表中的x坐标
                lstRect[1] -= displacement_settings.offset_y    # 修改列表中的y坐标
                obstacle_sprite.rect = tuple(lstRect)           # 将列表转换为元组
                # print(displacement_settings.offset_x,"  ",displacement_settings.offset_y)
                # print("obstacle_sprite.rect ::: ",i,obstacle_sprite.rect)
                i += 1
             # 存在障碍时检测 2024/01/17
        
            collide_list = pygame.sprite.spritecollide(self,scene.obstacle,False)
            # print("self.player.rect >>>>>>>> ",self.player.rect)
            # for item in self.scene.obstacle:
            #     print("item rect ::::::::: ",item.rect)
            # 有碰撞精灵
            if len(collide_list)>0 :
                i = 0
                for item in scene.obstacle:
                    # print("item ::: " ,item)
                    if(i== 5):
                        dungeon_sprite = item
                        
                        # 判断是否触发地牢场景
                        if dungeon_sprite in collide_list:
                            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_DUNGEON}))
                    if(i == 6):
                        Wild_sprite = item
                       
                        # 判断是否触发野外gif场景    
                        if Wild_sprite in collide_list:
                            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH,{'map':GameState.GAME_PLAY_WILD}))
                    i += 1
            # 碰撞检测
            if len(collide_list)>0:
                retValue = True
                for obstacle_sprite in scene.obstacle:
                    lstRect = list(obstacle_sprite.rect)            # 将元组转换为列表
                    lstRect[0] += displacement_settings.offset_x    # 修改列表中的x坐标
                    lstRect[1] += displacement_settings.offset_y    # 修改列表中的y坐标
                    obstacle_sprite.rect = tuple(lstRect)           # 将列表转换为元组
            else:
                self.moveObstacle(scene)
                self.movePortals(scene)
                retValue = False
            displacement_settings.offset_x = 0
            displacement_settings.offset_y = 0
        return retValue