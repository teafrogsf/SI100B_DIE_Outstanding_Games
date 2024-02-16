# -*- coding:utf-8 -*-

import pygame
from Setting import *
from Map import *
from Box import *
from Event import GameEvent
from Player import Player
from Enemy import Enemy

class Scene():
    def __init__(self, window, player):
        # 场景本身的属性，例如场景的大小，场景的背景贴图/地图
        self.window = window

        # camera系统
        self.visibleGroup = self.CameraGroup()

        # 场景中碰撞元素
        self.collideGroup = self.CollisionGroup()
        # 场景中传送门
        self.portableGroup = pygame.sprite.Group()

        # 场景中的玩家
        self.player = player
        self.player.rect.center = (0,0)

        # 场景中的NPC
        self.npcGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()

        # 场景调用的Box
        self.box = None

        # BGM
        self.BGM = getattr(GamePath, 'bgm' + (self.__class__.__name__).removesuffix('_Scene'))

    def update(self, player, keyDown, keys):
        player.move(keys)
        player.update(keys)
        player.move_cancel(keys, self.collideGroup.collide_check(self.portableGroup, self.npcGroup, self.enemyGroup, self.visibleGroup, player))
        if self.box != None:
            if self.box.isFinished:
                if isinstance(self.box, BattleBox):
                    self.enemyGroup.remove(self.box.enemy)
                    self.collideGroup.remove(self.box.enemy)
                    self.visibleGroup.remove(self.box.enemy)
                self.box = None
                self.player.talking = False
            else:
                self.box.update(keyDown)
    def render(self, player):
        self.visibleGroup.custom_draw(player)
        if self.box != None:
            self.box.render()

    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.displaySurface = pygame.display.get_surface()
            # camera offset
            self.offsetX = 0
            self.offsetY = 0

        def custom_draw(self, player):
            self.offsetX = player.rect.centerx - WindowSettings.width // 2
            self.offsetY = player.rect.centery - WindowSettings.height // 2
            
            for sprite in self.sprites():
                self.displaySurface.blit(sprite.image, sprite.rect.center - pygame.math.Vector2(self.offsetX, self.offsetY))
        
    class CollisionGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.collisionRange = WindowSettings.width // 4
        def collide_check(self, portableGroup, npcGroup, EnemyGroup, visibleGroup, player):
            # 碰撞检测
            collidedSprites = [sprite for sprite in self if abs(sprite.rect.centerx - player.rect.centerx) < self.collisionRange 
                                and abs(sprite.rect.centery - player.rect.centery) < self.collisionRange 
                                and pygame.sprite.collide_mask(player, sprite)] # 熔断优化性能
            collidedSpritesRect = [sprite for sprite in self if abs(sprite.rect.centerx - player.rect.centerx) < self.collisionRange 
                                and isinstance(sprite, NPC)
                                and abs(sprite.rect.centery - player.rect.centery) < self.collisionRange 
                                and pygame.sprite.collide_rect(player, sprite)] # 熔断优化性能
            collidedSprites.extend(collidedSpritesRect)
            # 可以进一步处理对特定障碍物的响应
            for sprite in collidedSprites:
                if sprite in portableGroup:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH, target=sprite.portalTarget))
                if sprite in npcGroup:
                    if hasattr(sprite, 'shopType'):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP, shopType=sprite.shopType))
                    if hasattr(sprite, 'dialogType'):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG, dialogType=sprite.dialogType, dialogNPC = sprite))
                    if hasattr(sprite, 'HPChange'):
                        self.remove(sprite)
                        npcGroup.remove(sprite)
                        visibleGroup.remove(sprite)
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':player, 'HP':int(player.HP * sprite.HPChange)}))
                        pygame.display.get_surface().fill((255, 255, 255))
                        pygame.display.update()
                        pygame.display.get_surface().fill((255, 255, 255))
                        pygame.display.update()
                        pygame.display.get_surface().fill((255, 255, 255))
                        pygame.display.update()
                if sprite in EnemyGroup:
                    if isinstance(sprite, Enemy):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE, enemy = sprite))
                        
            if collidedSprites != []:
                return True
            else:
                pass
                   

