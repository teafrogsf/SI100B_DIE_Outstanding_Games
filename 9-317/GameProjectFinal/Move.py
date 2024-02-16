import pygame
from Settings import *


# moves are diveded into Physical moves and Special moves
# power of Physical move depends on Atk of attacker and Def of defender
# power of Special move depends on SpA of attacker and SpD of defender

class Move():
    def __init__(self, category, type):
        self.category = category
        self.type = type
        self.name = None

class PhysicalMove(Move):
    def __init__(self, name, type, accuracy, power):
        super().__init__(MoveCategory.PHYSICAL, type)
        self.name = name
        self.accuracy = accuracy
        self.power = power
    def get_info(self):
        return [self.name, "Physical", f"pow : {self.power}", f"acc : {self.accuracy}"]

class SpecialMove(Move):
    def __init__(self, name, type, accuracy, power):
        super().__init__(MoveCategory.SPECIAL, type)
        self.name = name
        self.accuracy = accuracy
        self.power = power
    def get_info(self):
        return [self.name, "Special", f"pow : {self.power}", f"acc : {self.accuracy}"]

# moves
Tackle = PhysicalMove("Tackle", Types.NORMAL, 95, 35)
VineWhip = PhysicalMove("Vine Whip", Types.GRASS, 100, 35)
RazorLeaf = PhysicalMove("Razor Leaf", Types.GRASS, 95, 55)
SolarBeam = SpecialMove("Solar Beam", Types.GRASS, 100, 120)
Scratch = PhysicalMove("Scratch", Types.NORMAL, 100, 40)
Ember = SpecialMove("Ember", Types.FIRE, 100, 40)
MetalClaw = PhysicalMove("Metal Claw", Types.STEEL, 95, 50)
Flamethrower = SpecialMove("Flamethrower", Types.FIRE, 100, 90)
WaterGun = SpecialMove("Water Gun", Types.WATER, 100, 40)
Bite = PhysicalMove("Bite", Types.DARK, 100, 60)
HydroPump = SpecialMove("Hydro Pump", Types.WATER, 80, 120)
TakeDown = PhysicalMove("Take Down", Types.NORMAL, 85, 90)
Gust = SpecialMove("Gust", Types.FLYING, 100, 40)
WingAttack = PhysicalMove("Wing Attack", Types.FLYING, 100, 60)
ShadowPunch = PhysicalMove("Shadow Punch", Types.GHOST, 100, 60)
ShadowBall = SpecialMove("Shadow Ball", Types.GHOST, 100, 80)
SludgeBomb = SpecialMove("Sludge Bomb", Types.POISON, 100, 90)
Thunderbolt = SpecialMove("Thunderbolt", Types.ELECTRIC, 100, 95)
Pursuit = PhysicalMove("Pursuit", Types.FIGHTING, 100, 40)
Earthquake = PhysicalMove("Earthquake", Types.GROUND, 100, 100)
AirSlash = SpecialMove("Air Slash", Types.FLYING, 95, 75)
Psychic = SpecialMove("Psychic", Types.PSYCHIC, 100, 90)
DazzlingGleam = SpecialMove("Dazzling Gleam", Types.FAIRY, 100, 80)
Psyshock = SpecialMove("Psyshock", Types.PSYCHIC, 100, 80)
Confusion = SpecialMove("Confusion", Types.PSYCHIC, 100, 50)
ZenHeadbutt = PhysicalMove(" Zen Headbutt", Types.PSYCHIC, 90, 80)
HammerArm = PhysicalMove("Hammer Arm", Types.FIGHTING, 100, 90)
MeteorMash = PhysicalMove("Meteor Mash", Types.STEEL, 90, 90)
EarthPower = SpecialMove("Earth Power", Types.GROUND, 100, 90)
LowSweep = PhysicalMove("Low Sweep", Types.FIGHTING, 100, 65)
BrickBreak = PhysicalMove("Brick Break", Types.FIGHTING, 100, 75)
AerialAce = PhysicalMove("Aerial Ace", Types.FLYING, 100, 60)
FlameCharge = PhysicalMove("Flame Charge", Types.FIRE, 100, 50)
Thunder = SpecialMove("Thunder", Types.ELECTRIC, 70, 120)
DrillPeck = PhysicalMove("Drill Peck", Types.FIGHTING, 100, 80)
AuraSphere = SpecialMove("Aura Sphere", Types.FIGHTING, 100, 80)
AncientPower = SpecialMove("Ancient Power", Types.ROCK, 100, 60)
DragonClaw = PhysicalMove("Dragon Claw", Types.DRAGON, 100, 80)
Fly = PhysicalMove("Fly", Types.FLYING, 100, 90)
IronTail = PhysicalMove("Iron Tail", Types.STEEL, 75, 100)
Discharge = SpecialMove("Discharge", Types.ELECTRIC, 100, 80)