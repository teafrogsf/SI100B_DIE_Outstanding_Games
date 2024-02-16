import pygame
from math import floor
from random import randint
from Pokemon import *
from Move import *
from Settings import *

class Battle():
    def __init__(self):
        self.timeCounter = 0

    def encounter_wildpoke(self):
        self.timeCounter += 1
        if self.timeCounter >= 30:
            self.timeCounter = 0
            if randint(0, 100) < BattleSettings.encounterProbability:
                return True
        return False

    def effect(self, defender:Pokemon, move:Move):  # check damage coefficient
        if defender.type2 is not None:
            return typeTable[move.type][defender.type1] * typeTable[move.type][defender.type2]
        return typeTable[move.type][defender.type1]
    def effect_description(self, effect):
        if effect > 1:
            return "It is Super Effective!"
        if effect == 1:
            return "It is Effective."
        if effect < 1 and effect != 0:
            return "It is Not very Effective..."
        if effect == 0:
            return "It is No Effective...."
        
    def attack(self, attacker:Pokemon, defender:Pokemon, move:Move):    # special fomula to calculate damage
        if isinstance(move, PhysicalMove):
            addition = (85 + randint(0, 15)) / 100 * self.effect(defender, move)
            if attacker.type1 == move.type or attacker.type2 == move.type:
                addition *= 1.5

            damege = floor(((attacker.level * 2 + 5) / 250) * (attacker.stat[StatID.Atk] / defender.stat[StatID.Def]) * move.power + 2)
            if damege <= 0:
                damege = 1
            return damege
        if isinstance(move, SpecialMove):
            addition = (85 + randint(0, 15)) / 100 * self.effect(defender, move)
            if attacker.type1 == move.type or attacker.type2 == move.type:
                addition *= 1.5
            
            damege = floor(((attacker.level * 2 + 5) / 250) * (attacker.stat[StatID.SpA] / defender.stat[StatID.SpD]) * move.power + 2)
            if damege <= 0:
                damege = 1
            return damege
        
    def attacker(self, frePokemon:Pokemon, enePokemon:Pokemon): # check speed
        if frePokemon.stat[StatID.Spd] > enePokemon.stat[StatID.Spd]:
            return 0
        elif frePokemon.stat[StatID.Spd] < enePokemon.stat[StatID.Spd]:
            return 1
        else:
            return randint(0, 1)
        