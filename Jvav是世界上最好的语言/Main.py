import time
import pygame
import random
from GameManager import GameManager

def main():
    pygame.init()
    pygame.mixer.init()
    random.seed(int(time.time()))
    manager=GameManager()
    while True:
        manager.update()
        pygame.display.flip()

if __name__ == "__main__":
    main()