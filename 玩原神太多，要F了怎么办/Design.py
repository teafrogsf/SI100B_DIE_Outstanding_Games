# -*- coding:utf-8 -*-

import pygame

import Settings
from GameLogic import *


def load_map(filepath):
    map_data = []
    with open(filepath, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            if row == []:
                continue
            map_data.append(row)
    return map_data


class MapInfo:
    detail = {
        "name": [
            "无名之地",
            "中心地",
            "群岛"
        ]
    }


class GroundMatrix:
    map = []
    map.append(load_map("./maps/newbie_ground_map.txt"))
    map.append(load_map("./maps/town_ground_map.txt"))
    map.append(load_map("./maps/island_ground_map.txt"))

# 1: Bush, 2: Grass, 3: Flower, 4: Tree 注意tree是写左上角格子位置，所以另外四个都必需留0


class BushGrassFlowerTreeMatrix:
    map = []
    map.append(load_map("./maps/newbie_item_map.txt"))
    map.append(load_map("./maps/town_item_map.txt"))
    map.append(load_map("./maps/island_item_map.txt"))

# 每张地图两个出生点，一个是没开神像前的，开神像后是另一个点
# 上面是在乱说


class BirthInfo:
    point = [(42, 49),
             (2, 23),
             (2, 2)
             ]
    direction = [0,
                 3,
                 1
                 ]

# 相机的初始位置，与上面的出生点坐标相关（这东西目前好像没啥用了）


# class CameraInitialTopLeft:
#     map = [[(0, 0), (0, 0)],
#            [(0, 0), (0, 0)],
#            [(0, 0), (0, 0)]
#            ]

class CatCake:
    es = {      # every single catcake
        "cat_trash": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_01.png",
            "dead": r".\assets\catcake\dead\cake_01_dead.png",
            "hp": 100,
            "atk": 25,
            "def": 15,
            "gold": 100,
            "flavor": [Settings.FlavorInfo.STRANGE, Settings.FlavorInfo.BITTER],
            "name": "垃圾糕"
        },
        "Marisa's cat_trash": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_01.png",
            "dead": r".\assets\catcake\dead\cake_01_dead.png",
            "hp": 80,
            "atk": 18,
            "def": 18,
            "gold": 100,
            "flavor": [Settings.FlavorInfo.STRANGE, Settings.FlavorInfo.BITTER],
            "name": "垃圾糕"
        },
        "Sanae's cat_trash": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_01.png",
            "dead": r".\assets\catcake\dead\cake_01_dead.png",
            "hp": 70,
            "atk": 18,
            "def": 18,
            "gold": 100,
            "flavor": [Settings.FlavorInfo.STRANGE, Settings.FlavorInfo.BITTER],
            "name": "垃圾糕"
        },
        "Cirno's cat_trash": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_01.png",
            "dead": r".\assets\catcake\dead\cake_01_dead.png",
            "hp": 120,
            "atk": 40,
            "def": 40,
            "gold": 100,
            "flavor": [Settings.FlavorInfo.STRANGE, Settings.FlavorInfo.BITTER],
            "name": "垃圾糕"
        },
        "Youmu's cat_trash": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_01.png",
            "dead": r".\assets\catcake\dead\cake_01_dead.png",
            "hp": 200,
            "atk": 60,
            "def": 60,
            "gold": 100,
            "flavor": [Settings.FlavorInfo.STRANGE, Settings.FlavorInfo.BITTER],
            "name": "垃圾糕"
        },
        "cat_ice": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_02.png",
            "dead": r".\assets\catcake\dead\cake_02_dead.png",
            "hp": 150,
            "atk": 18,
            "def": 30,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.COLD, Settings.FlavorInfo.SWEET],
            "name": "冰糕"
        },
        "Sanae's cat_ice": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_02.png",
            "dead": r".\assets\catcake\dead\cake_02_dead.png",
            "hp": 70,
            "atk": 15,
            "def": 20,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.COLD, Settings.FlavorInfo.SWEET],
            "name": "冰糕"
        },
        "Cirno's cat_ice": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_02.png",
            "dead": r".\assets\catcake\dead\cake_02_dead.png",
            "hp": 180,
            "atk": 30,
            "def": 50,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.COLD, Settings.FlavorInfo.SWEET],
            "name": "冰糕"
        },
        "Youmu's cat_ice": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_02.png",
            "dead": r".\assets\catcake\dead\cake_02_dead.png",
            "hp": 250,
            "atk": 50,
            "def": 70,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.COLD, Settings.FlavorInfo.SWEET],
            "name": "冰糕"
        },
        "cat_mochi": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_03.png",
            "dead": r".\assets\catcake\dead\cake_03_dead.png",
            "hp": 150,
            "atk": 30,
            "def": 18,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.SALTY, Settings.FlavorInfo.STICKY],
            "name": "糯米团"
        },
        "Sanae's cat_mochi": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_03.png",
            "dead": r".\assets\catcake\dead\cake_03_dead.png",
            "hp": 70,
            "atk": 25,
            "def": 15,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.SALTY, Settings.FlavorInfo.STICKY],
            "name": "糯米团"
        },
        "Cirno's cat_mochi": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_03.png",
            "dead": r".\assets\catcake\dead\cake_03_dead.png",
            "hp": 180,
            "atk": 50,
            "def": 30,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.SALTY, Settings.FlavorInfo.STICKY],
            "name": "糯米团"
        },
        "Youmu's cat_mochi": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_03.png",
            "dead": r".\assets\catcake\dead\cake_03_dead.png",
            "hp": 250,
            "atk": 70,
            "def": 50,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.SALTY, Settings.FlavorInfo.STICKY],
            "name": "糯米团"
        },
        "cat_flower": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_04.png",
            "dead": r".\assets\catcake\dead\cake_04_dead.png",
            "hp": 80,
            "atk": 40,
            "def": 40,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.SWEET, Settings.FlavorInfo.STRANGE],
            "name": "梅花糕"
        },
        "Cirno's cat_flower": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_04.png",
            "dead": r".\assets\catcake\dead\cake_04_dead.png",
            "hp": 120,
            "atk": 60,
            "def": 60,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.SWEET, Settings.FlavorInfo.STRANGE],
            "name": "梅花糕"
        },
        "Youmu's cat_flower": {
            # "battle" :
            # "gif" :
            "preview": r".\assets\catcake\preview\cake_04.png",
            "dead": r".\assets\catcake\dead\cake_04_dead.png",
            "hp": 150,
            "atk": 100,
            "def": 100,
            "gold": 110,
            "flavor": [Settings.FlavorInfo.SWEET, Settings.FlavorInfo.STRANGE],
            "name": "梅花糕"
        }
    }


