# -*- coding:utf-8 -*-

from typing import Tuple
import pygame,sys
import random
from typing import *
from Settings import *
from Item import item
from Settings import BattleSettings
class DialogBox:
    def __init__(self, window,order,texts:list,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        ##### Your Code Here ↓ #####
        self.order=order
        self.images=[pygame.transform.scale(pygame.image.load(img),
                    (WindowSettings.width,WindowSettings.height))
                    for img in GamePath.dialog_box]
        self.window = window
        self.texts=texts
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.fontColor2=(0,0,0)
        self.font = pygame.font.Font(r".\assets\font.TTF", self.fontSize)
        self.font1= pygame.font.Font(r".\assets\font.TTF", 24)
        self.bg = pygame.Surface((DialogSettings.boxWidth,
            DialogSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)
        ##### Your Code Here ↑ #####
        
    def draw(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    def render(self):
        ##### Your Code Here ↓ #####
        self.window.blit(self.images[self.order],(0,0))
        offset = 0
        for text in self.texts:
            self.window.blit(self.font.render(text,
                True, self.fontColor),
                (DialogSettings.textStartX, DialogSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        ##### Your Code Here ↑ #####

class BattleBox:
    def __init__(self,player, monster,fontSize: int = BattleSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), bgColor: Tuple[int, int, int, int] = (191, 171, 137, 200)) :
        ##### Your Code Here ↓ #####
        self.player = player
        self.monster = monster
        self.player_rect = BattleSettings.Player_rect
        self.monster_rect = BattleSettings.Monster_rect
        self.rect = BattleSettings.rect
        self.state = False
        self.bgColor = bgColor
        self.is_attacking = False
        self.being_attacked = False
        self.move_back_p = False
        self.move_back_m = False
        self.meanless_choice = False
        self.be_poisoned = 0
        self.attackweapon = None
        self.healing = False
        self.poisoning = False
        self.extra_settlement = False
        self.is_critical = False
        self.boss =False
        ##### Your Code Here ↑ #####
    def update(self):
        if self.monster.is_mimic:
            self.monster.image = pygame.transform.scale(pygame.image.load(GamePath.mimic),Monster_size[1])
        if self.is_attacking:
            if self.player_rect.colliderect(self.monster_rect):
                self.move_back_p = True
                self.attack_update(self.attackweapon)
            if self.player_rect == BattleSettings.Player_rect_0:
                if self.move_back_p == True:
                    self.is_attacking = False
                    self.being_attacked = True
                    pygame.time.delay(500)
                self.move_back_p =  False
            if not self.player_rect.colliderect(self.monster_rect) and not self.move_back_p:
                self.player_rect.x+=10
                self.player_rect.y-=10
            if self.player_rect != BattleSettings.Player_rect_0 and self.move_back_p:
                self.player_rect.x -= 10
                self.player_rect.y += 10
        if self.monster.HP<=0:
                    self.being_attacked = False
                    return
        if self.being_attacked:
            if self.monster_rect.colliderect(self.player_rect):
                self.move_back_m = True
                self.being_attacked_update()
            if self.monster_rect == BattleSettings.Monster_rect_0:
                if self.move_back_m == True:
                    self.being_attacked = False
                    pygame.time.delay(500)
                    self.extra_settlement = True
                    self.special_update()
                self.move_back_m = False
            if not self.monster_rect.colliderect(self.player_rect) and not self.move_back_m:
                self.monster_rect.x-=10
                self.monster_rect.y+=10
            if self.monster_rect != BattleSettings.Monster_rect_0 and self.move_back_m:
                self.monster_rect.x += 10
                self.monster_rect.y -= 10
    def attack_update(self,item):
        if item.wand == True:
            self.monster.HP = 0
            return
        if random.random()<=0.2:
            self.monster.HP=self.monster.HP-item.attack*2
            self.is_critical = True
        else:
            self.monster.HP=self.monster.HP-item.attack
    def being_attacked_update(self):    
        self.player.HP -= self.monster.attack
    def special_update(self):
        if self.be_poisoned:
            self.monster.HP-=self.be_poisoned
    def draw(self,window):
        ##### Your Code Here ↓ #####
        pygame.draw.rect(window, self.bgColor, self.rect)
        window.blit(pygame.transform.scale(self.player.images['back'][0],(PlayerSettings.playerWidth*2.5,PlayerSettings.playerHeight*2.5)),self.player_rect)
        self.print_detail(window)
        self.print_HP(self.player,BattleSettings.Player_HP_pos_x,BattleSettings.Player_HP_pos_y,window)
        self.print_HP(self.monster,BattleSettings.Monster_HP_pos_x,BattleSettings.Monster_HP_pos_y,window)
        if self.be_poisoned!=0:
            window.blit(pygame.transform.scale(self.monster.be_poisoned,(self.monster.rect[2]*2.5,self.monster.rect[3]*2.5)),self.monster_rect)       
        else:
            window.blit(pygame.transform.scale(self.monster.image,(self.monster.rect[2]*2.5,self.monster.rect[3]*2.5)),self.monster_rect)      
        ##### Your Code Here ↑ #####
    def print_HP(self, object,x,y,window):
        print_text('HP: '+str(object.HP),window,x,y)
        left = pygame.transform.scale(pygame.image.load(GamePath.HP[0]),(HPbox.size,HPbox.size))
        middle = pygame.transform.scale(pygame.image.load(GamePath.HP[1]),(HPbox.size,HPbox.size))
        right = pygame.transform.scale(pygame.image.load(GamePath.HP[2]),(HPbox.size,HPbox.size))
        left_empty = pygame.transform.scale(pygame.image.load(GamePath.HP[3]),(HPbox.size,HPbox.size))
        middle_empty = pygame.transform.scale(pygame.image.load(GamePath.HP[4]),(HPbox.size,HPbox.size))
        right_empty = pygame.transform.scale(pygame.image.load(GamePath.HP[5]),(HPbox.size,HPbox.size))
        y+=40
        window.blit(left_empty,(x,y,HPbox.size,HPbox.size))
        dx = HPbox.size
        for i in range(1,object.init_HP-1):
            window.blit(middle_empty,(x+dx,y,HPbox.size,HPbox.size))
            dx += HPbox.size
        window.blit(right_empty,(x+dx,y,HPbox.size,HPbox.size))
        dx = HPbox.size
        if object.HP>0:
            window.blit(left,(x,y,HPbox.size,HPbox.size))
            for i in range(1,object.HP-1):
                window.blit(middle,(x+dx,y,HPbox.size,HPbox.size))
                dx += HPbox.size
            if object.HP == object.init_HP:
                window.blit(right,(x+dx,y,HPbox.size,HPbox.size))
            else:
                 window.blit(middle,(x+dx,y,HPbox.size,HPbox.size))
        # for i in range(object.init_HP):
        #     window.blit()
    def print_detail(self,window):
        self.box = pygame.image.load(GamePath.battle_detail)
        window.blit(self.box,(0,0))
        if self.attackweapon !=None and self.is_attacking and self.monster.HP>0:
            if self.is_critical:
                print_text('你对敌人使用' + self.attackweapon.name + '造成暴击!',window,WindowSettings.width*10/100,WindowSettings.height*72/100)    
            else:
                print_text('你对敌人使用' + self.attackweapon.name + '攻击',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
        if self.being_attacked and self.player.HP>0:
            print_text('你被敌人攻击',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
        if self.meanless_choice:
            print_text('这不是一件有效的物品',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
        if self.healing:
            print_text('你使用生命药水恢复五点生命值！',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
        if self.poisoning:
            print_text('！敌人中毒！',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
        if self.be_poisoned !=0 and self.extra_settlement:
            print_text('敌人中毒，受到一点伤害',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
        if self.player.HP<=0:
            print_text('寄',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
        elif self.monster.HP<=0:
            if self.monster.is_mimic:
                print_text('获得油灯\n （这里究竟是什么情况，我最好回去找村长询问一下）',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
            else:
                if self.player.EX==1 or self.player.EX==2:
                    print_text('胜利 EX: '+str(self.player.EX+1)+'战斗的经验使武器变得更强了',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
                else:
                    print_text('胜利',window,WindowSettings.width*10/100,WindowSettings.height*72/100)
class ShoppingBox:
    def __init__(self, window, npc, player,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def buy(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
class BackpackBox:
    def __init__(self,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (139, 69, 19, 128)):
        ##### Your Code Here ↓ #####
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.bgColor = bgColor
        self.state = False
        self.CD = BackpackSettings.CD
        self.last_time_pressed = 0
        self.items = pygame.sprite.Group()
        self.selecting = 0
        self.image = pygame.image.load(GamePath.backpack)
        self.image = pygame.transform.scale(self.image,(400,600))
        #### Your Code Here ↑ #####
        self.add_item(Items.letter,(type.weapon,1))
        self.add_item(Items.poison,(type.poison,1))
        self.add_item(Items.achieve_list)
    def add_item(self, tmp : Items, item_type = (0,0)):
        tmp_item = item(pygame.image.load(GamePath.items[tmp.value]), BackpackSettings.backpack_rect[0] , BackpackSettings.backpack_rect[1])
        tmp_item.text = itemtext[tmp.value]
        tmp_item.name = tmp.name

        if item_type[0] == type.weapon :
            tmp_item.attack = item_type[1]
        if item_type[0] == type.healing :
            tmp_item.healing = item_type[1]
        if item_type[0] == type.poison :
            tmp_item.poison = item_type[1]
        if item_type[0] == type.magic_wand :
            tmp_item.wand = True
        self.items.add(tmp_item)
    def remove_item(self, tmp : Items):
        for x in self.items:
            if x.name == tmp.name:
                self.items.remove(x)
    def add_achieve(self,text):
        self.remove_item(Items.achieve_list)
        itemtext[Items.achieve_list.value]=itemtext[Items.achieve_list.value]+'\n'+text
        self.add_item(Items.achieve_list)
    def draw(self, window):
        ##### Your Code Here ↓ #####
        # pygame.draw.rect(window, self.bgColor, BackpackSettings.backpack_rect)
        window.blit(self.image,(50,50))
        window.blit(pygame.transform.scale(pygame.image.load(GamePath.UI),(400,450)),(500,50))
        dx = 36
        dy = -11
        num = 0
        for tmp_item in self.items:
            if num%4==0:
                dx = 36
                dy +=BackpackSettings.item_size+7
            if num == self.selecting:
                text = tmp_item.text
                print_text(text,window,WindowSettings.width*40/100,WindowSettings.height*20/100,20)
            tmp_item.draw(window,num == self.selecting,dx,dy)
            dx+=BackpackSettings.item_size+2
            num +=1
    def battle_draw(self,window):
        window.blit(self.image,(50,50))
        dx = 36
        dy = -11
        num = 0
        font = pygame.font.Font(pygame.font.get_default_font(), 40)
        for tmp_item in self.items:
            if num%4==0:
                dx = 36
                dy +=BackpackSettings.item_size+7
            tmp_item.draw(window,num == self.selecting,dx,dy)
            dx+=BackpackSettings.item_size+2
            num +=1
    def boss_draw(self,window):
        window.blit(self.image,(50,500))
        dx = 36
        dy = -11
        num = 0
        font = pygame.font.Font(pygame.font.get_default_font(), 40)
        for tmp_item in self.items:
            if num%4==0:
                dx = 36
                dy +=BackpackSettings.item_size+7
            tmp_item.draw(window,num == self.selecting,dx,dy)
            dx+=BackpackSettings.item_size+2
            num +=1
    def update(self, keys):
        if keys[pygame.K_w] and self.selecting-4 >=0:
            self.selecting-=4
        if keys[pygame.K_s] and self.selecting+4 <= len(GamePath.items)-1:
            self.selecting+=4
        if keys[pygame.K_a] and self.selecting-1 >=0:
            self.selecting-=1
        if keys[pygame.K_d] and self.selecting+1 <= len(GamePath.items)-1:
            self.selecting+=1
        if any(keys):
            self.last_time_pressed = pygame.time.get_ticks()
    def battle_update(self, keys, battle_box : BattleBox):
        if keys[pygame.K_w] and self.selecting-4 >=0:
            self.selecting-=4
        if keys[pygame.K_s] and self.selecting+4 <= len(GamePath.items)-1:
            self.selecting+=4
        if keys[pygame.K_a] and self.selecting-1 >=0:
            self.selecting-=1
        if keys[pygame.K_d] and self.selecting+1 <= len(GamePath.items)-1:
            self.selecting+=1
        if any(keys):
            self.last_time_pressed = pygame.time.get_ticks()
            num = 0
            battle_box.healing = False
            battle_box.poisoning = False
            battle_box.extra_settlement = False
            battle_box.is_critical = False
            if battle_box.monster.HP <= 0 or battle_box.player.HP <= 0:
                    battle_box.state = False
            if keys[pygame.K_RETURN]:
                for item in self.items:
                    if num == self.selecting:
                        if battle_box.meanless_choice== True:
                            battle_box.meanless_choice = False
                        if item.attack != 0 or item.wand == True:
                            battle_box.is_attacking = True
                            # battle_box.attack_update(item)
                            # battle_box.being_attacked_update()
                            battle_box.attackweapon = item
                        elif item.healing != 0:
                            if battle_box.player.HP+item.healing <=PlayerSettings.init_playerHP:
                                battle_box.player.HP+=item.healing
                            else:
                                battle_box.player.HP=PlayerSettings.init_playerHP
                            self.remove_item(item)
                            self.add_item(Items.empty_bottle)
                            battle_box.healing = True
                        elif item.poison != 0:
                            battle_box.be_poisoned += item.poison
                            self.remove_item(item)
                            battle_box.poisoning = True
                        else:
                            battle_box.meanless_choice = True
                    num+=1
class SelfBox:
    def __init__(self,texts,type):
        self.texts = texts
        self.index = 0
        self.image = pygame.image.load(GamePath.dialog_box[0])
        self.rect = self.image.get_rect()
        self.state = True
        self.last_time_pressed = 0
        self.CD = 500
        self.type = type
    def draw(self,window):
        window.blit(self.image,self.rect)
        print_text(self.texts[self.index],window,220,565,30)
    def update(self,keys):
        if keys[pygame.K_RETURN]:
            self.index+=1
        if self.index==len(self.texts):
            self.state = False
            talkover[self.type.value]=True
            pygame.time.delay(500)

            


def print_text(text, window, x, y , size=40):
    tmp_text = text
    textlist = text.split('\n')
    dy=0
    font = pygame.font.Font(pygame.font.match_font('幼圆'), size)
    for i in textlist:
        text_surface = font.render(i, True, (255, 255, 255))
        text_position = (x, y+dy)
        window.blit(text_surface, text_position)
        dy+=30

def print_text_withbox(text,window, x, y):
    tmp_text = str(text)
    font = pygame.font.Font(pygame.font.match_font('幼圆'), 40)
    text_surface = font.render(tmp_text,True,(0,0,0))
    text_rect = text_surface.get_rect()
    box = pygame.transform.scale(pygame.image.load(GamePath.UI),(text_rect.width,text_rect.height))
    text_position = (x,y)
    window.blit(box,text_position)
    window.blit(text_surface,text_position)
