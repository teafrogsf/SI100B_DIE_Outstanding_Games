import pygame
from GameManager import GameManager

def main():
    pygame.init() # pygame初始化
    manager = GameManager() # 初始化游戏管理器
    while True:
        if manager.needRestart == True:
            manager = GameManager()
        manager.update()
        manager.render()

if __name__ == "__main__":
    main()