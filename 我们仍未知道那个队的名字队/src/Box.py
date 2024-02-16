import time
from Weapon import Weapon
import pygame
from Setting import baseWidth, baseHeight, fps, ShopGoodsList, Dialog, GoldReward, GamePath
from Event import GameEvent
import random
from Animation import Animation
from Enemy import Enemy_SIST, Enemy_SLST, Enemy_SPST, Enemy_Student, Boss

class Box:
    def __init__(self, window, fontSize: int = 32, fontColor: tuple = (255, 255, 255)):
        self.window = window
        self.boxCenterX = baseWidth * 5
        self.boxCenterY = baseHeight * 5

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(GamePath.font, self.fontSize)
        self.smallFontSize = 17  # 设定一个较小的字体大小
        self.smallFont = pygame.font.Font(GamePath.font, self.smallFontSize)  # 创建一个新的字体对象

        self.textOffsetY = baseHeight

        self.bg = None

        self.isFinished = False

    def update(self, keyDown):
        if keyDown == pygame.K_UP and self.cursorIndex > 0:
            self.move_cursor(-1)
        if keyDown == pygame.K_DOWN and self.cursorIndex < len(self.itemList) - 1:
            self.move_cursor(1)
        if keyDown == pygame.K_RETURN:
            self.choose()
        if keyDown == pygame.K_x:
            self.close()

    def move_cursor(self,value):
        self.cursorIndex += value

    def close(self):
        self.isFinished = True

class Dialog_GuideBox(Box):
    def __init__(self, window, NPC, fontSize: int = 25, fontColor: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(window, fontSize, fontColor)
        self.bg = pygame.Surface((baseWidth*8, baseHeight*6), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 200))
        self.bgRect = self.bg.get_rect()
        self.bgRect.center = (self.boxCenterX, self.boxCenterY) #获得并确定rect中心
        self.dialogList = Dialog.guide
        self.textOffsetY = baseHeight // 2
        NPCimageOriginalSize = NPC.image.get_size()
        NPCimageNewSize = (baseWidth *2, baseWidth * 2 * NPCimageOriginalSize[1] // NPCimageOriginalSize[0])
        self.NPCTalkingImage = pygame.transform.scale(NPC.image, NPCimageNewSize)
        self.NPCTalkingImageRect = self.NPCTalkingImage.get_rect(topleft = (self.bgRect.topleft[0], self.bgRect.topleft[1] + baseHeight))

    def render(self):
        self.window.blit(self.bg, self.bgRect)
        # 渲染选项
        for i, dialog in enumerate(self.dialogList):
            text = self.font.render(dialog, True, self.fontColor)
            textRect = text.get_rect(topleft=(self.bgRect.topleft[0] + baseWidth * 2, self.bgRect.topleft[1] + baseHeight + self.textOffsetY * i))
            self.window.blit(text, textRect)
        self.window.blit(self.NPCTalkingImage, self.NPCTalkingImageRect)

    def update(self, keyDown):
        if keyDown == pygame.K_x:
            self.close()

class Shop_HomeBox(Box):
    def __init__(self, window, player, fontSize: int = 32, fontColor: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(window, fontSize, fontColor)
        self.bg = pygame.Surface((baseWidth*8, baseHeight*8), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 200))
        self.bgRect = self.bg.get_rect()
        self.bgRect.center = (self.boxCenterX, self.boxCenterY) #获得并确定rect中心
        self.player = player # 确定玩家参数
        self.itemList = ShopGoodsList.homeShopList
        self.cursorIndex = 0 # 光标位置
        self.cursorCD = 10 # 光标闪烁计时器
        self.purchaseMessage = ''
        self.purchaseMessageCD = 60
        self.purchaseMessageColor = (255, 0, 0)
    
    def render(self):
        self.window.blit(self.bg, self.bgRect)

        # 渲染选项
        for i, item in enumerate(self.itemList):
            text = self.font.render(item[0], True, self.fontColor)
            textRect = text.get_rect(topleft=(self.bgRect.topleft[0] + baseWidth * 2, self.bgRect.topleft[1] + baseHeight * 1 + self.textOffsetY * i))
            self.window.blit(text, textRect)

            if i == self.cursorIndex and self.cursorCD >= fps // 3:
                pygame.draw.rect(self.window, (255, 255, 255), textRect)
                if self.cursorCD >= fps // 3 * 2:
                    self.cursorCD = 0

            text = self.font.render(str(item[1]), True, self.fontColor)
            textRect = text.get_rect(topleft=(self.bgRect.topleft[0] + baseWidth * 6, self.bgRect.topleft[1] + baseHeight * 1 + self.textOffsetY * i))
            self.window.blit(text, textRect)

        # 渲染提示信息
        text = self.font.render("Money: " + str(self.player.money)+"         "+"HP: "+str(self.player.HP), True, self.fontColor)
        textRect = text.get_rect(center=(self.boxCenterX, self.bgRect.bottomright[1] - self.textOffsetY * 3))
        self.window.blit(text, textRect)
        
        text = self.font.render("Press Enter to buy         Press X to exit", True, self.fontColor)
        textRect = text.get_rect(center=(self.boxCenterX, self.bgRect.bottomright[1] - self.textOffsetY * 1))
        self.window.blit(text, textRect)

        text = self.font.render("Press Up/Down to move cursor", True, self.fontColor)
        textRect = text.get_rect(center=(self.boxCenterX, self.bgRect.bottomright[1] - self.textOffsetY * 2))
        self.window.blit(text, textRect)

        self.cursorCD += 1

        if self.purchaseMessage:
            purchaseMessageSurface = self.smallFont.render(self.purchaseMessage, True, self.purchaseMessageColor)
            purchaseMessageX = self.bgRect.centerx - purchaseMessageSurface.get_width() / 2
            purchaseMessageY = self.bgRect.centery
            self.window.blit(purchaseMessageSurface, (purchaseMessageX, purchaseMessageY))
    
    def choose(self):
        if self.cursorIndex == 0:
            if self.player.money >= self.itemList[self.cursorIndex][1]:
                newWeapon = Weapon.get_weapon()
                self.purchaseMessage = f"恭喜您获得了 {newWeapon.name}, {newWeapon.description}, ATK+ {newWeapon.ATK}, DEF+{newWeapon.DEF} !"
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.player,'weapon':newWeapon,'money':-self.itemList[self.cursorIndex][1]}))
        if self.cursorIndex == 1:
            if self.player.money >= self.itemList[self.cursorIndex][1]:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.player,'HP':-1000,'money':-self.itemList[self.cursorIndex][1]}))
        

