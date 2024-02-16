import pygame
import Battle
from NPCs import *
from Pokemon import *
from typing import *
from Settings import *

# interface generators

class DialogBox():
    def __init__(self, window, npcPath:str, text:list,
                 fontSize:int=DialogSettings.textSize,
                 fontColor:Tuple[int, int, int]=(255, 255, 255),
                 bgColor:Tuple[int, int, int, int]=(0, 0, 0, DialogSettings.boxAlpha)):
        self.window = window
        self.text = text

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.bg = pygame.Surface((DialogSettings.boxWidth, DialogSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)

        self.npcImage = pygame.image.load(npcPath)
        self.npcImage = pygame.transform.scale(self.npcImage, (DialogSettings.npcWidth, DialogSettings.npcHeight))

    def render(self):
        self.window.blit(self.bg, (DialogSettings.boxStartX, DialogSettings.boxStartY))
        self.window.blit(self.npcImage, (DialogSettings.npcCoordX, DialogSettings.npcCoordY))

        offset = 0
        for text in self.text:
            self.window.blit(self.font.render(text, True, self.fontColor), (DialogSettings.textStartX, DialogSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist

class ShopingBox():
    def __init__(self, window, npcPath:str, player, items,
                 fontSize:int=DialogSettings.textSize,
                 fontColor:Tuple[int, int, int]=(255, 255, 255),
                 bgColor:Tuple[int, int, int, int]=(0, 0, 0, DialogSettings.boxAlpha)):
        self.window = window

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.bg = pygame.Surface((DialogSettings.boxWidth, DialogSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)

        self.npcImage = pygame.image.load(npcPath)
        self.npcImage = pygame.transform.scale(self.npcImage, (DialogSettings.npcWidth, DialogSettings.npcHeight))

        self.player = player
        self.items = items
        self.selectID = 0
        self.selectCD = 0
        self.pressCD = 0

    def buy(self):
        if self.player.money >= itemCost[self.selectID]:
            self.player.money -= itemCost[self.selectID]
            self.player.bag[self.selectID] += 1

    def render(self):
        self.window.blit(self.bg, (ShopSettings.boxStartX, ShopSettings.boxStartY))
        self.window.blit(self.npcImage, (DialogSettings.npcCoordX, DialogSettings.npcCoordY))

        offset = 0
        for ID, item in enumerate(list(self.items.keys())):
            if ID == self.selectID:
                text = "[F]->" + item + " " + self.items[item]
            else:
                text = "      " + item + " " + self.items[item]
            self.window.blit(self.font.render(text, True, self.fontColor), (ShopSettings.textStartX, ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist

        if self.selectID != len(self.items) - 1:
            texts = ["Money : " + str(self.player.money), itemNameList[self.selectID] + " : " + str(self.player.bag[self.selectID])]
        else:
            texts = ["Money : " + str(self.player.money)]
        offset = 0
        sepX = WindowSettings.width // 5 * 2
        for text in texts:
            self.window.blit(self.font.render(text, True, self.fontColor), (ShopSettings.textStartX + sepX, ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist

class SubMenuBox():
    def __init__(self, window, player,
                 fontSize:int=DialogSettings.textSize,
                 fontColor:Tuple[int, int, int]=(255, 255, 255),
                 bgColor:Tuple[int, int, int, int]=(0, 0, 0, DialogSettings.boxAlpha)):
        self.window = window
        self.player = player

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.bg = pygame.Surface((SubMenuSetting.boxWidth, SubMenuSetting.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.menuBg = pygame.Surface((SubMenuSetting.menuWidth, SubMenuSetting.menuHeight), pygame.SRCALPHA)
        self.menuBg.fill(bgColor)
        
        self.state = SubMenuSetting.stateMenu
        self.bagSelectID = 0
        self.bagSelectCD = 0
        self.usePosion = False
        self.ableToHeal = False

        self.pokeSelectID = 0
        self.pokeSelectCD = 0
        self.pokeTodo = 0
        self.chooseID = 0
        self.pokeExchangeID = 0
        self.pokeSelectFlag = False
        self.pokeExchangeFlag = False
        self.releaseFlag = False
        self.ableToExchange = False

        self.menuSelectID = 0
        self.menuSelectCD = 0
        self.pressCD = 0

        self.overview = False

    def render(self, keys):
        if self.state == SubMenuSetting.stateMenu:  # submenu interface
            self.window.blit(self.menuBg, (SubMenuSetting.menuStartX, SubMenuSetting.menuStartY))
            self.window.blit(self.font.render("Menu", True, self.fontColor), (SubMenuSetting.menuTextStartX, SubMenuSetting.menuTextStartY))

            offset = DialogSettings.textVerticalDist
            texts = ["Pokemon", "Bag", "[Nothing]", "Back", "Exit"]
            for ID in range(len(texts)):
                if ID == self.menuSelectID:
                    text = "[F]->" + texts[ID]
                else:
                    text = "    " + texts[ID]
                self.window.blit(self.font.render(text, True, self.fontColor), (SubMenuSetting.menuTextStartX, SubMenuSetting.menuTextStartY + offset))
                offset += DialogSettings.textVerticalDist

        if self.state == SubMenuSetting.statePokemon:   # Pokemon interface
            self.window.blit(self.bg, (SubMenuSetting.boxStartX, SubMenuSetting.boxStartY))
            if not self.overview:
                if self.pokeSelectFlag == True and not self.pokeExchangeFlag and not self.releaseFlag:
                    texts = ["Overview", "Exchange", "Release", "Back"]
                    offset = 0
                    for ID in range(len(texts)):
                        if ID == self.pokeTodo:
                            text = "[F]->" + texts[ID]
                        else:
                            text = "     " + texts[ID]
                        self.window.blit(self.font.render(text, True, self.fontColor),
                                        (SubMenuSetting.todoTextStartX, SubMenuSetting.todoTextStartY + offset))
                        offset += DialogSettings.textVerticalDist
                
                if self.releaseFlag == True:
                    self.window.blit(self.font.render("Release?", True, self.fontColor), (SubMenuSetting.todoTextStartX, SubMenuSetting.todoTextStartY))
                    texts = ["Yes", "No"]
                    offset = DialogSettings.textVerticalDist
                    for ID in range(len(texts)):
                        if ID == self.chooseID:
                            text = "[F]->" + texts[ID]
                        else:
                            text = "     " + texts[ID]
                        self.window.blit(self.font.render(text, True, self.fontColor),
                                        (SubMenuSetting.todoTextStartX, SubMenuSetting.todoTextStartY + offset))
                        offset += DialogSettings.textVerticalDist
                
                if self.ableToExchange == True:
                    self.window.blit(self.font.render("[F]Exchange", True, self.fontColor), (SubMenuSetting.todoTextStartX, SubMenuSetting.todoTextStartY))

                offset = 0
                for ID in range(len(self.player.pokemons)):
                    pokemon = self.player.pokemons[ID]
                    if pokemon is not None:
                        if ID == 0:
                            image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.startImageWidth, SubMenuSetting.startImageHeight))
                            self.window.blit(image, (SubMenuSetting.startPokeCoorX, SubMenuSetting.startPokeCoorY))
                        else:
                            image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.otherImageWidth, SubMenuSetting.otherImageHeight))
                            if ID == self.pokeSelectID and not self.pokeSelectFlag:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX - 40, SubMenuSetting.otherPokeCoorY + offset))
                            elif ID == self.pokeSelectID or ID == self.pokeExchangeID:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX - 40, SubMenuSetting.otherPokeCoorY + offset))
                            else:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX, SubMenuSetting.otherPokeCoorY + offset))
                            offset += SubMenuSetting.textVerticalDist
                
                for ID in range(7):
                    if not self.pokeExchangeFlag:
                        if ID == self.pokeSelectID and not self.pokeSelectFlag:
                            if ID == 0 and self.player.pokemons[ID] is not None:
                                texts = ["[F]->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}",
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            elif ID == 6:
                                texts = ["[F]->Back"]
                            elif self.player.pokemons[ID] is not None:
                                texts = ["[F]->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}" + \
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            else:
                                texts = ["[F]->[None]"]
                        elif ID == self.pokeSelectID and self.pokeSelectFlag:
                            if ID == 0 and self.player.pokemons[ID] is not None:
                                texts = ["   ->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}",
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            elif self.player.pokemons[ID] is not None:
                                texts = ["   ->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}" + \
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        else:
                            if ID == 0 and self.player.pokemons[ID] is not None:
                                texts = ["     " + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}",
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            elif ID == 6:
                                texts = ["     Back"]
                            elif self.player.pokemons[ID] is not None:
                                texts = ["     " + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}" + \
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            else:
                                texts = ["     [None]"]
                    else:
                        if ID == self.pokeExchangeID:
                            if ID == 0:
                                texts = ["[F]->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}",
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            elif ID == 6:
                                texts = ["[F]->Back"]
                            elif self.player.pokemons[ID] is not None:
                                texts = ["[F]->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}" + \
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            else:
                                texts = ["[F]->[None]"]
                        elif ID == self.pokeSelectID:
                            if ID == 0:
                                texts = ["   ->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}",
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            elif self.player.pokemons[ID] is not None:
                                texts = ["   ->" + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}" + \
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        else:
                            if ID == 0 and self.player.pokemons[ID] is not None:
                                texts = ["     " + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}",
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            elif ID == 6:
                                texts = ["     Back"]
                            elif self.player.pokemons[ID] is not None:
                                texts = ["     " + self.player.pokemons[ID].name,
                                        f"     Level : {self.player.pokemons[ID].level}" + \
                                        f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                            else:
                                texts = ["     [None]"]

                    if ID == 0:
                        offset = 0
                        for text in texts:
                            self.window.blit(self.font.render(text, True, self.fontColor),
                                            (SubMenuSetting.startTextStartX, SubMenuSetting.startTextStartY + offset))
                            offset += DialogSettings.textVerticalDist
                    else:
                        offset = (ID - 1) * SubMenuSetting.textVerticalDist
                        for text in texts:
                            self.window.blit(self.font.render(text, True, self.fontColor),
                                            (SubMenuSetting.otherTextStartX, SubMenuSetting.otherTextStartY + offset))
                            offset += DialogSettings.textVerticalDist


            elif self.overview == True: # Pokemon overview interface
                # includes Pokemon status and moves' description
                pokemon = self.player.pokemons[self.pokeSelectID]
                info = pokemon.get_info()
                image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.imageWidth, SubMenuSetting.imageHeight))
                self.window.blit(image, (SubMenuSetting.imageCoorX, SubMenuSetting.imageCoorY))

                texts = [info[InfoID.name], "", info[InfoID.level], info[InfoID.exp]]
                offset = 0
                for text in texts:
                    self.window.blit(self.font.render(text, True, self.fontColor), 
                                     (SubMenuSetting.leftTextStartX, SubMenuSetting.leftTextStartY + offset))
                    offset += DialogSettings.textVerticalDist

                moveName = ["" for _ in range(4)]
                movePower = ["" for _ in range(4)]
                for i in range(4):
                    if pokemon.moves[i] is not None:
                        moveName[i] = pokemon.moves[i].name
                        movePower[i] = f"Power : {pokemon.moves[i].power}"
                    else:
                        moveName[i] = "[None]"
                        movePower[i] = ""
                texts = [info[InfoID.type], "", info[InfoID.HP], info[InfoID.Atk], info[InfoID.Def], "",
                         moveName[0], movePower[0], "", moveName[2], movePower[2]]
                offset = 0
                for text in texts:
                    self.window.blit(self.font.render(text, True, self.fontColor),
                                     (SubMenuSetting.middleTextStartX, SubMenuSetting.middleTextStartY + offset))
                    offset += DialogSettings.textVerticalDist
                texts = [info[InfoID.nature], "", info[InfoID.SpA], info[InfoID.SpD], info[InfoID.Spd], "",
                         moveName[1], movePower[1], "", moveName[3], movePower[3]]
                offset = 0
                for text in texts:
                    self.window.blit(self.font.render(text, True, self.fontColor),
                                     (SubMenuSetting.rightTextStartX, SubMenuSetting.rightTextStartY + offset))
                    offset += DialogSettings.textVerticalDist

                self.window.blit(self.font.render("Back[Q]", True, self.fontColor), (SubMenuSetting.quitCoorX, SubMenuSetting.quitCoorY))


        if self.state == SubMenuSetting.stateBag:   # bag interface
            self.window.blit(self.bg, (SubMenuSetting.boxStartX, SubMenuSetting.boxStartY))
            if not self.usePosion:
                bagImage = pygame.image.load(GamePath.bag)
                bagImage = pygame.transform.scale(bagImage, (SubMenuSetting.bagImageHeight, SubMenuSetting.bagImageHeight))
                self.window.blit(bagImage, (SubMenuSetting.bagImageCoorX, SubMenuSetting.bagImageCoorY))

                text = f"    Money : {self.player.money}"
                self.window.blit(self.font.render(text, True, self.fontColor), 
                                 (SubMenuSetting.itemStartX, SubMenuSetting.itemStartY))

                offset = DialogSettings.textVerticalDist * 2
                for ID in range(len(self.player.bag) + 1):
                    if ID < len(self.player.bag):
                        if ID == self.bagSelectID:
                            text = "[F]->" + itemNameList[ID] + " : " + str(self.player.bag[ID])
                        else:
                            text = "    " + itemNameList[ID] + " : " + str(self.player.bag[ID])
                        self.window.blit(self.font.render(text, True, self.fontColor), (SubMenuSetting.itemStartX, SubMenuSetting.itemStartY + offset))
                        offset += DialogSettings.textVerticalDist
                    else:
                        if ID == self.bagSelectID:
                            text = "[F]->Back"
                        else:
                            text = "    Back"
                        self.window.blit(self.font.render(text, True, self.fontColor), (SubMenuSetting.quitCoorX, SubMenuSetting.quitCoorY))
                if self.bagSelectID != len(self.player.bag):
                    itemImage = pygame.image.load(GamePath.items[self.bagSelectID])
                    itemImage = pygame.transform.scale(itemImage, (SubMenuSetting.itemImageWidth, SubMenuSetting.itemImageHeight))

                    self.window.blit(itemImage, (SubMenuSetting.itemImageCoorX, SubMenuSetting.itemImageCoorY))
                    self.window.blit(self.font.render(itemDescription[self.bagSelectID], True, self.fontColor),
                                    (SubMenuSetting.textStartX, SubMenuSetting.textStartY))
            else:
                if self.ableToHeal == True:
                    offset = 0
                    texts = [f"Posion : {self.player.bag[ItemID.posion]}", "[F]Heal 20 HP"]
                    for text in texts:
                        self.window.blit(self.font.render(text, True, self.fontColor),
                                         (SubMenuSetting.todoTextStartX, SubMenuSetting.todoTextStartY + offset))
                        offset += DialogSettings.textVerticalDist
                offset = 0
                for ID in range(len(self.player.pokemons)):
                    pokemon = self.player.pokemons[ID]
                    if pokemon is not None:
                        if ID == 0:
                            image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.startImageWidth, SubMenuSetting.startImageHeight))
                            self.window.blit(image, (SubMenuSetting.startPokeCoorX, SubMenuSetting.startPokeCoorY))
                        else:
                            image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.otherImageWidth, SubMenuSetting.otherImageHeight))
                            if ID == self.pokeSelectID and not self.pokeSelectFlag:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX - 40, SubMenuSetting.otherPokeCoorY + offset))
                            elif ID == self.pokeSelectID or ID == self.pokeExchangeID:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX - 40, SubMenuSetting.otherPokeCoorY + offset))
                            else:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX, SubMenuSetting.otherPokeCoorY + offset))
                            offset += SubMenuSetting.textVerticalDist

                for ID in range(7):
                    if ID == self.pokeSelectID:
                        if ID == 0 and self.player.pokemons[ID] is not None:
                            texts = ["[F]->" + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}",
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        elif ID == 6:
                            texts = ["[F]->Back"]
                        elif self.player.pokemons[ID] is not None:
                            texts = ["[F]->" + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}" + \
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        else:
                            texts = ["[F]->[None]"]
                    else:
                        if ID == 0 and self.player.pokemons[ID] is not None:
                            texts = ["     " + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}",
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        elif ID == 6:
                            texts = ["     Back"]
                        elif self.player.pokemons[ID] is not None:
                            texts = ["     " + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}" + \
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        else:
                            texts = ["     [None]"]
                    
                    if ID == 0:
                        offset = 0
                        for text in texts:
                            self.window.blit(self.font.render(text, True, self.fontColor),
                                            (SubMenuSetting.startTextStartX, SubMenuSetting.startTextStartY + offset))
                            offset += DialogSettings.textVerticalDist
                    else:
                        offset = (ID - 1) * SubMenuSetting.textVerticalDist
                        for text in texts:
                            self.window.blit(self.font.render(text, True, self.fontColor),
                                            (SubMenuSetting.otherTextStartX, SubMenuSetting.otherTextStartY + offset))
                            offset += DialogSettings.textVerticalDist