class Skills:
    es = {      # every single skill
        "A": {
            "card": r".\assets\skill\A.png",
            "preview": r".\assets\skill\A.png",
            "name": "至尊平A！",
            "id": "A",
            "description": "帝国の绝雄猫糕！至尊平A",
            "short_des": "帝国の绝雄猫糕！至尊平A",
            "r": 1,
            "pp": -1,
            "skillAnimateTime": 12,
            "animate": Settings.SkillSettings.AttackPath,
            "execute": [ExeSkill(0, "enemy", {"hp": {"apply": "atk", "whose": "cake", "num": -1}})]
        },
        "skill_red": {
            "card": r".\assets\skill\red.png",
            "preview": r".\assets\skill\red_preview.png",
            "name": "猫糕遨游之夜",
            "id": "red",
            "description": "人类从不掩饰掌控星空的欲望...当然，也包括猫糕在内(?) 使用此技能，对敌方连续三个目标以自身攻击力80%发动攻击",
            "short_des": "对敌方连续三个猫糕造成一定伤害",
            "r": 3,
            "pp": 2,
            "skillAnimateTime": 12,
            "animate": Settings.SkillSettings.AttackPath,
            "execute": [ExeSkill(-1, "enemy", {"hp": {"apply": "atk", "whose": "cake", "num": -0.8}}),\
                        ExeSkill(0, "enemy", {"hp": {"apply": "atk", "whose": "cake", "num": -0.8}}),\
                        ExeSkill(1, "enemy", {"hp": {"apply": "atk", "whose": "cake", "num": -0.8}})]
        },
        "skill_yellow": {
            "card": r".\assets\skill\yellow.png",
            "preview": r".\assets\skill\yellow_preview.png",
            "name": "糕的回响",
            "id": "yellow",
            "description": "猫糕这么可爱，怎么可以伤害猫糕！ 使用此技能，为我方所有猫糕回复等同于自身防御力50%的生命值，回复的生命值不会超过生命值上限",
            "short_des": "根据防御力为我方所有猫糕回复少量生命值",
            "r": 4,
            "pp": 2,
            "cd": 0,
            "skillAnimateTime": 12,
            "animate": Settings.SkillSettings.HealPath,
            "execute": [ExeSkill(0, "self", {"hp": {"apply": "def", "whose": "cake", "num": 0.5}}),\
                        ExeSkill(1, "self", {"hp": {"apply": "def", "whose": "cake", "num": 0.5}}),\
                        ExeSkill(2, "self", {"hp": {"apply": "def", "whose": "cake", "num": 0.5}}),\
                        ExeSkill(3, "self", {"hp": {"apply": "def", "whose": "cake", "num": 0.5}}),]
        },
        "skill_ice": {
            "card": r".\assets\skill\ice.png",
            "preview": r".\assets\skill\ice_preview.png",
            "name": "以糕为剑",
            "id": "ice",
            "description": "胜利是需要牺牲的，必要的牺牲是值得的！使用此技能，自爆，并对敌方所有目标以当前血量的80%为攻击力发动攻击",
            "short_des": "牺牲自己，以此对所有敌方目标造成伤害",
            "r": 4,
            "pp": 2,
            "skillAnimateTime": 12,
            "animate": Settings.SkillSettings.AttackPath,
            "execute": [ExeSkill(0, "enemy", {"hp": {"apply": "hp", "whose": "cake", "num": -0.8}}),\
                        ExeSkill(1, "enemy", {"hp": {"apply": "hp", "whose": "cake", "num": -0.8}}),\
                        ExeSkill(2, "enemy", {"hp": {"apply": "hp", "whose": "cake", "num": -0.8}}),\
                        ExeSkill(3, "enemy", {"hp": {"apply": "hp", "whose": "cake", "num": -0.8}}),\
                        ExeSkill(0, "self", {"hp": {"apply": "hp", "whose": "cake", "num": -100}}),]
        },
        "skill_pink": {
            "card": r".\assets\skill\pink.png",
            "preview": r".\assets\skill\pink_preview.png",
            "name": "记忆中的糕",
            "id": "pink",
            "description": "记忆是人类最宝贵的东西，也是猫糕最宝贵的东西！使用此技能，使全体己方猫糕攻击和防御属性变为1.2倍",
            "short_des": "给所有己方猫糕buff",
            "r": 4,
            "pp": 2,
            "skillAnimateTime": 12,
            "animate": Settings.SkillSettings.EnhancePath,
            "execute": [ExeSkill(0, "self", {"atk": {"apply": "atk", "whose": "self", "num": 0.2}}),\
                        ExeSkill(0, "self", {"def": {"apply": "def", "whose": "self", "num": 0.2}}),\
                        ExeSkill(1, "self", {"atk": {"apply": "atk", "whose": "self", "num": 0.2}}),\
                        ExeSkill(1, "self", {"def": {"apply": "def", "whose": "self", "num": 0.2}}),\
                        ExeSkill(2, "self", {"atk": {"apply": "atk", "whose": "self", "num": 0.2}}),\
                        ExeSkill(2, "self", {"def": {"apply": "def", "whose": "self", "num": 0.2}}),\
                        ExeSkill(3, "self", {"atk": {"apply": "atk", "whose": "self", "num": 0.2}}),\
                        ExeSkill(
                            3, "self", {"def": {"apply": "def", "whose": "self", "num": 0.2}})
                        ]
        },
        "skill_cyan": {
            "card": r".\assets\skill\cyan.png",
            "preview": r".\assets\skill\cyan_preview.png",
            "name": "猫猫漫步",
            "id": "cyan",
            "description": "猫猫总是容易分心，让敌方分心或许有利于战斗的胜利呢。使用此技能，让全体敌方猫糕攻击和防御变为0.8倍",
            "short_des": "给所有对方猫糕debuff",
            "r": 4,
            "pp": 2,
            "skillAnimateTime": 12,
            "animate": Settings.SkillSettings.EnhancePath,
            "execute": [ExeSkill(0, "enemy", {"atk": {"apply": "atk", "whose": "self", "num": -0.2}}),\
                        ExeSkill(0, "enemy", {"def": {"apply": "def", "whose": "self", "num": -0.2}}),\
                        ExeSkill(1, "enemy", {"atk": {"apply": "atk", "whose": "self", "num": -0.2}}),\
                        ExeSkill(1, "enemy", {"def": {"apply": "def", "whose": "self", "num": -0.2}}),\
                        ExeSkill(2, "enemy", {"atk": {"apply": "atk", "whose": "self", "num": -0.2}}),\
                        ExeSkill(2, "enemy", {"def": {"apply": "def", "whose": "self", "num": -0.2}}),\
                        ExeSkill(3, "enemy", {"atk": {"apply": "atk", "whose": "self", "num": -0.2}}),\
                        ExeSkill(3, "enemy", {
                                 "def": {"apply": "def", "whose": "self", "num": -0.2}})
                        ]
        }
    }


