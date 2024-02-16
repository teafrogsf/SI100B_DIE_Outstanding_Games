import pygame
from math import floor
from random import randint
from Settings import *

from Move import *


# every Pokemon has its own Species Strength
# every individual Pokemon has its Nature and Individual Valuse
# through special fomula to calculate the status of one particular Pokemon

class Pokemon():
    def __init__(self, level,  speciesStrength, frontPath, backPath):
        self.frontImage = pygame.image.load(frontPath)
        self.frontImage = pygame.transform.scale(self.frontImage, (PokemonSettings.width, PokemonSettings.height))
        self.backImage = pygame.image.load(backPath)
        self.backImage = pygame.transform.scale(self.backImage, (PokemonSettings.width, PokemonSettings.height))

        self.speciesStrength = speciesStrength # HP, Atk, Def, SpA, SpD, Spd
        self.individualValues = self.gen_IV()
        self.nature = self.gen_nature()
        self.level = level
        self.exp = 0
        self.stat = self.stat_calculator(self.speciesStrength, self.individualValues, self.level, self.nature)
        self.HP = self.stat[0]

        self.name = None
        self.type1 = None
        self.type2 = None
        self.moves = [None, None, None, None]
        self.movesNum = 0

    def add_move(self, move:Move):
        if self.movesNum < 4:
            self.moves[self.movesNum] = move
            self.movesNum += 1

    def expUp(self, exp):
        self.exp += exp
        while self.exp >= expList[self.level] and self.level < 100:
            self.exp -= expList[self.level]
            self.level += 1
        self.stat = self.stat_calculator(self.speciesStrength, self.individualValues, self.level, self.nature)
        self.HP = self.stat[StatID.HP]

    def get_info(self):
        if self.type2 is not None:
            Type = typeList[self.type1] + "+" + typeList[self.type2]
        else:
            Type = typeList[self.type1]
        return [self.name, Type, self.nature,
                f"Level : {self.level}", f"exp : {self.exp}/{expList[self.level]}",
                f"HP  : {self.stat[0]}", f"Atk : {self.stat[1]}", f"Def : {self.stat[2]}",
                f"SpA : {self.stat[3]}", f"SpD : {self.stat[4]}", f"Spd : {self.stat[5]}"]
    def get_battle_info(self):
        return [self.stat]

    def gen_IV(self):       # random generating
        return (randint(0, 31), randint(0, 31), randint(0, 31), randint(0, 31), randint(0, 31), randint(0, 31))
    def gen_nature(self):   # random generating
        return natureList[randint(0, 24)]
    def stat_calculator(self, speciesStrength:tuple[int, int, int, int, int, int],
                             individualValues:tuple[int, int, int, int, int, int],
                             level:int, nature:str):
        HP = ((speciesStrength[StatID.HP] * 2 + individualValues[StatID.HP]) * level // 100) + 10 + level
        Atk = floor((((speciesStrength[StatID.Atk] * 2 + individualValues[StatID.Atk]) * level // 100) + 5) * (1 + natureTable[nature][0]))
        Def = floor((((speciesStrength[StatID.Def] * 2 + individualValues[StatID.Def]) * level // 100) + 5) * (1 + natureTable[nature][1]))
        SpA = floor((((speciesStrength[StatID.SpA] * 2 + individualValues[StatID.SpA]) * level // 100) + 5) * (1 + natureTable[nature][2]))
        SpD = floor((((speciesStrength[StatID.SpD] * 2 + individualValues[StatID.SpD]) * level // 100) + 5) * (1 + natureTable[nature][3]))
        Spd = floor((((speciesStrength[StatID.Spd] * 2 + individualValues[StatID.Spd]) * level // 100) + 5) * (1 + natureTable[nature][4]))
        return (HP, Atk, Def, SpA, SpD, Spd)

# Pokemons
class Bulbasaur(Pokemon):
    def __init__(self, level):
        super().__init__(level, (45, 49, 49, 65, 65, 45), GamePath.pokemonFront[0], GamePath.pokemonBack[0])
        self.name = "Bulbasaur"
        self.type1 = Types.GRASS
        self.type2 = None
        self.add_move(Tackle)
        self.add_move(VineWhip)
        self.add_move(RazorLeaf)
        self.add_move(SolarBeam)

class Charmander(Pokemon):
    def __init__(self, level):
        super().__init__(level, (39, 52, 43, 60, 50, 65), GamePath.pokemonFront[1], GamePath.pokemonBack[1])
        self.name = "Charmander"
        self.type1 = Types.FIRE
        self.type2 = None
        self.add_move(Scratch)
        self.add_move(Ember)
        self.add_move(MetalClaw)
        self.add_move(Flamethrower)

class Squirtle(Pokemon):
    def __init__(self, level):
        super().__init__(level, (44, 48, 65, 50, 64, 43), GamePath.pokemonFront[2], GamePath.pokemonBack[2])
        self.name = "Squirtle"
        self.type1 = Types.WATER
        self.type2 = None
        self.add_move(Tackle)
        self.add_move(WaterGun)
        self.add_move(Bite)

class Poochyena(Pokemon):
    def __init__(self, level):
        super().__init__(level, (35, 55, 35, 30, 30, 35), GamePath.pokemonFront[3], GamePath.pokemonBack[3])
        self.name = "Poochyena"
        self.type1 = Types.DARK
        self.type2 = None
        self.add_move(Tackle)
        self.add_move(Bite)

class Pidgey(Pokemon):
    def __init__(self, level):
        super().__init__(level, (40, 45, 40, 35, 35, 56), GamePath.pokemonFront[4], GamePath.pokemonBack[4])
        self.name = "Pidgey"
        self.type1 = Types.NORMAL
        self.type2 = Types.FLYING
        self.add_move(Tackle)
        self.add_move(Gust)

class Gengar(Pokemon):
    def __init__(self, level):
        super().__init__(level, (60, 65, 60, 130, 75, 110), GamePath.pokemonFront[5], GamePath.pokemonBack[5])
        self.name = "Gengar"
        self.type1 = Types.GHOST
        self.type2 = Types.POISON
        self.add_move(ShadowPunch)
        self.add_move(ShadowBall)
        self.add_move(SludgeBomb)
        self.add_move(Thunderbolt)

class Dusclops(Pokemon):
    def __init__(self, level):
        super().__init__(level, (40, 70, 130, 60, 130, 25), GamePath.pokemonFront[6], GamePath.pokemonBack[6])
        self.name = "Dusclops"
        self.type1 = Types.GHOST
        self.type2 = None
        self.add_move(ShadowPunch)
        self.add_move(Pursuit)
        self.add_move(Earthquake)

class Xatu(Pokemon):
    def __init__(self, level):
        super().__init__(level, (60, 75, 70, 95, 70, 95), GamePath.pokemonFront[7], GamePath.pokemonBack[7])
        self.name = "Xatu"
        self.type1 = Types.PSYCHIC
        self.type2 = Types.FLYING
        self.add_move(WingAttack)
        self.add_move(AirSlash)
        self.add_move(Psychic)

class Gardevoir(Pokemon):
    def __init__(self, level):
        super().__init__(level, (68, 65, 65, 125, 115, 80), GamePath.pokemonFront[8], GamePath.pokemonBack[8])
        self.name = "Gardevoir"
        self.type1 = Types.PSYCHIC
        self.type2 = Types.FAIRY
        self.add_move(DazzlingGleam)
        self.add_move(Psychic)
        self.add_move(Psyshock)
        self.add_move(ShadowBall)

class Metang(Pokemon):
    def __init__(self, level):
        super().__init__(level, (60, 75, 100, 55, 80, 50), GamePath.pokemonFront[9], GamePath.pokemonBack[9])
        self.name = "Metang"
        self.type1 = Types.STEEL
        self.type2 = Types.PSYCHIC
        self.add_move(MetalClaw)
        self.add_move(Confusion)
        self.add_move(ZenHeadbutt)

class Metagross(Pokemon):
    def __init__(self, level):
        super().__init__(level, (80, 135, 130, 95, 90, 70), GamePath.pokemonFront[10], GamePath.pokemonBack[10])
        self.name = "Metagross"
        self.type1 = Types.STEEL
        self.type2 = Types.PSYCHIC
        self.add_move(MetalClaw)
        self.add_move(ZenHeadbutt)
        self.add_move(HammerArm)
        self.add_move(MeteorMash)

class Claydol(Pokemon):
    def __init__(self, level):
        super().__init__(level, (60, 70, 105, 70, 120, 75), GamePath.pokemonFront[11], GamePath.pokemonBack[11])
        self.name = "Claydol"
        self.type1 = Types.GROUND
        self.type2 = Types.PSYCHIC
        self.add_move(Confusion)
        self.add_move(Earthquake)
        self.add_move(EarthPower)

class Hariyama(Pokemon):
    def __init__(self, level):
        super().__init__(level, (144, 120, 60, 40, 60, 50), GamePath.pokemonFront[12], GamePath.pokemonBack[12])
        self.name = "Hariyama"
        self.type1 = Types.FIGHTING
        self.type2 = None
        self.add_move(Tackle)
        self.add_move(LowSweep)
        self.add_move(BrickBreak)

class Blaziken(Pokemon):
    def __init__(self, level):
        super().__init__(level, (80, 120, 70, 110, 70, 80), GamePath.pokemonFront[13], GamePath.pokemonBack[13])
        self.name = "Blaziken"
        self.type1 = Types.FIRE
        self.type2 = Types.FIGHTING
        self.add_move(BrickBreak)
        self.add_move(Flamethrower)
        self.add_move(AerialAce)
        self.add_move(FlameCharge)

class Zapdos(Pokemon):
    def __init__(self, level):
        super().__init__(level, (90, 90, 85, 125, 90, 100), GamePath.pokemonFront[14], GamePath.pokemonBack[14])
        self.name = "Zapdos"
        self.type1 = Types.ELECTRIC
        self.type2 = Types.FLYING
        self.add_move(Thunderbolt)
        self.add_move(Thunder)
        self.add_move(AerialAce)
        self.add_move(DrillPeck)

class Mewtwo(Pokemon):
    def __init__(self, level):
        super().__init__(level, (106, 110, 90, 154, 90, 130), GamePath.pokemonFront[15], GamePath.pokemonBack[15])
        self.name = "Mewtwo"
        self.type1 = Types.PSYCHIC
        self.type2 = None
        self.add_move(Psychic)
        self.add_move(Psyshock)
        self.add_move(AuraSphere)
        self.add_move(AncientPower)

class Salamence(Pokemon):
    def __init__(self, level):
        super().__init__(level, (90, 135, 80, 110, 80, 100), GamePath.pokemonFront[16], GamePath.pokemonBack[16])
        self.name = "Salamence"
        self.type1 = Types.DRAGON
        self.type2 = Types.FLYING
        self.add_move(DragonClaw)
        self.add_move(Fly)
        self.add_move(Bite)
        self.add_move(Flamethrower)

class Pikachu(Pokemon):
    def __init__(self, level):
        super().__init__(level, (35, 55, 40, 50, 50, 90), GamePath.pokemonFront[17], GamePath.pokemonBack[17])
        self.name = "Pikachu"
        self.type1 = Types.ELECTRIC
        self.type2 = None
        self.add_move(Thunderbolt)
        self.add_move(Thunder)
        self.add_move(IronTail)
        self.add_move(Discharge)


# Pokemons in tall grass
wildPokemons = [Poochyena(13), Poochyena(14), Poochyena(16), Poochyena(17), Pidgey(13), Pidgey(14), Pidgey(15), Pidgey(17),
                Xatu(17), Xatu(18), Claydol(17), Claydol(18), Claydol(20), Metang(18), Metang(19), Metagross(20),
                Hariyama(18), Hariyama(19), Hariyama(20), Bulbasaur(20), Charmander(20), Squirtle(20),
                Pikachu(10), Gengar(20), Zapdos(30)]