class BattleBox():
    def __init__(self, window, player, npc:NPCtrainer|Pokemon,
                 fontSize:int=BattleSettings.textSize,
                 fontColor:Tuple[int, int, int]=(255, 255, 255),
                 bgColor:Tuple[int, int, int, int]=(0, 0, 0, BattleSettings.boxAlpha)):
        self.window = window
        self.player = player
        self.npcTrainer = None
        self.pressF = False
        
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.bg = pygame.Surface((BattleSettings.boxWidth, BattleSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)

        
        self.frePokemon = player.pokemons[0]
        self.freStat = player.pokemons[0].get_battle_info()
        self.frePokemonImg = pygame.transform.scale(player.pokemons[0].frontImage, (BattleSettings.playerWidth, BattleSettings.playerHeight))
        self.frePokemonX = BattleSettings.playerCoordX
        self.frePokemonY = BattleSettings.playerCoordY

        if isinstance(npc, NPCtrainer):
            self.enePokemon = npc.pokemons[0]
            self.eneStat = npc.pokemons[0].get_battle_info()
            self.enePokemonImg = pygame.transform.scale(npc.pokemons[0].frontImage, (BattleSettings.monsterWidth, BattleSettings.monsterHeight))
            self.npcTrainer = npc
        if isinstance(npc, Pokemon):
            self.enePokemon = npc
            self.eneStat = npc.get_battle_info()
            self.enePokemonImg = pygame.transform.scale(npc.frontImage, (BattleSettings.monsterWidth, BattleSettings.monsterHeight))
        self.enePokemonX = BattleSettings.monsterCoordX
        self.enePokemonY = BattleSettings.monsterCoordY
        
        self.pokeBallX = BattleSettings.pokeBallCoorX
        self.pokeBallY = BattleSettings.pokeBallCoorY
        self.pokeCaptureCnt = 0
        self.ableToRandom = True
        self.determin = True
        self.captureFlag = False
        self.capture = False

        self.cnt = 0
        self.description = []
        self.isPlayingAnimation = False
        self.isFinished = False
        self.isSettle = False
        self.currentAnimationCount = 0
        self.direction = 1
        self.attacker = 0
        self.changeFlag = False
        self.skipFlag = False
        self.exchangeFlag = False
        self.useItemFlag = False
        self.usePosionFlag = False
        self.ableToHeal = False
        self.usePokeBallFlag = False
        self.ballAnimation = False
        self.defeated = False
        self.defeatAll = False
        self.beat = False
        self.npcPokeFlag = False
        self.canCaptureFlag = False
        self.exp = []

        self.state = BattleSettings.stateAct
        self.actSelectID = 0
        self.actSelectCD = 0
        self.moveSelectID = 0
        self.moveSelectCD = 0
        self.bagSelectID = 0
        self.bagSelectCD = 0
        self.pokeSelectID = 1
        self.pokeSelectCD = 0
        self.pressCD = 0

    def settlement(self, battle:Battle.Battle): # generate description after every move
        if not self.skipFlag and not self.defeated:
            if self.attacker == 0:
                damege = battle.attack(self.frePokemon, self.enePokemon, self.frePokemon.moves[self.moveSelectID])
                text = [f"{self.frePokemon.name} used {self.frePokemon.moves[self.moveSelectID].name}! It caused {damege} dameges",
                        battle.effect_description(battle.effect(self.enePokemon, self.frePokemon.moves[self.moveSelectID])) + "   [F]"]

                self.enePokemon.HP = max(0, self.enePokemon.HP - damege)
                self.attacker = 1
                self.direction = -1
            else:
                moveID = randint(0, self.enePokemon.movesNum - 1)
                damege = battle.attack(self.enePokemon, self.frePokemon, self.enePokemon.moves[moveID])
                text = [f"{self.enePokemon.name} used {self.enePokemon.moves[moveID].name}! It caused {damege} dameges",
                        battle.effect_description(battle.effect(self.frePokemon, self.enePokemon.moves[moveID])) + "   [F]"]
                
                self.frePokemon.HP = max(0, self.frePokemon.HP - damege)
                self.attacker = 0
                self.direction = 1
        elif self.capture:
            self.capture = False
            text = [f"Catching {self.enePokemon.name} failed" + "   [F]"]
            self.attacker = 1
            self.direction = -1
        elif not self.usePosionFlag and not self.defeated:
            text = [f"Get Back! {self.player.pokemons[self.pokeSelectID].name}", f"Come out! {self.player.pokemons[0].name}" + "   [F]"]
            self.attacker = 1
            self.direction = -1
        elif self.defeated == True:
            text = [f"Get Back! {self.player.pokemons[self.pokeSelectID].name}", f"Come out! {self.player.pokemons[0].name}" + "   [F]"]
        else:
            text = [f"Player used posion", f"{self.player.pokemons[self.pokeSelectID].name} was healed 20 HP" + "   [F]"]
            self.attacker = 1
            self.direction = -1
        return text

    def render(self, battle:Battle.Battle, keys):
        self.window.blit(self.bg, (BattleSettings.boxStartX, BattleSettings.boxStartY))

        if self.state == BattleSettings.stateAct:   # act interface
            self.window.blit(self.frePokemonImg, (self.frePokemonX, self.frePokemonY))
            self.window.blit(self.enePokemonImg, (self.enePokemonX, self.enePokemonY))
            
            offset = 0
            texts = [self.frePokemon.name, f"Level : {self.frePokemon.level}" ,f"HP : {self.frePokemon.HP}/{self.frePokemon.stat[0]}"]
            for text in texts:
                self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.textPlayerStartX, BattleSettings.textStartY + offset))
                offset += BattleSettings.textVerticalDist
            offset = 0
            texts = [self.enePokemon.name, f"Level : {self.enePokemon.level}", f"HP : {self.enePokemon.HP}/{self.enePokemon.stat[0]}"]
            for text in texts:
                self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.textMonsterStartX, BattleSettings.textStartY + offset))
                offset += BattleSettings.textVerticalDist

            texts = ["Battle", "Bag", "Pokemon", "Escape"]
            for ID in range(4):
                if ID == self.actSelectID:
                    texts[ID] = "[F]->" + texts[ID]
                self.window.blit(self.font.render(texts[ID], True, self.fontColor), (BattleSettings.actCoorX[ID], BattleSettings.actCoorY[ID]))
            

        if self.state == BattleSettings.stateMove:  # choosing move interface
            self.window.blit(self.frePokemonImg, (self.frePokemonX, self.frePokemonY))
            self.window.blit(self.enePokemonImg, (self.enePokemonX, self.enePokemonY))

            offset = 0
            texts = [self.frePokemon.name, f"Level : {self.frePokemon.level}" ,f"HP : {self.frePokemon.HP}/{self.frePokemon.stat[0]}"]
            for text in texts:
                self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.textPlayerStartX, BattleSettings.textStartY + offset))
                offset += BattleSettings.textVerticalDist
            offset = 0
            texts = [self.enePokemon.name, f"Level : {self.enePokemon.level}", f"HP : {self.enePokemon.HP}/{self.enePokemon.stat[0]}"]
            for text in texts:
                self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.textMonsterStartX, BattleSettings.textStartY + offset))
                offset += BattleSettings.textVerticalDist

            if self.cnt >= 2:
                if keys[pygame.K_f] and self.pressCD == 0:
                    self.description = []
                    self.isSettle = False
                    self.cnt = 0
                    self.pressCD = BattleSettings.pressCD

            offset = 0
            for text in self.description:
                self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.descriptionX, BattleSettings.descriptionY + offset))
                offset += BattleSettings.textVerticalDist

            if not self.skipFlag and len(self.description) == 0:
                offset = 0
                texts = [f"Power : {self.frePokemon.moves[self.moveSelectID].power}",
                         f"Type : {typeList[self.frePokemon.moves[self.moveSelectID].type]}",
                         "", "Back[Q]"]
                for text in texts:
                    self.window.blit(self.font.render(text, True, self.fontColor),
                                     (BattleSettings.moveDescriptionX, BattleSettings.moveDescriptionY + offset))
                    offset += BattleSettings.textVerticalDist
            else:
                self.window.blit(self.font.render("Back[Q]", True, self.fontColor),
                                 (BattleSettings.moveDescriptionX, BattleSettings.moveDescriptionY + BattleSettings.textVerticalDist * 3))

            for ID in range(4):
                if ID == self.moveSelectID and not self.isSettle and not self.isFinished and not self.skipFlag:
                    if self.frePokemon.moves[ID] is not None:
                        text = "[F]->" + self.frePokemon.moves[ID].name
                    else:
                        text = "[F]->[None]"
                else:
                    if self.frePokemon.moves[ID] is not None:
                        text = "    " + self.frePokemon.moves[ID].name
                    else:
                        text = "    [None]"
                self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.moveCoorX[ID], BattleSettings.moveCoorY[ID]))

            if self.isPlayingAnimation and not self.isFinished and self.isSettle:
                if self.currentAnimationCount < BattleSettings.animationCount:
                    currentDirection = self.direction
                else:
                    currentDirection = self.direction * -1
                if self.attacker == 0:
                    self.frePokemonX += currentDirection * BattleSettings.stepSize
                else:
                    self.enePokemonX += currentDirection * BattleSettings.stepSize
                self.currentAnimationCount += 1

                if self.currentAnimationCount >= BattleSettings.animationCount * 2:
                    self.isPlayingAnimation = False
                    self.changeFlag = True
                    self.currentAnimationCount = 0
            
            if keys[pygame.K_f] and self.pressCD == 0 and not self.npcPokeFlag:
                if not self.defeated:
                    self.isPlayingAnimation = True
                    self.isSettle = True
                else:
                    self.description = []
                self.skipFlag = False
                self.defeated = False
                self.usePosionFlag = False
                self.pressCD = BattleSettings.pressCD

            if self.changeFlag:
                self.description = self.settlement(battle)
                self.changeFlag = False
                if not self.defeated:
                    self.cnt += 1

            if self.frePokemon.HP == 0 or self.enePokemon.HP == 0:  # judge one Pokemon win
                if len(self.description) != 0:
                    if keys[pygame.K_f]:
                        self.description = []
                        self.pressCD = BattleSettings.pressCD
                else:
                    if self.enePokemon.HP == 0:
                        if self.npcTrainer is not None:
                            
                            if self.npcTrainer.ableToBattlePokeNum > 1:
                                self.npcPokeFlag = True
                                newID = self.npcTrainer.pokemonNum - self.npcTrainer.ableToBattlePokeNum + 1
                                texts = [f"Trainer retrieved {self.enePokemon.name}",
                                         f"Dispatch {self.npcTrainer.pokemons[newID].name}" + "   [F]"]
                                
                                if keys[pygame.K_f] and self.pressCD == 0:
                                    self.npcPokeFlag = False
                                    self.npcTrainer.ableToBattlePokeNum -= 1
                                    ID = self.npcTrainer.pokemonNum - self.npcTrainer.ableToBattlePokeNum
                                    self.enePokemon = self.npcTrainer.pokemons[ID]
                                    self.eneStat = self.npcTrainer.pokemons[ID].get_battle_info()
                                    self.enePokemonImg = pygame.transform.scale(self.npcTrainer.pokemons[ID].frontImage,
                                                                                ((BattleSettings.monsterWidth, BattleSettings.monsterHeight)))
                                    self.attacker = battle.attacker(self.frePokemon, self.enePokemon)
                                    self.direction = 1 - self.attacker * 2
                                    self.pressCD = BattleSettings.pressCD
                            else:
                                self.npcTrainer.ableToBattlePokeNum -= 1
                                texts = ["You win this battle", "Gain 3000 money [ENTER]"]  # gain 3000 money when defeating trainer
                                if self.npcTrainer.BOSSFlag:
                                    texts.append("YOU defeated the BOSS !") # defeat BOSS and end game
                                self.isFinished = True
                                self.beat = True
                        else:
                            texts = ["You win this battle", f"Gain 1000 money [ENTER]"] # gain 1000 money when defeating wild Pokemon
                            self.isFinished = True
                            self.beat = True
                        for ID in range(6):
                            if self.player.pokemons[ID] is not None:    # calculate exp for every Pokemon
                                exp = 4 * (100 + self.player.pokemons[ID].level - self.enePokemon.level) + 5 * self.enePokemon.level
                                if ID != 0:
                                    exp = floor(0.8 * exp)
                                self.exp.append(exp)
                        offset = 0
                        for text in texts:
                            self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.settleCoorX, BattleSettings.settleCoorY + offset))
                            offset += DialogSettings.textVerticalDist
                    if self.frePokemon.HP == 0:
                        if self.player.ableToBattlePokeNum > 1:
                            self.player.ableToBattlePokeNum -= 1
                            self.defeated = True
                            self.state = BattleSettings.statePoke
                        else:
                            self.player.ableToBattlePokeNum -= 1
                            texts = ["You lose this battle", "Half of money was lost [ENTER]"] 
                            # lose half money when being defeated by wildPokemon or trainer
                            offset = 0
                            for text in texts:
                                self.window.blit(self.font.render(text, True, self.fontColor),
                                                 (BattleSettings.settleCoorX, BattleSettings.settleCoorY + offset))
                                offset += BattleSettings.textVerticalDist
                            self.defeatAll = True
                            self.isFinished = True
                    self.cnt = 0
                    self.isSettle = False
                    self.isPlayingAnimation = False
        
        if self.state == BattleSettings.stateBag:   # bag interface
            if not self.usePosionFlag and not self.usePokeBallFlag:
                bagImage = pygame.image.load(GamePath.bag)
                bagImage = pygame.transform.scale(bagImage, (SubMenuSetting.bagImageHeight, SubMenuSetting.bagImageHeight))
                self.window.blit(bagImage, (SubMenuSetting.bagImageCoorX, SubMenuSetting.bagImageCoorY))

                if self.canCaptureFlag:
                    texts = ["Can not catch more Pokemon", "Please release Pokemon first" + "   [F]"]
                    # can not catch new Pokemon when the number of your Pokemons reaches to 6
                    offset = 0
                    for text in texts:
                        self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.descriptionX, BattleSettings.descriptionY + offset))
                        offset += DialogSettings.textVerticalDist
                else:
                    offset = 0
                    for ID in range(len(self.player.bag) + 1):
                        if ID < len(self.player.bag):
                            if ID == self.bagSelectID:
                                text = "[F]->" + itemNameList[ID] + " : " + str(self.player.bag[ID])
                            else:
                                text = "    " + itemNameList[ID] + " : " + str(self.player.bag[ID])
                            self.window.blit(self.font.render(text, True, self.fontColor), (SubMenuSetting.itemStartX, SubMenuSetting.itemStartY + offset))
                            offset += DialogSettings.textVerticalDist
                        else:
                            if ID == self.bagSelectID:
                                text = "[F]->Back"
                            else:
                                text = "    Back"
                            self.window.blit(self.font.render(text, True, self.fontColor), (SubMenuSetting.quitCoorX, SubMenuSetting.quitCoorY))
                    if self.bagSelectID != len(self.player.bag):
                        itemImage = pygame.image.load(GamePath.items[self.bagSelectID])
                        itemImage = pygame.transform.scale(itemImage, (SubMenuSetting.itemImageWidth, SubMenuSetting.itemImageHeight))

                        self.window.blit(itemImage, (SubMenuSetting.itemImageCoorX, SubMenuSetting.itemImageCoorY))
                        self.window.blit(self.font.render(itemDescription[self.bagSelectID], True, self.fontColor),
                                        (SubMenuSetting.textStartX, SubMenuSetting.textStartY))
            elif self.usePokeBallFlag == True:  # use PokeBall interface
                image = pygame.image.load(GamePath.items[ItemID.pokeBall])
                image = pygame.transform.scale(image, (BattleSettings.pokeBallWidth, BattleSettings.pokeBallHeight))
                if self.determin == True:
                    self.window.blit(image, (self.pokeBallX, self.pokeBallY))
                    if self.ballAnimation:
                        if self.currentAnimationCount < BattleSettings.animationCount * 2:
                            if self.currentAnimationCount < BattleSettings.animationCount:
                                currentDirection = -1
                            else:
                                currentDirection = 1
                            self.pokeBallY += currentDirection * BattleSettings.stepSize
                        self.currentAnimationCount += 1

                        if self.currentAnimationCount >= BattleSettings.animationCount * 4:
                            self.ableToRandom = True
                            self.ballAnimation = False
                            self.currentAnimationCount = 0

                if self.captureFlag == True:    # catch successfully
                    text = f"Congratulation! {self.enePokemon.name} GET!  [ENTER]"
                    self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.descriptionX, BattleSettings.descriptionY))
                if not self.determin:           # catching failed
                    text = f"Oh no! {self.enePokemon.name} broke away!  [F]"
                    self.window.blit(self.font.render(text, True, self.fontColor), (BattleSettings.descriptionX, BattleSettings.descriptionY))

            elif self.usePosionFlag == True:    # use posion interface
                if self.ableToHeal == True:
                    offset = 0
                    texts = [f"Posion : {self.player.bag[ItemID.posion]}", "[F]Heal 20 HP"]
                    for text in texts:
                        self.window.blit(self.font.render(text, True, self.fontColor),
                                         (SubMenuSetting.todoTextStartX, SubMenuSetting.todoTextStartY + offset))
                        offset += DialogSettings.textVerticalDist
                offset = 0
                for ID in range(len(self.player.pokemons)):
                    pokemon = self.player.pokemons[ID]
                    if pokemon is not None:
                        if ID == 0:
                            image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.startImageWidth, SubMenuSetting.startImageHeight))
                            self.window.blit(image, (SubMenuSetting.startPokeCoorX, SubMenuSetting.startPokeCoorY))
                        else:
                            image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.otherImageWidth, SubMenuSetting.otherImageHeight))
                            if ID == self.pokeSelectID:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX - 40, SubMenuSetting.otherPokeCoorY + offset))
                            else:
                                self.window.blit(image, (SubMenuSetting.otherPokeCoorX, SubMenuSetting.otherPokeCoorY + offset))
                            offset += SubMenuSetting.textVerticalDist

                for ID in range(7):
                    if ID == self.pokeSelectID:
                        if ID == 0 and self.player.pokemons[ID] is not None:
                            texts = ["[F]->" + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}",
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        elif ID == 6:
                            texts = ["[F]->Back"]
                        elif self.player.pokemons[ID] is not None:
                            texts = ["[F]->" + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}" + \
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        else:
                            texts = ["[F]->[None]"]
                    else:
                        if ID == 0 and self.player.pokemons[ID] is not None:
                            texts = ["     " + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}",
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        elif ID == 6:
                            texts = ["     Back"]
                        elif self.player.pokemons[ID] is not None:
                            texts = ["     " + self.player.pokemons[ID].name,
                                    f"     Level : {self.player.pokemons[ID].level}" + \
                                    f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                        else:
                            texts = ["     [None]"]
                    
                    if ID == 0:
                        offset = 0
                        for text in texts:
                            self.window.blit(self.font.render(text, True, self.fontColor),
                                            (SubMenuSetting.startTextStartX, SubMenuSetting.startTextStartY + offset))
                            offset += DialogSettings.textVerticalDist
                    else:
                        offset = (ID - 1) * SubMenuSetting.textVerticalDist
                        for text in texts:
                            self.window.blit(self.font.render(text, True, self.fontColor),
                                            (SubMenuSetting.otherTextStartX, SubMenuSetting.otherTextStartY + offset))
                            offset += DialogSettings.textVerticalDist

        if self.state == BattleSettings.statePoke:  # chooose Pokemon interface
            if self.pokeSelectID < 6:
                if self.player.pokemons[self.pokeSelectID] is not None:
                    self.window.blit(self.font.render("[F]Exchange", True, self.fontColor),
                                     (SubMenuSetting.todoTextStartX, SubMenuSetting.todoTextStartY))

            offset = 0
            for ID in range(len(self.player.pokemons)):
                pokemon = self.player.pokemons[ID]
                if pokemon is not None:
                    if ID == 0:
                        image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.startImageWidth, SubMenuSetting.startImageHeight))
                        self.window.blit(image, (SubMenuSetting.startPokeCoorX, SubMenuSetting.startPokeCoorY))
                    else:
                        image = pygame.transform.scale(pokemon.frontImage, (SubMenuSetting.otherImageWidth, SubMenuSetting.otherImageHeight))
                        if ID == self.pokeSelectID:
                            self.window.blit(image, (SubMenuSetting.otherPokeCoorX - 40, SubMenuSetting.otherPokeCoorY + offset))
                        else:
                            self.window.blit(image, (SubMenuSetting.otherPokeCoorX, SubMenuSetting.otherPokeCoorY + offset))
                        offset += SubMenuSetting.textVerticalDist

            for ID in range(7):
                if ID == self.pokeSelectID:
                    if ID == 6:
                        texts = ["[F]->Back"]
                    elif self.player.pokemons[ID] is not None:
                        texts = ["[F]->" + self.player.pokemons[ID].name,
                                f"     Level : {self.player.pokemons[ID].level}" + \
                                f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                    else:
                        texts = ["[F]->[None]"]
                else:
                    if ID == 0:
                        texts = ["   ->" + self.player.pokemons[ID].name,
                                f"     Level : {self.player.pokemons[ID].level}",
                                f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                    elif ID == 6:
                        texts = ["     Back"]
                    elif self.player.pokemons[ID] is not None:
                        texts = ["     " + self.player.pokemons[ID].name,
                                f"     Level : {self.player.pokemons[ID].level}" + \
                                f"     HP : {self.player.pokemons[ID].HP}/{self.player.pokemons[ID].stat[StatID.HP]}"]
                    else:
                        texts = ["     [None]"]
                
                if ID == 0:
                    offset = 0
                    for text in texts:
                        self.window.blit(self.font.render(text, True, self.fontColor),
                                        (SubMenuSetting.startTextStartX, SubMenuSetting.startTextStartY + offset))
                        offset += DialogSettings.textVerticalDist
                else:
                    offset = (ID - 1) * SubMenuSetting.textVerticalDist
                    for text in texts:
                        self.window.blit(self.font.render(text, True, self.fontColor),
                                        (SubMenuSetting.otherTextStartX, SubMenuSetting.otherTextStartY + offset))
                        offset += DialogSettings.textVerticalDist

        if  self.state == BattleSettings.stateEscape:   # escape interface
            if self.player.encounter == True:
                text = "Successfully escaped! [ENTER]"
            else:
                text = "The battle between Trainers should not escape! [F]"
            self.window.blit(self.font.render(text, True, self.fontColor), (WindowSettings.width // 6, WindowSettings.height // 2))