class BellDetail:
    map = {
        "bell1": {
            "area": 0,
            "destination": 1,
            "x": 28,
            "y": 19,
            "text": [
                "是否敲钟？敲钟将前往区域1：中心地"
            ],
            "options": [
                ["敲敲敲", "让我康康下张地图", "不敲不敲"]
            ],
            "execute": [
                [[ExeProcess("map", 1), ExeTP(BirthInfo.point[1][0], BirthInfo.point[1][1], dir=BirthInfo.direction[1], area=1)],
                 [ExeProcess("map", 1), ExeTP(
                     BirthInfo.point[1][0], BirthInfo.point[1][1], dir=BirthInfo.direction[1], area=1)],
                 [ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png"
            ],
            "scale": [
                (350, 550)
            ],
            "imgxy": [
                (95, 70)
            ],
            "hint": "进入钟楼"
        },
        "bell2": {
            "area": 1,
            "destination": 2,
            "x": 71,
            "y": 12,
            "text": [
                "是否敲钟？敲钟将前往区域2：群岛"
            ],
            "options": [
                ["敲敲敲", "让我康康下张地图", "不敲不敲"]
            ],
            "execute": [
                [[ExeProcess("map", 2), ExeTP(BirthInfo.point[2][0], BirthInfo.point[2][1], dir=BirthInfo.direction[2], area=2)],
                 [ExeProcess("map", 2), ExeTP(
                     BirthInfo.point[2][0], BirthInfo.point[2][1], dir=BirthInfo.direction[2], area=2)],
                 [ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png"
            ],
            "scale": [
                (350, 550)
            ],
            "imgxy": [
                (95, 70)
            ],
            "hint": "进入钟楼"
        }
    }


class SpecialDetail:
    map = {
        "pinktree": {
            "area": 1,
            "x": 36,
            "y": 14,
            "img": r".\assets\map\pinktree.png",
            "width": 380,
            "height": 415,
            "rect_height": 120,
            "rect_width": 248
        }
    }


class ShopDetail:
    catergory = ["属性加成", "猫糕", "技能卡"]
    map = {
        "shop_under_pinktree": {
            "area": 1,
            "surface": r".\assets\figure\1.png",
            "x": 37,
            "y": 26,
            "text": [
                "欢迎来到薄利大商店，只要有钱就什么都能买到哦~",
            ],
            "options": [
                ["进入商店", "关闭"],
            ],
            "execute": [
                [[ExeClose(), ExeOpenShop()], [ExeClose()]],
            ],
            "img": [
                r".\assets\figure\001_07.png"
            ],
            "scale": [
                (515, 550)
            ],
            "imgxy": [
                (8, 70)
            ],
            "goods": [
                {
                    "number": 0,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点攻击力(1)",
                    "price": 100,
                    "execute": [ExeAttribute("atk", 10)],
                    "premise": []
                },
                {
                    "number": 1,
                    "img": None,
                    "sort": 0,
                    "description": "增加20点生命值(1)",
                    "price": 100,
                    "execute": [ExeAttribute("hp", 20)],
                    "premise": []
                },
                {
                    "number": 2,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点防御力(1)",
                    "price": 100,
                    "execute": [ExeAttribute("def", 10)],
                    "premise": []
                },
                {
                    "number": 3,
                    "img": None,
                    "sort": 0,
                    "description": "增加20%金币获取率(1)",
                    "price": 150,
                    "execute": [ExeAttribute("gold", 20)],
                    "premise": []
                },
                {
                    "number": 4,
                    "img": r".\assets\skill\yellow_preview.png",
                    "sort": 2,
                    "description": "糕的回响：为我方所有猫糕回复少量生命值",
                    "price": 300,
                    "execute": [ExeProcess("skill", "skill_yellow")],
                    "premise": []
                },
                {
                    "number": 5,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点攻击力(2)",
                    "price": 300,
                    "execute": [ExeAttribute("atk", 10)],
                    "premise": [0]
                },
                {
                    "number": 6,
                    "img": None,
                    "sort": 0,
                    "description": "增加20点生命值(2)",
                    "price": 300,
                    "execute": [ExeAttribute("hp", 20)],
                    "premise": [1]
                },
                {
                    "number": 7,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点防御力(2)",
                    "price": 300,
                    "execute": [ExeAttribute("def", 10)],
                    "premise": [2]
                },
                {
                    "number": 8,
                    "img": None,
                    "sort": 0,
                    "description": "增加20%金币获取率(2)",
                    "price": 500,
                    "execute": [ExeAttribute("gold", 20)],
                    "premise": [3]
                },
                {
                    "number": 10,
                    "img": r".\assets\skill\pink_preview.png",
                    "sort": 2,
                    "description": "记忆中的糕：给所有己方猫糕buff",
                    "price": 300,
                    "execute": [ExeProcess("skill", "skill_pink")],
                    "premise": []
                },
                {
                    "number": 11,
                    "img": r".\assets\skill\cyan_preview.png",
                    "sort": 2,
                    "description": "猫猫漫步：给所有对方猫糕debuff",
                    "price": 300,
                    "execute": [ExeProcess("skill", "skill_cyan")],
                    "premise": []
                },
                {
                    "number": 12,
                    "img": r".\assets\catcake\preview\cake_03.png",
                    "sort": 1,
                    "description": "糯米团：hp150 atk30 def18 gold110%",
                    "price": 300,
                    "execute": [ExeProcess("cat", "cat_mochi")],
                    "premise": []
                },
                {
                    "number": 13,
                    "img": r".\assets\catcake\preview\cake_04.png",
                    "sort": 1,
                    "description": "梅花糕：hp80 atk40 def40 gold110%",
                    "price": 300,
                    "execute": [ExeProcess("cat", "cat_flower")],
                    "premise": []
                },
                {
                    "number": 14,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点攻击力(3)",
                    "price": 300,
                    "execute": [ExeAttribute("atk", 10)],
                    "premise": [5]
                },
                {
                    "number": 15,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点攻击力(4)",
                    "price": 300,
                    "execute": [ExeAttribute("atk", 10)],
                    "premise": [14]
                },
                {
                    "number": 16,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点攻击力(5)",
                    "price": 300,
                    "execute": [ExeAttribute("atk", 10)],
                    "premise": [15]
                },
                {
                    "number": 17,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点攻击力(6)",
                    "price": 300,
                    "execute": [ExeAttribute("atk", 10)],
                    "premise": [16]
                },
                {
                    "number": 18,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点攻击力(7)",
                    "price": 300,
                    "execute": [ExeAttribute("atk", 10)],
                    "premise": [17]
                },
                {
                    "number": 19,
                    "img": None,
                    "sort": 0,
                    "description": "增加20点生命值(3)",
                    "price": 100,
                    "execute": [ExeAttribute("hp", 20)],
                    "premise": [6]
                },
                {
                    "number": 20,
                    "img": None,
                    "sort": 0,
                    "description": "增加20点生命值(4)",
                    "price": 100,
                    "execute": [ExeAttribute("hp", 20)],
                    "premise": [19]
                },
                {
                    "number": 21,
                    "img": None,
                    "sort": 0,
                    "description": "增加20点生命值(5)",
                    "price": 100,
                    "execute": [ExeAttribute("hp", 20)],
                    "premise": [20]
                },
                {
                    "number": 22,
                    "img": None,
                    "sort": 0,
                    "description": "增加20点生命值(6)",
                    "price": 100,
                    "execute": [ExeAttribute("hp", 20)],
                    "premise": [21]
                },
                {
                    "number": 23,
                    "img": None,
                    "sort": 0,
                    "description": "增加20点生命值(7)",
                    "price": 100,
                    "execute": [ExeAttribute("hp", 20)],
                    "premise": [22]
                },
                {
                    "number": 24,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点防御力(3)",
                    "price": 300,
                    "execute": [ExeAttribute("def", 10)],
                    "premise": [7]
                },
                {
                    "number": 25,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点防御力(4)",
                    "price": 300,
                    "execute": [ExeAttribute("def", 10)],
                    "premise": [24]
                },
                {
                    "number": 26,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点防御力(5)",
                    "price": 300,
                    "execute": [ExeAttribute("def", 10)],
                    "premise": [25]
                },
                {
                    "number": 27,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点防御力(6)",
                    "price": 300,
                    "execute": [ExeAttribute("def", 10)],
                    "premise": [26]
                },
                {
                    "number": 28,
                    "img": None,
                    "sort": 0,
                    "description": "增加10点防御力(7)",
                    "price": 300,
                    "execute": [ExeAttribute("def", 10)],
                    "premise": [27]
                },
                {
                    "number": 29,
                    "img": None,
                    "sort": 0,
                    "description": "增加20%金币获取率(3)",
                    "price": 500,
                    "execute": [ExeAttribute("gold", 20)],
                    "premise": [8]
                },
                {
                    "number": 30,
                    "img": None,
                    "sort": 0,
                    "description": "增加20%金币获取率(4)",
                    "price": 500,
                    "execute": [ExeAttribute("gold", 20)],
                    "premise": [29]
                }
            ]
        }
    }


class EnemyDetail:
    map = {
        "Marisa": {
            "surface": r".\assets\figure\2.png",
            "area": 0,
            "x": 27,
            "y": 8,
            "text": [
                "你好啊过路人",
                "可恶，你的碰撞体积怎么正好是一个方格啊喂！挡着路了啊喂！",
                "那就来打一架吧 D A Z E ！",
                "是我..输了..",
                "新手关都能输啊？菜，就多练",
                "哈哈哈哈太简单了哈哈哈哈"
            ],
            "options": [
                ["奇怪的人出现了", "是战斗的气息"],
                ["下一页"],
                ["进入战斗", "好好教训她", "逃跑"],
                ["嘲讽"],
                ["落荒而逃"],
                ["继续前进"]
            ],
            "execute": [
                [[ExePage(1)], [ExePage(1)]],
                [[ExePage(2)]],
                [[ExeBattle(3, 4)], [ExeBattle(3, 4)], [ExeClose()]],
                [[ExePage(5)]],
                [[ExeRefresh(), ExeClose()]],
                [[ExeMoney(100, useRate=True), ExeProcess("enemy", "Marisa"), ExeSave(
                ), ExeRefresh(), ExeClose()]]   # winMoney = 100 魔理沙最不值钱了~
            ],
            "img": [
                r".\assets\figure\002_03.png",
                r".\assets\player\talk\1.png",
                r".\assets\figure\002_08.png",
                r".\assets\figure\002_02.png",
                r".\assets\figure\002_05.png",
                r".\assets\player\talk\3.png"
            ],
            "scale": [
                (353, 550),
                (350, 550),
                (353, 550),
                (353, 550),
                (353, 550),
                (350, 550),
            ],
            "imgxy": [
                (90, 70),
                (95, 70),
                (90, 70),
                (90, 70),
                (90, 70),
                (95, 70)
            ],
            "cakeSurface": [
                "Marisa's cat_trash"
            ],
            "cakeSkill": [
                (None, None)
            ],
            "background": r".\assets\map\Marisa_background.png"
        },
        "Sanae": {
            "surface": r".\assets\figure\85.png",
            "area": 0,
            "x": 11,
            "y": 21,
            "text": [
                "站住，不许走！",
                "可恶的薄利商店抢占了我寿石商店的所有客源，破产后我只能在这里打劫了QAQ",
                "接招吧，「八坂之神风」！",
                "呜呜我就这么点钱都给你了，你能不能把薄利商店老板也欧拉一顿啊",
                "新手关都能输啊",
                "┭┮﹏┭┮ 没钱辣没钱辣真的没钱辣"
            ],
            "options": [
                ["早苗真好看", "我信仰神奈子", "都是些什么选项啊"],
                ["什么奇怪的剧情"],
                ["你的猫能发弹幕吗", "好好教训她", "溜了溜了"],
                ["？", "再多给一点钱"],
                ["落荒而逃"],
                ["不管她继续前进"]
            ],
            "execute": [
                [[ExePage(1)], [ExePage(1)], [ExePage(1)]],
                [[ExePage(2)]],
                [[ExeBattle(3, 4)], [ExeBattle(3, 4)], [ExeClose()]],
                [[ExePage(5)], [ExePage(5)]],
                [[ExeRefresh(), ExeClose()]],
                [[ExeMoney(150, useRate=True), ExeProcess(
                    "enemy", "Sanae"), ExeSave(), ExeRefresh(), ExeClose()]]
            ],
            "img": [
                r".\assets\figure\085_06.png",
                r".\assets\figure\085_05.png",
                r".\assets\figure\085_07.png",
                r".\assets\figure\085_02.png",
                r".\assets\figure\085_01.png",
                r".\assets\figure\085_02.png"
            ],
            "scale": [
                (463, 550),
                (463, 550),
                (463, 550),
                (463, 550),
                (463, 550),
                (463, 550)
            ],
            "imgxy": [
                (-10, 70),
                (-10, 70),
                (-10, 70),
                (-10, 70),
                (-10, 70),
                (-10, 70)
            ],
            "cakeSurface": [
                "Sanae's cat_trash",
                "Sanae's cat_ice",
                "Sanae's cat_mochi"
            ],
            "cakeSkill": [
                ("skill_red", None),
                ("skill_yellow", None),
                (None, None)
            ],
            "background": r".\assets\map\Sanae_background.png"
        },
        "Cirno": {
            "surface": r".\assets\figure\39.png",
            "area": 1,
            "x": 10,
            "y": 47,
            "text": [
                "喂，那边的，湖水怎么都结冰了，是不是你干的？",
                "薄利老板说是某个冰妖精做的，可是我绕着湖找了好久好久连一个人影都看不见。现在我终于见着人了，你说，你是不是冰妖精！",
                "什么？这么嚣张，那你一定是坏蛋冰妖精没错了！接招！",
                "你一直在那里说些什么怪话，这么笨蛋一定是冰妖精没错了！接招！",
                "呜呜呜打不过。。。",
                "嘿嘿，绮卤糯大胜利！",
                "？"
            ],
            "options": [
                ["果然会有琪露诺啊", "不是我不是我", "是我又怎样"],
                ["果然是笨蛋呢", "给剧情点赞"],
                ["好好教训她", "看看其它选项", "逃跑"],
                ["好好教训她", "看看其它选项", "逃跑"],
                ["其实冰妖精就是你", "其实你就是冰妖精", "其实你是笨蛋"],
                ["练一练再来挑战她"],
                ["不管她继续前进"]
            ],
            "execute": [
                [[ExePage(1)], [ExePage(1)], [ExePage(1)]],
                [[ExePage(2)], [ExePage(3)]],
                [[ExeBattle(4, 5)], [ExePage(1)], [ExeClose()]],
                [[ExeBattle(4, 5)], [ExePage(1)], [ExeClose()]],
                [[ExePage(6)], [ExePage(6)], [ExePage(6)]],
                [[ExeRefresh(), ExeClose()]],
                [[ExeMoney(500, useRate=True), ExeProcess(
                    "enemy", "Cirno"), ExeSave(), ExeRefresh(), ExeClose()]]
            ],
            "img": [
                r".\assets\figure\039_01.png",
                r".\assets\figure\039_01.png",
                r".\assets\figure\039_01.png",
                r".\assets\figure\039_01.png",
                r".\assets\figure\039_02.png",
                r".\assets\figure\039_03.png",
                r".\assets\figure\039_04.png"
            ],
            "scale": [
                (354, 550),
                (354, 550),
                (354, 550),
                (354, 550),
                (354, 550),
                (354, 550),
                (354, 550)
            ],
            "imgxy": [
                (35, 70),
                (35, 70),
                (35, 70),
                (35, 70),
                (35, 70),
                (35, 70),
                (35, 70)
            ],
            "cakeSurface": [
                "Cirno's cat_mochi",
                "Cirno's cat_trash",
                "Cirno's cat_ice",
                "Cirno's cat_flower"
            ],
            "cakeSkill": [
                ("skill_ice", None),
                ("skill_pink", "skill_cyan"),
                ("skill_yellow", None),
                ("skill_red", None)
            ],
            "background": r".\assets\map\Cirno_background.png"
        },
        "Youmu": {
            "surface": r".\assets\figure\52.png",
            "area": 1,
            "x": 87,
            "y": 7,
            "text": [
                "写文本的太困了想睡觉就开摆了，于是他直接放出了他最喜欢的YOOO梦来和你战斗。",
                "好好好你赢了",
                "输了？再练练吧",
            ],
            "options": [
                ["心疼作者一秒"],
                ["OHHHHHHHHH"],
                ["OKKKKKKKKK"]
            ],
            "execute": [
                [[ExeBattle(1, 2)]],
                [[ExeMoney(500, useRate=True), ExeProcess(
                    "enemy", "Youmu"), ExeSave(), ExeRefresh(), ExeClose()]],
                [[ExeRefresh(), ExeClose()]]
            ],
            "img": [
                r".\assets\figure\052_00.png",
                r".\assets\figure\052_04.png",
                r".\assets\figure\052_00.png"
            ],
            "scale": [
                (528, 550),
                (528, 550),
                (528, 550)
            ],
            "imgxy": [
                (10, 70),
                (10, 70),
                (10, 70)
            ],
            "cakeSurface": [
                "Youmu's cat_mochi",
                "Youmu's cat_trash",
                "Youmu's cat_ice",
                "Youmu's cat_flower"
            ],
            "cakeSkill": [
                ("skill_ice", None),
                ("skill_pink", "skill_cyan"),
                ("skill_yellow", None),
                ("skill_red", None)
            ],
            "background": r".\assets\map\Youmu_background.png"
        }
    }


class BoardDetail:
    map = {
        "guide1": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 0,
            "x": 42,
            "y": 45,
            "surface": r".\assets\map\board.png",
            "text": [
                "木牌上写了很多字，仔细看看吧",
                "“wasd或上下左右键都可以控制移动，按住shift加快移动速度...",
                "...按TAB键或B键打开菜单页，菜单界面按Esc关闭菜单...",
                "`键进入命令行，再次按`键关闭命令行，现在只告诉你一条命令exit用来退出游戏，其他的命令会在之后的指引中获得”"
            ],
            "options": [
                ["下一页", "关闭"],
                ["下一页", "上一页", "关闭"],
                ["下一页", "上一页", "关闭"],
                ["上一页", "关闭"]
            ],
            "execute": [
                [[ExePage(1)], [ExeClose()]],
                [[ExePage(2)], [ExePage(0)], [ExeClose()]],
                [[ExePage(3)], [ExePage(1)], [ExeClose()]],
                [[ExePage(2)], [ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550),
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70),
                (95, 70),
                (95, 70)
            ],
            "hint": "查看指引的木牌"
        },
        "guide2": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 0,
            "x": 56,
            "y": 38,
            "surface": r".\assets\map\board.png",
            "text": [
                "你已经发现了一个传送点，现在试试在命令行中输入“tp beginning”"
            ],
            "options": [
                ["关闭"],
            ],
            "execute": [
                [[ExeClose()]],
            ],
            "img": [
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550)
            ],
            "imgxy": [
                (95, 70)
            ],
            "hint": "查看指引的木牌"
        },
        "guide3": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 0,
            "x": 24,
            "y": 8,
            "surface": r".\assets\map\board.png",
            "text": [
                "恭喜你战胜了第一个敌人！",
                "每次战胜敌人都可以获得一定金币，获得的金币数量取决于敌人的难度和自身的金币获取率",
                "注意：任何传送命令都会让敌人重新出现（似乎可以刷金币呢）"
            ],
            "options": [
                ["下一页"],
                ["下一页"],
                ["关闭"]
            ],
            "execute": [
                [[ExePage(1)]],
                [[ExePage(2)]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70),
                (95, 70)
            ],
            "hint": "查看指引的木牌"
        },
        "guide4": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 0,
            "x": 11,
            "y": 16,
            "surface": r".\assets\map\board.png",
            "text": [
                "你已经拥有一张技能卡了，按TAB键打开猫糕页，为垃圾糕装上技能卡吧！"
            ],
            "options": [
                ["关闭"]
            ],
            "execute": [
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550)
            ],
            "imgxy": [
                (95, 70)
            ],
            "hint": "查看指引的木牌"
        },
        "guide666": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 2,
            "x": 7,
            "y": 7,
            "surface": r".\assets\map\board.png",
            "text": [
                "这张地图精心设计，但是没精力设置任何敌人和奖励了",
                "还请尽可能逛逛这张地图，因为这张地图的复杂性能充分展现我们地图编辑器的实用性"
            ],
            "options": [
                ["下一页"],
                ["关闭"]
            ],
            "execute": [
                [[ExePage(1)]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "查看偷懒的告示"
        },
        "si100b": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 0,
            "x": 79,
            "y": 26,
            "surface": r".\assets\map\board.png",
            "text": [
                "SI100B"
            ],
            "options": [
                ["关闭"],
            ],
            "execute": [
                [[ExeClose()]],
            ],
            "img": [
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550)
            ],
            "imgxy": [
                (95, 70)
            ],
            "hint": "查看彩蛋"
        },
        "guide6": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 1,
            "x": 85,
            "y": 30,
            "surface": r".\assets\map\board.png",
            "text": [
                "乆乆乆",
            ],
            "options": [
                ["一定是***干的"]
            ],
            "execute": [
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550)
            ],
            "imgxy": [
                (95, 70)
            ],
            "hint": "看看彩蛋是什么"
        },
        "guide5": {
            "type": "Dialogue",
            "sur_scale": (30, 30),
            "area": 1,
            "x": 4,
            "y": 22,
            "surface": r".\assets\map\board.png",
            "text": [
                "试试map命令，例如“map 0”能回到初始之地，“map 1”能回到这里",
            ],
            "options": [
                ["关闭"]
            ],
            "execute": [
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550)
            ],
            "imgxy": [
                (95, 70)
            ],
            "hint": "查看指引的木牌"
        },
        "newbie_gift_gold": {
            "type": "Treasure",
            "sur_scale": (20, 20),
            "area": 0,
            "x": 42,
            "y": 43,
            "surface": r".\assets\map\treasure.png",
            "text": [
                "听说触摸石像会有好运？",
                "突然出现了很多金币！",
                "确实是好运石像！"
            ],
            "startPage": 2,
            "options": [
                ["触摸石像"],
                ["收入囊中"],
                ["高兴离开"]
            ],
            "execute": [
                [[ExeMoney(100), ExePage(1)]],
                [[ExeProcess("treasure", "newbie_gift_gold"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\3.png",
                r".\assets\player\talk\3.png"
            ],
            "scale": [
                (350, 550),
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70),
                (95, 70)
            ],
            "hint": "摸摸可爱的石像"
        },
        "so_many_gold": {
            "type": "Treasure",
            "sur_scale": (20, 20),
            "area": 1,
            "x": 63,
            "y": 7,
            "surface": r".\assets\map\treasure.png",
            "text": [
                "石像爆金币了！你获得了1000金币！",
                "还想要更多金币？直接使用作弊命令cheat+数字就可以获得任意数量金币！"
            ],
            "startPage": 1,
            "options": [
                ["好欸"],
                ["真方便呢"],
            ],
            "execute": [
                [[ExeMoney(1000), ExeProcess(
                    "treasure", "so_many_gold"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\3.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "摸摸可爱的石像"
        },
        "beginning": {
            "type": "Anchor",
            "sur_scale": (30, 30),
            "area": 0,
            "x": 50,
            "y": 41,
            "surface": r".\assets\map\anchor.png",
            "text": [
                "按照惯例这应该是一个传送点，我应该怎么做？",
                "一段信息自动地进入了你的头脑：“你不需要这么做，这不是某个日本游戏”",
                "“记住我的编号：beginning”",
                "传送点beginning，一个美好的开始"
            ],
            "startPage": 3,
            "options": [
                ["与石像对坐", "点燃篝火", "触碰石像"],
                ["。。。"],
                ["记住了"],
                ["离开"]
            ],
            "execute": [
                [[ExePage(1)], [ExePage(1)], [ExePage(1)]],
                [[ExePage(2)]],
                [[ExeProcess("anchor", "beginning"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\3.png"
            ],
            "scale": [
                (350, 550),
                (350, 550),
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70),
                (95, 70),
                (95, 70)
            ],
            "hint": "靠近和善的石像"
        },
        "halfway": {
            "type": "Anchor",
            "sur_scale": (30, 30),
            "area": 0,
            "x": 21,
            "y": 8,
            "surface": r".\assets\map\anchor.png",
            "text": [
                "“这里是是传送点halfway，这里正好是这张地图路程的一半，可以方便你直接跳转”",
                "传送点halfway"
            ],
            "startPage": 1,
            "options": [
                ["好"],
                ["离开"]
            ],
            "execute": [
                [[ExeProcess("anchor", "halfway"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "走近转角处的石像"
        },
        "meadow": {
            "type": "Anchor",
            "sur_scale": (30, 30),
            "area": 1,
            "x": 52,
            "y": 4,
            "surface": r".\assets\map\anchor.png",
            "text": [
                "这里是是传送点meadow，这里虽然没几个草，但还是得叫这个名字",
                "传送点meadow"
            ],
            "startPage": 1,
            "options": [
                ["。。。"],
                ["离开"]
            ],
            "execute": [
                [[ExeProcess("anchor", "meadow"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "走近草地上的石像"
        },
        "lake": {
            "type": "Anchor",
            "sur_scale": (30, 30),
            "area": 1,
            "x": 16,
            "y": 45,
            "surface": r".\assets\map\anchor.png",
            "text": [
                "这里是是传送点lake，要是有水贴图就好了QAQ",
                "传送点lake"
            ],
            "startPage": 1,
            "options": [
                ["好的捏"],
                ["离开"]
            ],
            "execute": [
                [[ExeProcess("anchor", "lake"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "走近湖畔的石像"
        },
        "pinktree": {
            "type": "Anchor",
            "sur_scale": (30, 30),
            "area": 1,
            "x": 47,
            "y": 26.5,
            "surface": r".\assets\map\anchor.png",
            "text": [
                "这里是是传送点pinktree，顾名思义旁边是棵粉红色的树（",
                "传送点pinktree"
            ],
            "startPage": 1,
            "options": [
                ["有点敷衍啊"],
                ["离开"]
            ],
            "execute": [
                [[ExeProcess("anchor", "pinktree"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "走近树旁的石像"
        },
        "fork": {
            "type": "Anchor",
            "sur_scale": (30, 30),
            "area": 1,
            "x": 78,
            "y": 12,
            "surface": r".\assets\map\anchor.png",
            "text": [
                "这里是是传送点fork，是分岔路口的意思",
                "传送点fork"
            ],
            "startPage": 1,
            "options": [
                ["好的捏"],
                ["离开"]
            ],
            "execute": [
                [[ExeProcess("anchor", "fork"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "走近路口的石像"
        },
        "newbie_first_cat": {
            "type": "Treasure",
            "sur_scale": (20, 20),
            "area": 0,
            "x": 38,
            "y": 12,
            "surface": r".\assets\map\treasure.png",
            "text": [
                "雕像后头好像有什么东西",
                "喵喵？",
                "这是。。垃圾糕！",
                "喵！",
                "总之一起出发吧！",
                "O(∩_∩)O",
                "与垃圾糕的相遇之地"
            ],
            "startPage": 6,
            "options": [
                ["小心查看"],
                ["是猫猫", "是糕点", "是垃圾桶！"],
                ["垃圾糕~"],
                ["喵喵喵？"],
                ["带上垃圾糕"],
                ["离开这里"],
                ["离开"]
            ],
            "execute": [
                [[ExePage(1)]],
                [[ExePage(2)], [ExePage(2)], [ExePage(2)]],
                [[ExePage(3)]],
                [[ExePage(4)]],
                [[ExePage(5)]],
                [[ExeProcess("treasure", "newbie_first_cat"),
                  ExeProcess("cat", "cat_trash"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\catcake\preview\cake_01.png",
                r".\assets\player\talk\4.png",
                r".\assets\catcake\preview\cake_01.png",
                r".\assets\player\talk\0.png",
                r".\assets\catcake\preview\cake_01.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (213, 238),
                (350, 550),
                (213, 238),
                (350, 550),
                (213, 238),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (140, 210),
                (95, 70),
                (140, 210),
                (95, 70),
                (140, 210),
                (95, 70)
            ],
            "hint": "摸摸雕像"
        },
        "newbie_first_skill": {
            "type": "Treasure",
            "sur_scale": (20, 20),
            "area": 0,
            "x": 16,
            "y": 16,
            "surface": r".\assets\map\treasure.png",
            "text": [
                "突然间，你感到一股莫名的冲动，仿佛你正在玩一款抽卡游戏",
                "哇~金色传说",
                "技能卡：猫糕携带这张技能卡将获得群攻技能",
                "不拿白不拿，反正免费拿",
                "你在这里获得了第一张技能卡"
            ],
            "startPage": 4,
            "options": [
                ["发生什么了？！"],
                ["这是红色！", "这也叫传说？", "查看卡面"],
                ["好欸", "画风有点奇怪捏", "是掉帧的气息"],
                ["高兴收下"],
                ["离开"]
            ],
            "execute": [
                [[ExePage(1)]],
                [[ExePage(2)], [ExePage(2)], [ExePage(2)]],
                [[ExePage(3)], [ExePage(3)], [ExePage(3)]],
                [[ExeProcess("treasure", "newbie_first_skill"),
                  ExeProcess("skill", "skill_red"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\5.png",
                r".\assets\skill\red.png",
                r".\assets\skill\red.png",
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (259, 456),
                (259, 456),
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (130, 130),
                (130, 130),
                (95, 70),
                (95, 70)
            ],
            "hint": "摸摸吉祥物"
        },
        "newbie_second_cat": {
            "type": "Treasure",
            "sur_scale": (20, 20),
            "area": 0,
            "x": 17,
            "y": 26,
            "surface": r".\assets\map\treasure.png",
            "text": [
                "我有种预感，在这里可以领取到第二只猫糕",
                "喵喵？",
                "我超。。冰。。糕！",
                "喵！",
                "O(∩_∩)O",
                "与冰糕的相遇之地"
            ],
            "startPage": 5,
            "options": [
                ["吼吼吼吼"],
                ["是猫猫", "是冰糕", "是冰糕喵"],
                ["是少女猫喵"],
                ["她真好看"],
                ["带上冰糕"],
                ["离开"]
            ],
            "execute": [
                [[ExePage(1)]],
                [[ExePage(2)], [ExePage(2)], [ExePage(2)]],
                [[ExePage(3)]],
                [[ExePage(4)]],
                [[ExeProcess("treasure", "newbie_second_cat"),
                  ExeProcess("cat", "cat_ice"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\1.png",
                r".\assets\catcake\preview\cake_02.png",
                r".\assets\player\talk\4.png",
                r".\assets\catcake\preview\cake_02.png",
                r".\assets\catcake\preview\cake_02.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (213, 238),
                (350, 550),
                (213, 238),
                (213, 238),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (140, 210),
                (95, 70),
                (140, 210),
                (140, 210),
                (95, 70)
            ],
            "hint": "摸摸雕像"
        },
        "lake_skill_ice": {
            "type": "Treasure",
            "sur_scale": (20, 20),
            "area": 1,
            "x": 2,
            "y": 40,
            "surface": r".\assets\map\treasure.png",
            "text": [
                "恭喜你获得了技能卡：以糕为剑",
                "使用此技能，自爆，并对敌方所有目标当前血量变化值80%的伤害",
                "奖励只能拿一次哦"
            ],
            "startPage": 2,
            "options": [
                ["好的"],
                ["高兴收下"],
                ["离开"]
            ],
            "execute": [
                [[ExePage(1)]],
                [[ExeProcess("treasure", "lake_skill_ice"),
                  ExeProcess("skill", "skill_ice"), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png",
                r".\assets\skill\ice.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (259, 456),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (130, 130),
                (95, 70)
            ],
            "hint": "摸摸雕像"
        },
        "fork_attribute_big_treasure": {
            "type": "Treasure",
            "sur_scale": (20, 20),
            "area": 1,
            "x": 84,
            "y": 7,
            "surface": r".\assets\map\treasure.png",
            "text": [
                "你获得了属性大礼包！所有角色基础属性都将增加20点！",
                "奖励只能拿一次哦"
            ],
            "startPage": 1,
            "options": [
                ["太棒了！"],
                ["离开"]
            ],
            "execute": [
                [[ExeProcess("treasure", "fork_attribute_big_treasure"),
                  ExeAttribute("hp", 20), ExeAttribute("atk", 20), ExeAttribute("def", 20), ExeAttribute("gold", 20), ExeClose()]],
                [[ExeClose()]]
            ],
            "img": [
                r".\assets\player\talk\0.png",
                r".\assets\player\talk\0.png"
            ],
            "scale": [
                (350, 550),
                (350, 550)
            ],
            "imgxy": [
                (95, 70),
                (95, 70)
            ],
            "hint": "摸摸雕像"
        }
    }
