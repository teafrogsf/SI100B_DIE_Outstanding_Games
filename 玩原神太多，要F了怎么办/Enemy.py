from Settings import *
from UI import *
import pygame


class Enemy:
    def __init__(self) -> None:
        self.isBattling = False
        self.cakeList = []  # 要导入