class Shop_KFCBox(Box):
    def __init__(self, window, player, fontSize: int = 32, fontColor: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(window, fontSize, fontColor)
        self.bg = pygame.Surface((baseWidth*8, baseHeight*8), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 200))
        self.bgRect = self.bg.get_rect()
        self.bgRect.center = (self.boxCenterX, self.boxCenterY) #获得并确定rect中心
        self.player = player # 确定玩家参数
        self.itemList = ShopGoodsList.KFCShopList
        self.cursorIndex = 0 # 光标位置
        self.cursorCD = 10 # 光标闪烁计时器
    
    def render(self):
        self.window.blit(self.bg, self.bgRect)

        # 渲染选项
        for i, item in enumerate(self.itemList):
            text = self.font.render(item[0], True, self.fontColor)
            textRect = text.get_rect(topleft=(self.bgRect.topleft[0] + baseWidth * 2, self.bgRect.topleft[1] + baseHeight * 1 + self.textOffsetY * i))
            self.window.blit(text, textRect)

            if i == self.cursorIndex and self.cursorCD >= fps // 3:
                pygame.draw.rect(self.window, (255, 255, 255), textRect)
                if self.cursorCD >= fps // 3 * 2:
                    self.cursorCD = 0

            text = self.font.render(str(item[1]), True, self.fontColor)
            textRect = text.get_rect(topleft=(self.bgRect.topleft[0] + baseWidth * 6, self.bgRect.topleft[1] + baseHeight * 1 + self.textOffsetY * i))
            self.window.blit(text, textRect)

        # 渲染提示信息
        text = self.font.render("Money: " + str(self.player.money)+"         "+"HP: "+str(self.player.HP), True, self.fontColor)
        textRect = text.get_rect(center=(self.boxCenterX, self.bgRect.bottomright[1] - self.textOffsetY * 3))
        self.window.blit(text, textRect)
        
        text = self.font.render("Press Enter to buy         Press X to exit", True, self.fontColor)
        textRect = text.get_rect(center=(self.boxCenterX, self.bgRect.bottomright[1] - self.textOffsetY * 1))
        self.window.blit(text, textRect)

        text = self.font.render("Press Up/Down to move cursor", True, self.fontColor)
        textRect = text.get_rect(center=(self.boxCenterX, self.bgRect.bottomright[1] - self.textOffsetY * 2))
        self.window.blit(text, textRect)

        self.cursorCD += 1
    
    def choose(self):
        if self.player.money >= self.itemList[self.cursorIndex][1]:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.player,'HP':self.itemList[self.cursorIndex][2],'money':-self.itemList[self.cursorIndex][1]}))

