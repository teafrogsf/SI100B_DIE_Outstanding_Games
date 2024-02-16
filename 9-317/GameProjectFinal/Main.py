import pygame

from Player import Player
from GameManager import Gamemanager
from Pokemon import *
from Settings import *

def run():
    # game init
    pygame.init()
    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption("Pokemon ?")

    manager = Gamemanager(window)
    # initial Pokemons
    player = Player([Gardevoir(20), Pikachu(20)])
    while True:
        manager.tick(30)            # tick setting
        manager.event_queue(player) # process event queue
        keys = pygame.key.get_pressed()
        
        # render and update
        if manager.state == GameState.MAIN_MENU or manager.state == GameState.GAME_PLAY_ORIGIN:
            manager.render()
        elif manager.state == GameState.END_GAME:
            manager.render()
        else:
            player.update(keys, manager.scene)
            manager.update(player)
            manager.render()
            player.draw(window)
            manager.triggers(player, keys)
            manager.events(player, keys)

        pygame.display.flip()



if __name__ == "__main__":
    run()