class Home_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (700, 1300)
        # ground
        for tile in load_ground(GamePath.sceneHomeMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneHomeMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        # npc
        for npc_layer in ['Shop_NPC','Guide_NPC']:
            for npc in load_npc(GamePath.sceneHomeMap,npc_layer):
                self.npcGroup.add(npc)
                self.visibleGroup.add(npc)
                self.collideGroup.add(npc)
        
        # portable
        for portalTarget in ['Universe']:
            for portal in load_portal(GamePath.sceneHomeMap,'portal_Universe',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)
        
        self.visibleGroup.add(player)
    
class School_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (1300, 900)
        # ground
        for tile in load_ground(GamePath.sceneSchoolMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneSchoolMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        
        # portable
        for portalTarget in ['SIST','SLST','SPST','Underground','KFC']:
            for portal in load_portal(GamePath.sceneSchoolMap,f'portal_{portalTarget}',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)
        
        self.visibleGroup.add(player)

class SLST_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (100, 400)
        # ground
        for tile in load_ground(GamePath.sceneSLSTMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneSLSTMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        # enemy
        for enemy_layer in ['Enemy_SLST','Enemy_Student']:
            for enemy in load_npc(GamePath.sceneSLSTMap,enemy_layer):
                self.enemyGroup.add(enemy)
                self.visibleGroup.add(enemy)
                self.collideGroup.add(enemy)
        
        # portable
        for portalTarget in ['School']:
            for portal in load_portal(GamePath.sceneSLSTMap,'portal_School',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)
        
        self.visibleGroup.add(player)

class SPST_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (1440, 640)
        # ground
        for tile in load_ground(GamePath.sceneSPSTMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneSPSTMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        # enemy
        for enemy_layer in ['Enemy_SPST', 'Enemy_Student']:
            for enemy in load_npc(GamePath.sceneSPSTMap,enemy_layer):
                self.enemyGroup.add(enemy)
                self.visibleGroup.add(enemy)
                self.collideGroup.add(enemy)
        
        # portable
        for portalTarget in ['School']:
            for portal in load_portal(GamePath.sceneSPSTMap,'portal_School',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)

        self.visibleGroup.add(player)

class SIST_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (116, 612)
        # ground
        for tile in load_ground(GamePath.sceneSISTMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneSISTMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        # enemy
        for enemy_layer in ['Enemy_SIST']:
            for enemy in load_npc(GamePath.sceneSISTMap,enemy_layer):
                self.enemyGroup.add(enemy)
                self.visibleGroup.add(enemy)
                self.collideGroup.add(enemy)
        
        # portable
        for portalTarget in ['School']:
            for portal in load_portal(GamePath.sceneSISTMap,'portal_School',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)
        self.visibleGroup.add(player)

class Underground_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (150, 450)
        # ground
        for tile in load_ground(GamePath.sceneUndergroundMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneUndergroundMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        # enemy
        for enemy_layer in ['Boss']:
            for enemy in load_npc(GamePath.sceneUndergroundMap,enemy_layer):
                self.enemyGroup.add(enemy)
                self.visibleGroup.add(enemy)
                self.collideGroup.add(enemy)
        
        # treasure_npc
        for treasure_layer in ['Treasure_NPC']:
            for treasure in load_npc(GamePath.sceneUndergroundMap,treasure_layer):
                self.npcGroup.add(treasure)
                self.visibleGroup.add(treasure)
                self.collideGroup.add(treasure)
        
        # portable
        for portalTarget in ['School']:
            for portal in load_portal(GamePath.sceneUndergroundMap,'portal_School',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)

        self.visibleGroup.add(player)

class KFC_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (100, 350)
        # ground
        for tile in load_ground(GamePath.sceneKFCMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneKFCMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        # npc
        for npc_layer in ['KFC_NPC']:
            for npc in load_npc(GamePath.sceneKFCMap,npc_layer):
                self.npcGroup.add(npc)
                self.visibleGroup.add(npc)
                self.collideGroup.add(npc)
        
        # portable
        for portalTarget in ['School']:
            for portal in load_portal(GamePath.sceneKFCMap,'portal_School',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)

        self.visibleGroup.add(player)

class Universe_Scene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.playerPos = (80, 500)
        # ground
        for tile in load_ground(GamePath.sceneUniverseMap):
            self.visibleGroup.add(tile)
        
        # obstacles
        for tile in load_obstacles(GamePath.sceneUniverseMap):
            self.collideGroup.add(tile)
            self.visibleGroup.add(tile)
        
        
        # portable
        for portalTarget in ['School']:
            for portal in load_portal(GamePath.sceneUniverseMap,'portal_School',portalTarget):
                self.portableGroup.add(portal)
                self.visibleGroup.add(portal)
                self.collideGroup.add(portal)

        self.visibleGroup.add(player)

    class CollisionGroup(Scene.CollisionGroup):  #Override Inner Class
        def collide_check(self, portableGroup, npcGroup, EnemyGroup, visibleGroup, player):
            # 碰撞检测

            collidedSprites = [sprite for sprite in self if abs(sprite.rect.centerx - player.rect.centerx) < self.collisionRange 
                                and abs(sprite.rect.centery - player.rect.centery) < self.collisionRange 
                                and pygame.sprite.collide_mask(player, sprite)] # 熔断优化性能

            # 可以进一步处理对特定障碍物的响应
            for sprite in collidedSprites:
            # 确定碰撞的边界
                if sprite in portableGroup:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH, target=sprite.portalTarget))
                else:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIED))

    class CameraGroup(Scene.CameraGroup):
        def __init__(self):
            super().__init__()
            self.spaceShipImg = pygame.image.load(GamePath.spaceShipImg)
            self.spaceShipImg = pygame.transform.scale(self.spaceShipImg, (PlayerSettings.width, PlayerSettings.width))

        def custom_draw(self, player):
            self.offsetX = player.rect.centerx - WindowSettings.width // 2
            self.offsetY = player.rect.centery - WindowSettings.height // 2
            
            for sprite in self.sprites():
                if isinstance(sprite, Player):
                    self.displaySurface.blit(self.spaceShipImg, sprite.rect.center - pygame.math.Vector2(self.offsetX, self.offsetY))
                else:
                    self.displaySurface.blit(sprite.image, sprite.rect.center - pygame.math.Vector2(self.offsetX, self.offsetY))
