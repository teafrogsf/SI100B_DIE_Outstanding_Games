import pygame

import sys

a=pygame.font.get_fonts()
def run_game():
    pygame.init()
    window = pygame.display.set_mode((1300,620))


    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        window.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for x in range(6):
            for i in range(20*x,20*(x+1)):
                b=pygame.font.SysFont(a[i], 20)
                text = b.render(f"ATK Buff BUFF {i}",True,(20,0,0),(255,255,255))
                window.blit(text,(10+200*x,30*(i%20)))
        print(a[18])
        pygame.display.flip()

if __name__ == "__main__":
    run_game()
    
