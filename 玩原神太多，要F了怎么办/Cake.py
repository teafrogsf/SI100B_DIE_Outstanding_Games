# -*- coding:utf-8 -*-

from Settings import *
from UI import *
import pygame


class Cake:
    def __init__(self) -> None:
        self.hp = 0
        self.pp = 0
        self.atk = 0
        self.dfc = 0
        self.flavor = None
        self.skillList = []  # 要导入
