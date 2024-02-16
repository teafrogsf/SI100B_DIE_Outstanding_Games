from Settings import *
from UI import *
import pygame


class NPC:
    def __init__(self) -> None:
        self.isBattling = False
        self.isTalking = False
        self.cakeList = []  # 战斗队列，未满的话从仓库导入，满的话要实现交换
