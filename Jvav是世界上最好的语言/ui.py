import pygame

from Settings import *
from Player import Player
from typing import Tuple


class UI:
    def __init__(self,window,fontSize: int = DialogSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255)):
        self.window=window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UISettings.ui_font, UISettings.ui_font_size)
        self.blood_bar_rect = pygame.Rect(12, 12, UISettings.blood_bar_width, UISettings.bar_height)
        self.mana_bar_rect = pygame.Rect(12, 40, UISettings.mana_bar_width, UISettings.bar_height)
        self.weapons = [pygame.transform.scale(pygame.image.load(weapon),
                                               (UISettings.item_box_size - 10, UISettings.item_box_size - 10))
                        for weapon in WeaponsImagePaths.WEAPON]
        self.hp=PlayerSettings.playerHP
        self.mp=PlayerSettings.playerMP
        self.gold=0
        self.suppliesImage=[pygame.transform.scale(pygame.image.load(img),(SupplySettings.width,SupplySettings.height)) for img in SupplySettings.Image]
        self.suppliesRect=[pygame.Rect(WindowSettings.width-100,12+SupplySettings.height*(2*i),SupplySettings.width,SupplySettings.height) for i in range(3)]
    
    def GetPlayerStatus(self,hp,mp,gold,hPortion,mPortion):
        self.hp=hp
        self.mp=mp
        self.supplies=[hPortion,mPortion,gold]

    def show_bar(self, current, max_amount, bg_rect, color, type):
        ratio = current*1.0/max_amount
        current_rect = pygame.Rect(12, 12+(40-12)*type, UISettings.blood_bar_width*ratio, UISettings.bar_height)
        pygame.draw.rect(self.display_surface, color, current_rect)
    
    def ShowStatus(self):
        self.window.blit(self.font.render("HP: "+str(self.hp),True,self.fontColor)
                         ,(32+UISettings.blood_bar_width,12))
        self.window.blit(self.font.render("MP: "+str(self.mp),True,self.fontColor)
                         ,(32+UISettings.blood_bar_width,40))

    # 武器框
    def selected_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, UISettings.item_box_size, UISettings.item_box_size)
        pygame.draw.rect(self.display_surface, UISettings.ui_bg_color, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UISettings.ui_border_color_active, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UISettings.ui_border_color, bg_rect, 3)
        return bg_rect

    def weapons_in_box(self, weapon_index, has_switched):
        bg_rect = self.selected_box(20, 600, has_switched)
        weapon_surf = self.weapons[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def suppliesRender(self):
        for i in range(3):
            self.window.blit(self.suppliesImage[i],self.suppliesRect[i])
            self.window.blit(
                self.font.render(str(self.supplies[i]),True,self.fontColor)
                ,(WindowSettings.width-60,12+SupplySettings.height*(2*i))
            )

    def display(self, player):
        self.show_bar(self.hp, PlayerSettings.playerHP,
                      self.blood_bar_rect, UISettings.blood_color,0)
        self.show_bar(self.mp, PlayerSettings.playerMP,
                      self.mana_bar_rect, UISettings.mana_color,1)
        self.weapons_in_box(player.weapon_index, not player.can_switch_weapon)
        self.suppliesRender()
        self.ShowStatus()
    
    def GameSuccess(self,duration):
        self.window.blit(
            self.font.render("Congratulations!",True,self.fontColor)
                ,(WindowSettings.width//2,WindowSettings.height//2)
        )
        self.window.blit(
            self.font.render("Game Time: "+str(duration)+" seconds",True,self.fontColor)
                ,(WindowSettings.width//2,WindowSettings.height//2+SupplySettings.height)
        )
        self.window.blit(
            self.font.render("Game will close after 5 seconds...",True,self.fontColor)
                ,(WindowSettings.width//2,WindowSettings.height//2+2*SupplySettings.height)
        )
    
    def GameFail(self):
        self.window.blit(
            self.font.render("Fail!",True,self.fontColor)
                ,(WindowSettings.width//2,WindowSettings.height//2)
        )
        self.window.blit(
            self.font.render("Game will close after 5 seconds...",True,self.fontColor)
                ,(WindowSettings.width//2,WindowSettings.height//2+SupplySettings.height)
        )