class BattleBox(Box):
    def __init__(self, window, player, enemy, fontSize: int = 32, fontColor: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(window, fontSize, fontColor)
        self.bg = pygame.Surface((baseWidth*8, baseHeight*8), pygame.SRCALPHA)
        self.bg.fill((0, 0, 0, 200))
        self.bgRect = self.bg.get_rect()
        self.bgRect.center = (self.boxCenterX, self.boxCenterY) #获得并确定rect中心
        self.textOffsetY = baseHeight

        self.player = player
        self.originalATK = player.ATK
        self.originalDEF = player.DEF
        PlayerimageOriginalSize = player.image.get_size()
        PlayerimageNewSize = (baseWidth *2, baseWidth * 2 * PlayerimageOriginalSize[1] // PlayerimageOriginalSize[0])
        self.PlayerBattleImage = pygame.transform.scale(player.images[8], PlayerimageNewSize)
        self.PlayerBattleImageRect = self.PlayerBattleImage.get_rect(center = (self.bgRect.topleft[0] + baseWidth * 3.5, self.bgRect.centery))

        self.inventory = player.inventory
        self.hasWeapon = False
        for item in self.inventory:
            if isinstance(item, Weapon):
                self.hasWeapon = True
                self.originalATK += item.ATK
                self.originalDEF += item.DEF
        if self.hasWeapon == False:
            self.inventory.append(Weapon.Weapon("空手", GamePath.weaponHand, ATK = 0, DEF = 0))
        
        self.currentATK = self.originalATK
        self.currentDEF = self.originalDEF

        self.enemy = enemy
        EnemyimageOriginalSize = enemy.image.get_size()
        EnemyimageNewSize = (baseWidth *2, baseWidth * 2 * EnemyimageOriginalSize[1] // EnemyimageOriginalSize[0])
        self.EnemyBattleImage = pygame.transform.scale(enemy.image, EnemyimageNewSize)
        self.EnemyBattleImageRect = self.EnemyBattleImage.get_rect(center = (self.bgRect.topleft[0] + baseWidth * 6.5, self.bgRect.centery))
        self.deadEnemyImage = pygame.transform.scale(enemy.deadImage, EnemyimageNewSize)
        self.deadEnemyImageRect = self.deadEnemyImage.get_rect(center = (self.bgRect.topleft[0] + baseWidth * 6.5, self.bgRect.centery))

        self.cursorIndex = 0 # 光标位置
        self.cursorCD = 10 # 光标闪烁计时器

        self.lastSkillChoice = None
        self.currentSkillChoice = None

        # 战斗选项区域
        self.actionbg = pygame.Surface((baseWidth*2, baseHeight*8), pygame.SRCALPHA)
        self.actionbg.fill((0, 0, 0, 200))
        self.actionbgRect = self.actionbg.get_rect()
        self.actionbgRect.topleft = self.bgRect.topleft #获得并确定rect中心

        self.battleMessage = ''
        self.battleMessageCD = 60
        self.battleMessageColor = (255, 0, 0)

        self.defeatMessage = ''
        self.defeatMessageCD = 120
        self.defeatMessageColor = (0, 255, 0)



        self.animation = None
        self.animationEnemy = None
        self.effectPosition = {
            'Sword': {
                'start': (self.PlayerBattleImageRect.centerx, self.PlayerBattleImageRect.centery),
                'target': (self.EnemyBattleImageRect.centerx, self.EnemyBattleImageRect.centery),
                },
            'Gun' : {'current': (self.EnemyBattleImageRect.centerx, self.EnemyBattleImageRect.centery - self.bgRect.height // 5)},
            'Axe' : {'current': (self.EnemyBattleImageRect.centerx, self.EnemyBattleImageRect.centery - self.bgRect.height // 5)},
            'Hand' : {'current': (self.EnemyBattleImageRect.centerx, self.EnemyBattleImageRect.centery)},
            'Shield' : {'current': (self.PlayerBattleImageRect.centerx, self.PlayerBattleImageRect.centery)},
            'Charge' : {'current': (self.PlayerBattleImageRect.centerx, self.PlayerBattleImageRect.centery)},
            'Poison' : {'current': (self.EnemyBattleImageRect.centerx, self.EnemyBattleImageRect.centery + baseWidth)},
            'Enemy' : {'current': (self.PlayerBattleImageRect.centerx, self.PlayerBattleImageRect.centery)},
            'Sword2' : {'start': (self.PlayerBattleImageRect.centerx, self.PlayerBattleImageRect.centery)}
            }
    

    def render(self):
        self.window.blit(self.bg, self.bgRect)
        self.window.blit(self.actionbg, self.actionbgRect)
            # 渲染信息
        playerInfo = ['','','']
        playerInfo[0] = 'HP: '+ str(self.player.HP)
        playerInfo[1] = 'ATK: '+ str(self.currentATK)
        playerInfo[2] = 'DEF: '+ str(self.currentDEF)
        enemyInfo = self.enemy.get_Info()
        k = 0
        j = 0
        for info in playerInfo:
            text = self.font.render(info, True, self.fontColor)
            textRect = text.get_rect(topleft = (self.bgRect.topleft[0] + baseWidth * 2.5, self.bgRect.topleft[1] + baseHeight // 2 + self.textOffsetY  // 2 * k))
            self.window.blit(text, textRect)
            k = k + 1
        for info in enemyInfo:
            text = self.font.render(info, True, self.fontColor)
            textRect = text.get_rect(topleft = (self.bgRect.topleft[0] + baseWidth * 6, self.bgRect.topleft[1] + baseHeight // 2 + self.textOffsetY  // 2 * j))
            self.window.blit(text, textRect)
            j = j + 1

            # 渲染角色和装备
        if self.enemy.HP <= 0 :
            self.window.blit(self.deadEnemyImage, self.deadEnemyImageRect)
        else:
            self.window.blit(self.EnemyBattleImage, self.EnemyBattleImageRect)  
        #self.window.blit(self.EnemyBattleImage, self.EnemyBattleImageRect)
        self.window.blit(self.PlayerBattleImage, self.PlayerBattleImageRect)
        for item in self.inventory:
            if isinstance(item, Weapon):
                WeaponImage = pygame.transform.scale(item.image, (baseWidth // 2, baseWidth // 2 * item.image.get_size()[1] // item.image.get_size()[0]))
                WeaponImage_rect = WeaponImage.get_rect(center = (self.bgRect.topleft[0] + baseWidth * 4, self.bgRect.centery))
                self.window.blit(WeaponImage, WeaponImage_rect)
        
        # 动态计算战斗消息的位置
        if self.battleMessage and self.battleMessageCD > 0:
            battleMessageSurface = self.smallFont.render(self.battleMessage, True, self.battleMessageColor)
            message_x = (self.PlayerBattleImageRect.centerx + self.EnemyBattleImageRect.centerx) / 2 - battleMessageSurface.get_width() / 2
            message_y = min(self.PlayerBattleImageRect.top, self.EnemyBattleImageRect.top) - battleMessageSurface.get_height() - 10  # 略靠上，且不与玩家和敌人重合
            self.window.blit(battleMessageSurface, (message_x, message_y))

        if self.defeatMessage and self.defeatMessageCD > 0:
            defeatMessageSurface = self.smallFont.render(self.defeatMessage, True, self.defeatMessageColor)
            message_x = (self.PlayerBattleImageRect.centerx + self.EnemyBattleImageRect.centerx) / 2 - defeatMessageSurface.get_width() / 2
            message_y = min(self.PlayerBattleImageRect.top, self.EnemyBattleImageRect.top) - defeatMessageSurface.get_height() + 8  # 略靠上，且不与玩家和敌人重合
            self.window.blit(defeatMessageSurface, (message_x, message_y))

                                              
        # if self.playAnimation == False:
        if self.animation == None and self.animationEnemy == None:
        #     # 渲染选项
            for i, item in enumerate(self.inventory):
                text = self.font.render(str(item), True, self.fontColor)
                textRect = text.get_rect(topleft = (self.bgRect.topleft[0] + baseWidth // 2, self.bgRect.topleft[1] + baseHeight * 3 + self.textOffsetY * i))
                self.window.blit(text, textRect)
                if i == self.cursorIndex and self.cursorCD >= fps // 3:
                    pygame.draw.rect(self.window, (255, 255, 255), textRect)
                    if self.cursorCD >= fps // 3 * 2:
                        self.cursorCD = 0
            self.cursorCD += 1
        else:
            if self.animation != None:
                if self.animation.isPlaying:
                    self.animation.draw(self.window)
                    self.animation.update()
                else:
                    self.animation = None
            if self.animationEnemy != None:
                if self.animationEnemy.isPlaying:
                    self.animationEnemy.draw(self.window)
                    self.animationEnemy.update()
                else:
                    self.animationEnemy = None

    def update(self, keyDown):
        if self.enemy.HP <= 0:
            if self.defeatMessageCD > 0:
                enemyName, newSkill = self.get_message_from_enemy()
                self.defeatMessage = f"成功击败了 {enemyName}! {newSkill}"
            if self.defeatMessageCD > 0:
                self.defeatMessageCD -= 1
            else:
                self.close()
        if self.enemy.HP > 0:
            if keyDown == pygame.K_UP and self.cursorIndex > 0:
                self.move_cursor(-1)
            if keyDown == pygame.K_DOWN and self.cursorIndex < len(self.inventory) - 1:
                self.move_cursor(1)
            if keyDown == pygame.K_RETURN:
                if self.animation == None:
                    self.choose()
        
        # 更新战斗消息持续时间
        if self.battleMessageCD > 0:
            self.battleMessageCD -= 1
            if self.battleMessageCD == 0:
                self.battleMessage = ''
        
    def get_message_from_enemy(self):
        if isinstance(self.enemy, Enemy_Student):
            return '学生', 'money + 250'
        elif isinstance(self.enemy, Enemy_SIST):
            return '作战机器人', '获得技能超载冲击: 下一回合造成300%的综合ATK的伤害, money+250'
        elif isinstance(self.enemy, Enemy_SLST):
            return '转基因怪兽', '获得技能毒素注射: 使得敌人的防御力永久减少当前的20%, money+250'
        elif isinstance(self.enemy, Enemy_SPST):
            return '转基因怪兽', '获得技能合金护盾: 下一回合拥有300%的综合DEF, money+250'
        elif isinstance(self.enemy, Boss):
            return 'Boss', '游戏结束'
        


                
    def close(self):
        pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.player, 'money': GoldReward.value}))
        self.isFinished = True
    
    def choose(self):
        self.battleMessage = ''
        self.battleMessageCD = 60

        if str(self.inventory[self.cursorIndex])[4:] == 'Gun': # Gun 普攻
            if self.currentATK - self.enemy.DEF > 0:
                self.battleMessage = 'Gun造成了 ' + str(self.currentATK - self.enemy.DEF) + '点伤害!'
                self.animation = Animation(type = 'Gun')
                self.animation.play(self.effectPosition[self.animation.type].get('current', (0, 0)))
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy,'HP':-(self.currentATK - self.enemy.DEF)}))

        if str(self.inventory[self.cursorIndex])[4:] == 'Sword': # Sword 普攻
            if self.currentATK - self.enemy.DEF > 0:
                triggerProbability = random.random()
                if triggerProbability < 0.4 and self.enemy.HP > 0 and self.currentATK * 2 < self.enemy.DEF * 2 + self.enemy.HP:
                    self.battleMessage = 'Sword触发了40%概率的二段连击！'
                    self.animation = Animation(type = 'Sword2')
                    self.animation.play(self.effectPosition[self.animation.type].get('start', (0, 0)))
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy,'HP':-(self.currentATK - self.enemy.DEF)}))
                    if self.enemy.HP > 0:
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy,'HP':-(self.currentATK - self.enemy.DEF)}))
                else:
                    self.battleMessage = 'Sword造成了' + str(self.currentATK - self.enemy.DEF) + '点伤害!'
                    self.animation = Animation(type = 'Sword')
                    self.animation.play(self.effectPosition[self.animation.type].get('start', (0, 0)))
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy,'HP':-(self.currentATK - self.enemy.DEF)}))
                
        if str(self.inventory[self.cursorIndex])[4:] == 'Axe': # Axe 普攻
            if self.currentATK - self.enemy.DEF > 0:
                self.animation = Animation(type = 'Axe')
                self.animation.play(self.effectPosition[self.animation.type].get('current', (0, 0)))
                if random.random() >= 0.3:
                    self.battleMessage = 'Axe造成了' + str(self.currentATK - self.enemy.DEF) + '点伤害!'
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy,'HP':-(self.currentATK - self.enemy.DEF)}))
                else:
                    self.battleMessage = 'Axe触发了30%概率的破甲！'
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy,'HP':-self.currentATK}))
                    
        if str(self.inventory[self.cursorIndex]) == '空手': # 空手普攻
            if self.currentATK - self.enemy.DEF > 0:
                self.animation = Animation(type = 'Hand')
                self.animation.play(self.effectPosition[self.animation.type].get('current', (0, 0)))
                self.battleMessage = '空手造成了' + str(self.currentATK - self.enemy.DEF) + '点伤害!'
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy,'HP':-(self.currentATK - self.enemy.DEF)}))

        # 重置技能效果

        if self.lastSkillChoice == '超载冲击':
            self.currentATK = self.originalATK
            self.lastSkillChoice = None
        if self.lastSkillChoice == '毒素注射':
            self.lastSkillChoice = None

        # 使用技能
        if str(self.inventory[self.cursorIndex]) == '合金护盾':
            self.battleMessage = '使用合金护盾 下一轮防御力提升3倍!'
            self.animation = Animation(type = 'Shield')
            self.animation.play(self.effectPosition[self.animation.type].get('current', (0, 0)))
            self.currentDEF = self.originalDEF
            self.currentDEF *= 3
            self.currentSkillChoice = '合金护盾'

        if str(self.inventory[self.cursorIndex]) == '超载冲击':
            self.battleMessage = '使用超载冲击 下一轮攻击力提升3倍!'
            self.currentATK *= 3
            self.animation = Animation(type = 'Charge')
            self.animation.play(self.effectPosition[self.animation.type].get('current', (0, 0)))
            self.currentSkillChoice = '超载冲击'

        if str(self.inventory[self.cursorIndex]) == '毒素注射':
            self.battleMessage = '使用毒素注射 敌人DEF永久降低20%!'
            self.animation = Animation(type = 'Poison')
            self.animation.play(self.effectPosition[self.animation.type].get('current', (0, 0)))
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy, 'DEF':self.enemy.DEF * 0.8}))
            self.currentSkillChoice = '毒素注射'
        
        # 发动Gun的特殊效果
        if self.currentSkillChoice in ['合金护盾', '超载冲击', '毒素注射']:
            for item in self.inventory:
                if isinstance(item, Weapon):
                    if str(item)[4:] == 'Gun':
                        if self.currentATK / 2 - self.enemy.DEF > 0:
                            self.animation = Animation(type = 'Gun')
                            self.animation.play(self.effectPosition[self.animation.type].get('current', (0, 0)))
                            pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.enemy, 'HP':-(self.currentATK / 2 - self.enemy.DEF)})) # Gun的50%伤害固定发动
        
        # Enemy攻击
        if self.enemy.ATK - self.currentDEF > 0: # Enemy 对 Player 造成伤害
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_VALUECALLCULATE, value = {'sprite':self.player,'HP':-(self.enemy.ATK - self.currentDEF)})) 
            self.animationEnemy = Animation(type = 'Enemy')
            self.animationEnemy.play(self.effectPosition[self.animationEnemy.type].get('current', (0, 0)))
            
        # 重置护盾效果
        if self.lastSkillChoice == '合金护盾':
            self.currentDEF = self.originalDEF
            self.lastSkillChoice = None

        self.lastSkillChoice = self.currentSkillChoice
        self.currentSkillChoice = None