from NPC import NPC
import pygame
from Setting import EnemySettings, GamePath

class Enemy(NPC):
    def __init__(self, pos, image = None,  HP = 0, ATK = 0, DEF = 0) -> None:
        super().__init__(pos, image)
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.deadImage = pygame.image.load(GamePath.deadEnemy)
    def get_Info(self) -> list:
        return ['HP: '+str(self.HP)[:8], 'ATK: '+str(self.ATK)[:5], 'DEF: '+str(self.DEF)[:5]]

class Enemy_Student(Enemy):
    def __init__(self, pos ,image) -> None:
        super().__init__(pos, image)
        self.HP = EnemySettings.enemyStudentSetting['HP']
        self.ATK = EnemySettings.enemyStudentSetting['ATK']
        self.DEF = EnemySettings.enemyStudentSetting['DEF']

class Enemy_SIST(Enemy):
    def __init__(self, pos, image) -> None:
        super().__init__(pos, image)
        self.HP = EnemySettings.enemySISTSetting['HP']
        self.ATK = EnemySettings.enemySISTSetting['ATK']
        self.DEF = EnemySettings.enemySISTSetting['DEF']

class Enemy_SLST(Enemy):
    def __init__(self, pos, image) -> None:
        super().__init__(pos, image)
        self.HP = EnemySettings.enemySLSTSetting['HP']
        self.ATK = EnemySettings.enemySLSTSetting['ATK']
        self.DEF = EnemySettings.enemySLSTSetting['DEF']

class Enemy_SPST(Enemy):
    def __init__(self, pos, image) -> None:
        super().__init__(pos, image)
        self.HP = EnemySettings.enemySPSTSetting['HP']
        self.ATK = EnemySettings.enemySPSTSetting['ATK']
        self.DEF = EnemySettings.enemySPSTSetting['DEF']

class Boss(Enemy):
    def __init__(self, pos, image) -> None:
        super().__init__(pos, image)
        self.HP = EnemySettings.enemyBossSetting['HP']
        self.ATK = EnemySettings.enemyBossSetting['ATK']
        self.DEF = EnemySettings.enemyBossSetting['DEF']