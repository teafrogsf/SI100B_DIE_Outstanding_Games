from Settings import *
import pygame


class UI:
    def __init__(self, UItype) -> None:
        self.isLive = False
        self.UIStartX = UISettings.UIStartX
        self.UIStartY = UISettings.UIStartY


class Skill(UI):  # BattleField下的猫糕技能框
    def __init__(self) -> None:
        '''
        表示是否被选中
        '''
        self.isSelected = False


class DialogBox(UI):  # 出现在MainMap中的角色对话框
    def __init__(self, text, fontColor, fontSize) -> None:
        self.text = text
        self.fontColor = fontColor
        self.fontSize = fontSize
        self.textStartX = DialogSettings.textStartX
        self.textStartY = DialogSettings.textStartY
        '''
        icon表示的是对话框左侧且正在说话的人物缩略图
        '''
        self.icon = None
        self.iconStartX = DialogSettings.iconStartX
        self.iconStartY = DialogSettings.iconStartY


class SelectBox(UI):  # 战斗时指示攻击对象（敌人）的方框
    def __init__(self) -> None:
        pass


class Tip(UI):  # 没有方框，但是有不同颜色的提示
    def __init__(self, text, fontColor, fontSize) -> None:
        self.text = text
        self.fontColor = fontColor
        self.fontSize = fontSize
        self.textStartX = DialogSettings.textStartX
        self.textStartY = DialogSettings.textStartY
        '''
        表示是否会上升消失
        '''
        self.uplift = False


class Commit(UI):  # 确定按钮
    def __init__(self) -> None:
        pass


class Cancel(UI):  # 取消按钮
    def __init__(self) -> None:
        pass


class Indicator(UI):  # 出现在BattleField中，指向正在发动攻击的player的精灵
    def __init__(self) -> None:
        pass


class EnergyBar(UI):  # 能量条，包括：hp、pp、怪物进入战斗状态倒计时
    def __init__(self) -> None:
        pass


class HideBox(UI):  # 在PreviewMap中出现，遮盖未被探索的地图
    def __init__(self) -> None:
        '''
        表示当前区域管辖的锚点
        '''
        self.teleportList = []


class Teleport(UI):  # 在PreviewMap中出现，表示传送锚点
    def __init__(self) -> None:
        pass


class Pager(UI):  # 在Bag中出现，翻页器
    def __init__(self, pagerType) -> None:
        '''
        表示前一页或者后一页
        '''
        self.pagerType = pagerType
