



# -*- coding:utf-8 -*-
import pygame
from GameManager import GameManager

def main():
    pygame.init()
    manager = GameManager()
    clock = pygame.time.Clock()#暂时加到这里 不知道为什么gamereset里面的没用
    manager.game_reset()
    
    while True:
        clock.tick(25)#暂时加到这里
        manager.update()
        manager.render()
        pygame.display.flip()

if __name__ == "__main__":
    main()