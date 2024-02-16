import pygame
from game_manager import *

class game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.Game = Game(self)
        
    def run(self):
        while True:
            self.Game.run()
            
if __name__ == "__main__":
    GAME = game()
    GAME.run()