from Setting import GamePath
import pygame
import random
'''
Weapon class
'''

class Weapon():
    def __init__(self, name, image, ATK, DEF, description = ""):
        self.name = name
        self.image = pygame.image.load(image)
        self.ATK = ATK
        self.DEF = DEF
        self.description = description
        
    def __str__(self) -> str:
        return self.name
    '''
    We will have many pre-defined weapons in the game.
    They only have their own name, image, effect(img)
    '''
    @staticmethod
    def predefined_weapon_templates():
        return [
            ("Sword", GamePath.weaponSword, '在战斗中有40%概率触发二段连击,总和造成两倍于综合ATK伤害'),
            ("Axe", GamePath.weaponAxe, '在战斗中有30%概率触发破甲, 当前攻击无视对方DEF'),
            ("Gun", GamePath.weaponGun, '可以在使用技能的回合发动攻击, 造成50%综合ATK的伤害') 
        ]


    def get_weapon():
        weapon_templates = Weapon.predefined_weapon_templates()
        random_template = random.choice(weapon_templates)
        weapon = Weapon(random_template[0], random_template[1], ATK = random.randint(400, 600), DEF = random.randint(100, 200), description=random_template[2])
        if weapon.ATK // 5 + weapon.DEF // 1.5 > 220:
            weapon.name = "[传说]" + weapon.name
        elif weapon.ATK // 5 + weapon.DEF // 2 > 190:
            weapon.name = "[史诗]" + weapon.name
        elif weapon.ATK // 5 + weapon.DEF // 2 > 170:
            weapon.name = "[稀有]" + weapon.name
        else:
            weapon.name = "[普通]" + weapon.name
        return weapon
    
        
