from Settings import *
from UI import *
from Cake import *
from Source import *
import pygame


class Warehouse:
    def __init__(self) -> None:
        self.cakeList = []  # 根据玩家信息导入
        self.sourceList = []  # 根据玩家信息导入
