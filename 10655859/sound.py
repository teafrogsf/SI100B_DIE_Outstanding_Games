import pygame

class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.sound_path = 'sound/'
        self.shotgun = pygame.mixer.Sound(self.sound_path + 'shotgun.wav')
        self.enemy_pain = pygame.mixer.Sound(self.sound_path + 'enemy_pain.wav')
        self.enemy_pain.set_volume(0.2)
        self.enemy_death = pygame.mixer.Sound(self.sound_path + 'enemy_death.wav')
        self.enemy_death.set_volume(0.2)
        self.enemy_attack = pygame.mixer.Sound(self.sound_path + 'enemy_attack.wav')
        self.enemy_attack.set_volume(0.2)
        self.player_pain = pygame.mixer.Sound(self.sound_path + 'player_pain.wav')
        self.bgm = pygame.mixer.Sound(self.sound_path + 'The Only Thing They Fear Is You(Remix)-SayMaxWel.flac')