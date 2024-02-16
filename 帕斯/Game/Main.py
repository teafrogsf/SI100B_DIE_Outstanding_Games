# -*- coding:utf-8 -*-
import sys
import pygame
from GameManager import GameManager
from Settings import *

def main():
    pygame.init()
    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption(WindowSettings.name)
    manager = GameManager(window)
 
    while True:
        manager.update()
        manager.render()
        pygame.display.flip()

if __name__ == "__main__":
    main()

# running
