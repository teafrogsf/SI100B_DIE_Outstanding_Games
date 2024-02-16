# -*- coding:utf-8 -*-

from Design import *

def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()

    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            merged_dict[key] = merge_dicts(merged_dict[key], value)
        else:
            merged_dict[key] = value

    return merged_dict

class Info:
    # 严格规定info目录结构为 2 层
    def __init__(self, info = {}) -> None:
        self.info = {
            "basic" : {
                "nickname" : "",
                "password" : "",
                "direction" : BirthInfo.direction[0],
                "x" : BirthInfo.point[0][0] * Settings.MapSettings.square,
                "y" : BirthInfo.point[0][1] * Settings.MapSettings.square,
                "area" : 0,
                # 人物状态 0: 正常行走, 1: 命令行, 2: 对话, 3: 遇敌, 4: 菜单, 5: 商店
                "state" : 0,
                "money" : 0,
                "atk" : 0,
                "def" : 0,
                "hp" : 0,
                "gold" : 100,
                "unit" : [None, None, None, None]
            },
            "progress" : {
                "anchor" : [],
                "treasure" : [],
                "cat" : [],
                "skill" : [],
                "map" : [0],
                "enemy": []
            },
            # 这个很特殊，我不知道会不会出问题
            "skillUse" : {
            },
            # 这个也很特殊，哎呦喂，真头疼
            "shoppingHistory": {

            }
        }
        self.info = merge_dicts(self.info, info)
    
    def get_info(self, entry):
        if entry in self.info:
            return self.info[entry]
        for catergory in self.info:
            if entry in self.info[catergory]:
                return self.info[catergory][entry]
        return Info().get_info(entry)
    
    def modify(self ,entry, content, ifExtend= False):
        if entry in self.info:
            if ifExtend:
                self.info[entry].append(content)
            else:
                self.info[entry] = content
            return 
        for catergory in self.info:
            if entry in self.info[catergory]:
                if ifExtend:
                    if content not in self.info[catergory][entry]:
                        self.info[catergory][entry].append(content)
                else:
                    self.info[catergory][entry] = content
                return 
        # test
        # print(content)