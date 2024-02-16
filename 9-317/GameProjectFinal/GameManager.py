import pygame
import sys

import Scene
import Attributes
import Player
import Battle
import BgmPlayer
from Pokemon import *
from PopUpBox import *
from Settings import *

class Gamemanager():
    def __init__(self, window):
        self.window = window
        self.scene = Scene.MainMenuScene(window, 0, 0)
        self.state = GameState.MAIN_MENU
        self.clock = pygame.time.Clock()
        self.bgm = BgmPlayer.BgmPlayer()

        # trigger -> event
        self.pressF = False
        self.talkingFlag = False
        self.shoppingFlag = False
        self.subMenuFlag = False
        self.battleFlag = False

    def tick(self, fps):    # ticks
        self.clock.tick(fps)
    def get_width(self):
        if self.state == GameState.GAME_PLAY_CITY:
            return WindowSettings.width * WindowSettings.outdoorScale
        elif self.state == GameState.GAME_PLAY_WILD:
            return SceneSettings.wild_tileXnum * SceneSettings.tileWidth
        else:
            return WindowSettings.width
    def get_height(self):
        if self.state == GameState.GAME_PLAY_CITY:
            return WindowSettings.height * WindowSettings.outdoorScale
        elif self.state == GameState.GAME_PLAY_WILD:
            return SceneSettings.wild_tileYnum * SceneSettings.tileHeight
        else:
            return WindowSettings.height

    # TRIGGERS : check whether event should happen

    def  talking_trigger(self, player:Player.Player, keys):
        if self.scene.dialogBox is None and self.scene.subMenuBox is None:  #can not talk while opening submenu
            for npc in self.scene.npcsNormal.sprites():
                if npc.can_talk() and player.colliSys.is_colliding_npcNormal(player, npc):
                    if keys[pygame.K_f]:
                        self.pressF = True
                    elif self.pressF == True:
                        if self.scene.state == GameState.GAME_PLAY_HOSPITAL:    # npc in hospital will heal Pokemons
                            self.scene.dialogBox = DialogBox(self.window, GamePath.healer, ["Your Pokemons have been healed. [ENTER]"])
                            for pokemon in player.pokemons:
                                if pokemon is not None:
                                    pokemon.HP = pokemon.stat[StatID.HP]
                        else:
                            self.scene.dialogBox = DialogBox(self.window, npc.path, npc.texts)
                        npc.talking = True
                        player.talking = True
                        self.scene.talkWith = npc
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG))   # event queue

    def shopping_trigger(self, player:Player.Player, keys):
        if self.scene.shoppingBox is None and self.scene.subMenuBox is None:    # can not shop while opening submenu
            for npc in self.scene.npcsTrader.sprites():
                if npc.can_talk() and player.colliSys.is_colliding_npcTrader(player, npc):
                    if keys[pygame.K_f]:
                        self.pressF = True
                    if self.pressF == True:
                        npc.talking = True
                        player.talking = True
                        self.scene.tradeWith = npc
                        self.scene.shoppingBox = ShopingBox(self.window, npc.path, player, itemList)
                        self.scene.shoppingBox.pressCD = ShopSettings.pressCD
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP)) # event queue
    
    def submenu_trigger(self, player:Player.Player, keys):
        if self.scene.battleBox is not None or self.scene.shoppingBox is not None:  # can not open submenu while shopping and battling
            return
        if self.scene.subMenuBox is None:
            if keys[pygame.K_e]:
                player.talking = True
                self.scene.subMenuBox = SubMenuBox(self.window, player)
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_SUBMENU))  # event queue

    def battle_trigger(self, player:Player.Player, keys):
        if self.scene.battleBox is None and self.scene.subMenuBox is None:  # can not battle while opening submenu
            if player.check_able_to_battle():   # check whether left Pokemons can battle
                for npc in self.scene.npcsTrainer.sprites():
                    if player.colliSys.is_colliding_npcTrainer(player, npc) and npc.ableToBattle == True and player.battleFailCD == 0:
                        # initailize battle settings

                        npc.battling = True
                        player.battling = True
                        for ID in range(player.pokemonNum): # avoid the first pokemon can not battle
                            if player.pokemons[ID].HP > 0:
                                tempPokemon = player.pokemons[0]
                                player.pokemons[0] = player.pokemons[ID]
                                player.pokemons[ID] = tempPokemon
                                break
                        self.scene.battleWith = npc
                        self.scene.battle = Battle.Battle()
                        self.scene.battleBox = BattleBox(self.window, player, npc)

                        self.scene.battleBox.actSelectCD = BattleSettings.actSelectCD
                        self.scene.battleBox.isFinished = False
                        self.scene.battleBox.changeFlag = False
                        self.scene.battleBox.attacker = self.scene.battle.attacker(player.pokemons[0], npc.pokemons[0])
                        self.scene.battleBox.direction = 1 - self.scene.battleBox.attacker * 2
                        self.scene.battleBox.render(self.scene.battle, keys)
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))   # event queue
                if player.encounter == True:
                    # if it is wild Pokemon

                    wildPokemon = wildPokemons[randint(0, len(wildPokemons) - 1)]
                    player.battling = True
                    self.scene.battle = Battle.Battle()
                    self.scene.battleBox = BattleBox(self.window, player, wildPokemon)

                    self.scene.battleBox.actSelectCD = BattleSettings.actSelectCD
                    self.scene.battleBox.isFinished = False
                    self.scene.battleBox.changeFlag = False
                    for ID in range(player.pokemonNum): # avoid the first pokemon can not battle
                        if player.pokemons[ID].HP >= 0:
                            tempPokemon = player.pokemons[0]
                            player.pokemons[0] = player.pokemons[ID]
                            player.pokemons[ID] = tempPokemon
                            break
                    self.scene.battleBox.attacker = self.scene.battle.attacker(player.pokemons[0], wildPokemon)
                    self.scene.battleBox.direction = 1 - self.scene.battleBox.attacker * 2
                    self.scene.battleBox.render(self.scene.battle, keys)
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))   # event queue
            else:
                for npc in self.scene.npcsTrainer.sprites():
                    if player.colliSys.is_colliding_npcTrainer(player, self.scene) or player.encounter == True:
                        if player.battleFailCD == 0:
                            player.talking = True
                            player.battleFailCD = BattleSettings.battleCD
                            self.scene.dialogBox = DialogBox(self.window, GamePath.player_down[0], ["No Pokemon can battle!   [ENTER]"])
                            pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG))   # event queue

    # EVENTS : recieving trigger and execute logical judgements

    def event_talking(self, player:Player.Player, keys):
        self.scene.dialogBox.render()
        if keys[pygame.K_RETURN]:
            if self.scene.talkWith is not None:
                self.scene.talkWith.talking = False
                self.scene.talkWith.reset_talkCD()
                self.scene.talkWith = None
            self.pressF = False
            player.talking = False
            self.scene.dialogBox = None
            self.talkingFlag = False
    
    def event_shopping(self, player:Player.Player, keys):
        # CD counter
        self.scene.shoppingBox.selectCD = max(0, self.scene.shoppingBox.selectCD - 1)
        self.scene.shoppingBox.pressCD = max(0, self.scene.shoppingBox.pressCD - 1)
        self.scene.shoppingBox.render()

        itemsNum = len(self.scene.shoppingBox.items)
        if self.scene.shoppingBox.selectCD == 0:    # selecting
            if keys[pygame.K_w]:
                self.scene.shoppingBox.selectID = (self.scene.shoppingBox.selectID - 1 + itemsNum) % itemsNum
                self.scene.shoppingBox.selectCD = ShopSettings.selectCD
            if keys[pygame.K_s]:
                self.scene.shoppingBox.selectID = (self.scene.shoppingBox.selectID + 1 + itemsNum) % itemsNum
                self.scene.shoppingBox.selectCD = ShopSettings.selectCD
        if keys[pygame.K_f] and self.scene.shoppingBox.pressCD == 0:
            self.scene.shoppingBox.pressCD = ShopSettings.pressCD
            if self.scene.shoppingBox.selectID == itemsNum - 1: # quit shopping
                self.scene.tradeWith.talking = False
                player.talking = False
                self.pressF = False
                self.scene.tradeWith.reset_talkCD()
                self.scene.tradeWith = None
                self.scene.shoppingBox.selectCD = 0
                self.scene.shoppingBox = None
                self.shoppingFlag = False
            else:
                self.scene.shoppingBox.buy()

    def event_submenu(self, player:Player.Player, keys):
        # CD counter
        self.scene.subMenuBox.menuSelectCD = max(0, self.scene.subMenuBox.menuSelectCD - 1)
        self.scene.subMenuBox.bagSelectCD = max(0, self.scene.subMenuBox.bagSelectCD - 1)
        self.scene.subMenuBox.pokeSelectCD = max(0, self.scene.subMenuBox.pokeSelectCD - 1)
        self.scene.subMenuBox.pressCD = max(0, self.scene.subMenuBox.pressCD - 1)
        self.scene.subMenuBox.render(keys)

        if self.scene.subMenuBox.state == SubMenuSetting.statePokemon:  # submenu state Pokemon interface
            if self.scene.subMenuBox.pokeSelectCD == 0 and self.scene.subMenuBox.pressCD == 0:
                if not self.scene.subMenuBox.pokeSelectFlag:
                    if keys[pygame.K_w]:
                        self.scene.subMenuBox.pokeSelectID = max(0, self.scene.subMenuBox.pokeSelectID - 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_s]:
                        self.scene.subMenuBox.pokeSelectID = min(6, self.scene.subMenuBox.pokeSelectID + 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_a]:
                        self.scene.subMenuBox.pokeSelectID = 0
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_d]:
                        self.scene.subMenuBox.pokeSelectID = 1
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_f]:
                        if self.scene.subMenuBox.pokeSelectID == 6:
                            self.scene.subMenuBox.state = SubMenuSetting.stateMenu
                            self.scene.subMenuBox.pokeSelectID = 0
                        elif player.pokemons[self.scene.subMenuBox.pokeSelectID] is not None:   # select one Pokemon
                            self.scene.subMenuBox.pokeSelectFlag = True
                        self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD
                elif not self.scene.subMenuBox.pokeExchangeFlag and not self.scene.subMenuBox.releaseFlag:  # subselections for one Pokemon
                    if keys[pygame.K_w]:
                        self.scene.subMenuBox.pokeTodo = max(0, self.scene.subMenuBox.pokeTodo - 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_s]:
                        self.scene.subMenuBox.pokeTodo = min(3, self.scene.subMenuBox.pokeTodo + 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_f]:
                        if self.scene.subMenuBox.pokeTodo == 0: # substate show Pokemon's overview
                            self.scene.subMenuBox.overview = True
                        if self.scene.subMenuBox.pokeTodo == 1: # substate exchange Pokemons
                            self.scene.subMenuBox.pokeExchangeFlag = True
                            if self.scene.subMenuBox.pokeSelectID == 0:
                                self.scene.subMenuBox.pokeExchangeID = 1
                            else:
                                self.scene.subMenuBox.pokeExchangeID = 0
                        if self.scene.subMenuBox.pokeTodo == 2: # substate release Pokemon
                            if player.pokemonNum > 1:
                                self.scene.subMenuBox.releaseFlag = True
                                self.scene.subMenuBox.chooseID = 1
                        if self.scene.subMenuBox.pokeTodo == 3: # back to the Pokemon interface
                            self.scene.subMenuBox.pokeSelectFlag = False
                            self.scene.subMenuBox.pokeTodo = 0
                        self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD
                
                if self.scene.subMenuBox.overview == True:  # overviw
                    if keys[pygame.K_q]:
                        self.scene.subMenuBox.overview = False
                        self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD

                if self.scene.subMenuBox.releaseFlag == True and self.scene.subMenuBox.pressCD == 0:    # release
                        if keys[pygame.K_w]:
                            self.scene.subMenuBox.chooseID = max(0, self.scene.subMenuBox.chooseID - 1)
                            self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD
                        if keys[pygame.K_s]:
                            self.scene.subMenuBox.chooseID = min(1, self.scene.subMenuBox.chooseID + 1)
                            self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD
                        if keys[pygame.K_f]:
                            if self.scene.subMenuBox.chooseID == 0:
                                player.release_pokemon(self.scene.subMenuBox.pokeSelectID)
                                self.scene.subMenuBox.releaseFlag = False
                                self.scene.subMenuBox.pokeSelectFlag = False
                            if self.scene.subMenuBox.chooseID == 1:
                                self.scene.subMenuBox.releaseFlag = False
                            self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD

                if self.scene.subMenuBox.pokeExchangeFlag == True and self.scene.subMenuBox.pressCD == 0:   # exchange
                    if self.scene.subMenuBox.pokeExchangeID != 6:
                        if player.pokemons[self.scene.subMenuBox.pokeExchangeID] is not None:
                            self.scene.subMenuBox.ableToExchange = True
                        else:
                            self.scene.subMenuBox.ableToExchange = False
                    else:
                        self.scene.subMenuBox.ableToExchange = False
                    # select the other Pokemon
                    
                    if keys[pygame.K_w]:
                        self.scene.subMenuBox.pokeExchangeID = max(0, self.scene.subMenuBox.pokeExchangeID - 1)
                        if self.scene.subMenuBox.pokeExchangeID == self.scene.subMenuBox.pokeSelectID:
                            if self.scene.subMenuBox.pokeSelectID == 0:
                                self.scene.subMenuBox.pokeExchangeID = 1
                            else:
                                self.scene.subMenuBox.pokeExchangeID = max(0, self.scene.subMenuBox.pokeExchangeID - 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_s]:
                        self.scene.subMenuBox.pokeExchangeID = min(6, self.scene.subMenuBox.pokeExchangeID + 1)
                        if self.scene.subMenuBox.pokeExchangeID == self.scene.subMenuBox.pokeSelectID:
                            self.scene.subMenuBox.pokeExchangeID = min(6, self.scene.subMenuBox.pokeExchangeID + 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_a]:
                        if self.scene.subMenuBox.pokeSelectID == 0:
                            self.scene.subMenuBox.pokeExchangeID = 1
                        else:
                            self.scene.subMenuBox.pokeExchangeID = 0
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_d]:
                        if self.scene.subMenuBox.pokeSelectID == 1:
                            self.scene.subMenuBox.pokeExchangeID = 2
                        else:
                            self.scene.subMenuBox.pokeExchangeID = 1
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_f]:
                        if self.scene.subMenuBox.pokeExchangeID == 6:
                            self.scene.subMenuBox.pokeExchangeFlag = False
                        elif self.scene.subMenuBox.ableToExchange == True:
                            tempPokemon = player.pokemons[self.scene.subMenuBox.pokeSelectID]
                            player.pokemons[self.scene.subMenuBox.pokeSelectID] = player.pokemons[self.scene.subMenuBox.pokeExchangeID]
                            player.pokemons[self.scene.subMenuBox.pokeExchangeID] = tempPokemon
                            
                            self.scene.subMenuBox.pokeSelectID = self.scene.subMenuBox.pokeExchangeID
                            self.scene.subMenuBox.pokeExchangeID = 0
                            self.scene.subMenuBox.ableToExchange = False
                            self.scene.subMenuBox.pokeExchangeFlag = False
                        self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD

        if self.scene.subMenuBox.state == SubMenuSetting.stateBag:  # submenu bag interface
            if self.scene.subMenuBox.bagSelectCD == 0 and self.scene.subMenuBox.pressCD == 0 and self.scene.subMenuBox.pokeSelectCD == 0:
                if self.scene.subMenuBox.usePosion == True: # use posion to heal Pokemon
                    if self.scene.subMenuBox.pokeSelectID < 6:
                        if player.pokemons[self.scene.subMenuBox.pokeSelectID] is not None:
                            self.scene.subMenuBox.ableToHeal = True
                        else:
                            self.scene.subMenuBox.ableToHeal = False
                    # selection for Pokemon

                    if keys[pygame.K_w]:
                        self.scene.subMenuBox.pokeSelectID = max(0, self.scene.subMenuBox.pokeSelectID - 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_s]:
                        self.scene.subMenuBox.pokeSelectID = min(6, self.scene.subMenuBox.pokeSelectID + 1)
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_a]:
                        self.scene.subMenuBox.pokeSelectID = 0
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD
                    if keys[pygame.K_d]:
                        self.scene.subMenuBox.pokeSelectID = 1
                        self.scene.subMenuBox.pokeSelectCD = SubMenuSetting.pokeSelectCD   
                    if keys[pygame.K_f]:
                        if self.scene.subMenuBox.pokeSelectID == 6:
                            self.scene.subMenuBox.usePosion = False
                        if self.scene.subMenuBox.ableToHeal == True:
                            ID = self.scene.subMenuBox.pokeSelectID
                            if player.pokemons[ID].HP < player.pokemons[ID].stat[StatID.HP] and player.bag[ItemID.posion] > 0:
                                player.pokemons[ID].HP = min(player.pokemons[ID].stat[StatID.HP], player.pokemons[ID].HP + 20)
                                player.bag[ItemID.posion] -= 1
                        self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD
                else:
                    # selection for item

                    if keys[pygame.K_w]:
                        self.scene.subMenuBox.bagSelectID = max(0, self.scene.subMenuBox.bagSelectID - 1)
                        self.scene.subMenuBox.bagSelectCD = SubMenuSetting.bagSelectCD
                    if keys[pygame.K_s]:
                        self.scene.subMenuBox.bagSelectID = min(len(player.bag), self.scene.subMenuBox.bagSelectID + 1)
                        self.scene.subMenuBox.bagSelectCD = SubMenuSetting.bagSelectCD
                    if keys[pygame.K_f]:
                        if self.scene.subMenuBox.bagSelectID == len(player.bag):    # back to submenu
                            self.scene.subMenuBox.state = SubMenuSetting.stateMenu
                            self.scene.subMenuBox.bagSelectID = 0
                        if self.scene.subMenuBox.bagSelectID == ItemID.posion and player.bag[ItemID.posion] > 0:    # use posion
                            self.scene.subMenuBox.usePosion = True
                        self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD
        
        if self.scene.subMenuBox.state == SubMenuSetting.stateMenu: #submenu interface
            if self.scene.subMenuBox.menuSelectCD == 0 and self.scene.subMenuBox.pressCD == 0:
                if keys[pygame.K_w]:
                    self.scene.subMenuBox.menuSelectID = max(0, self.scene.subMenuBox.menuSelectID - 1)
                    self.scene.subMenuBox.menuSelectCD = SubMenuSetting.menuSelectCD
                if keys[pygame.K_s]:
                    self.scene.subMenuBox.menuSelectID = min(4, self.scene.subMenuBox.menuSelectID + 1)
                    self.scene.subMenuBox.menuSelectCD = SubMenuSetting.menuSelectCD
                if keys[pygame.K_f]:
                    if self.scene.subMenuBox.menuSelectID < 2:  # choose Pokemon or Bag
                        self.scene.subMenuBox.state = self.scene.subMenuBox.menuSelectID
                        self.scene.subMenuBox.pressCD = SubMenuSetting.pressCD
                    if self.scene.subMenuBox.menuSelectID == SubMenuSetting.stateExit:  # quit game
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    if self.scene.subMenuBox.menuSelectID == SubMenuSetting.stateBack:  # back to game
                        player.talking = False
                        self.scene.subMenuBox = None
                        self.subMenuFlag = False

    def event_battle(self, player:Player.Player, keys):
        # CD counter
        self.scene.battleBox.moveSelectCD = max(0, self.scene.battleBox.moveSelectCD - 1)
        self.scene.battleBox.bagSelectCD = max(0, self.scene.battleBox.bagSelectCD - 1)
        self.scene.battleBox.pokeSelectCD = max(0, self.scene.battleBox.pokeSelectCD - 1)
        self.scene.battleBox.actSelectCD = max(0, self.scene.battleBox.actSelectCD - 1)
        self.scene.battleBox.pressCD = max(0, self.scene.battleBox.pressCD - 1)
        self.scene.battleBox.render(self.scene.battle, keys)

        if self.scene.battleBox.state == BattleSettings.stateAct and not self.scene.battleBox.isFinished:   # game state act choose interface
            if self.scene.battleBox.actSelectCD == 0 and self.scene.battleBox.pressCD == 0:
                if keys[pygame.K_w] or keys[pygame.K_s]:
                    self.scene.battleBox.actSelectID = (self.scene.battleBox.actSelectID + 2) % 4
                    self.scene.battleBox.actSelectCD = BattleSettings.actSelectCD
                if keys[pygame.K_a]:
                    self.scene.battleBox.actSelectID = (self.scene.battleBox.actSelectID + 3) % 4
                    self.scene.battleBox.actSelectCD = BattleSettings.actSelectCD
                if keys[pygame.K_d]:
                    self.scene.battleBox.actSelectID = (self.scene.battleBox.actSelectID + 1) % 4
                    self.scene.battleBox.actSelectCD = BattleSettings.actSelectCD
                if keys[pygame.K_f]:
                    self.scene.battleBox.state = self.scene.battleBox.actSelectID
                    self.scene.battleBox.pressCD = BattleSettings.pressCD
        
        # choose move to attack enemy Pokemon
        if self.scene.battleBox.state == BattleSettings.stateMove and not self.scene.battleBox.isFinished and not self.scene.battleBox.skipFlag:
            if self.scene.battleBox.moveSelectCD == 0 and self.scene.battleBox.pressCD == 0:
                if keys[pygame.K_w] or keys[pygame.K_s]:
                    if self.scene.battleBox.frePokemon.moves[(self.scene.battleBox.moveSelectID + 2) % 4] is not None:
                        self.scene.battleBox.moveSelectID = (self.scene.battleBox.moveSelectID + 2) % 4
                        self.scene.battleBox.moveSelectCD = BattleSettings.moveSelectCD
                if keys[pygame.K_a]:
                    if self.scene.battleBox.frePokemon.moves[(self.scene.battleBox.moveSelectID + 3) % 4] is not None:
                        self.scene.battleBox.moveSelectID = (self.scene.battleBox.moveSelectID + 3) % 4
                        self.scene.battleBox.moveSelectCD = BattleSettings.moveSelectCD
                if keys[pygame.K_d]:
                    if self.scene.battleBox.frePokemon.moves[(self.scene.battleBox.moveSelectID + 1) % 4] is not None:
                        self.scene.battleBox.moveSelectID = (self.scene.battleBox.moveSelectID + 1) % 4
                        self.scene.battleBox.moveSelectCD = BattleSettings.moveSelectCD
                if keys[pygame.K_q]:
                    if len(self.scene.battleBox.description) == 0:
                        self.scene.battleBox.state = BattleSettings.stateAct

        if self.scene.battleBox.state == BattleSettings.stateBag:   # use bag while battling
            if self.scene.battleBox.bagSelectCD == 0 and self.scene.battleBox.pokeSelectCD == 0 and self.scene.battleBox.pressCD == 0:
                if self.scene.battleBox.usePosionFlag == True:  # use pposion while battling
                    if self.scene.battleBox.pokeSelectID < 6:
                        if player.pokemons[self.scene.battleBox.pokeSelectID] is not None:
                            self.scene.battleBox.ableToHeal = True
                        else:
                            self.scene.battleBox.ableToHeal = False
                    if keys[pygame.K_w]:
                        self.scene.battleBox.pokeSelectID = max(0, self.scene.battleBox.pokeSelectID - 1)
                        self.scene.battleBox.pokeSelectCD = BattleSettings.pokeSelectCD
                    if keys[pygame.K_s]:
                        self.scene.battleBox.pokeSelectID = min(6, self.scene.battleBox.pokeSelectID + 1)
                        self.scene.battleBox.pokeSelectCD = BattleSettings.pokeSelectCD
                    if keys[pygame.K_a]:
                        self.scene.battleBox.pokeSelectID = 0
                        self.scene.battleBox.pokeSelectCD = BattleSettings.pokeSelectCD
                    if keys[pygame.K_d]:
                        self.scene.battleBox.pokeSelectID = 1
                        self.scene.battleBox.pokeSelectCD = BattleSettings.pokeSelectCD
                    if keys[pygame.K_f]:
                        if self.scene.battleBox.pokeSelectID == 6:
                            self.scene.battleBox.usePosionFlag = False
                            self.scene.battleBox.pokeSelectID = 1
                        elif self.scene.battleBox.ableToHeal == True:
                            ID = self.scene.battleBox.pokeSelectID
                            if player.pokemons[ID].HP < player.pokemons[ID].stat[StatID.HP]:
                                if player.pokemons[ID].HP == 0:
                                    player.ableToBattlePokeNum += 1
                                player.pokemons[ID].HP = min(player.pokemons[ID].stat[StatID.HP], player.pokemons[ID].HP + 20)
                                player.bag[ItemID.posion] -= 1
                                self.scene.battleBox.changeFlag = True  # after using posion, can just wait the enemy Pokemon to attack
                                self.scene.battleBox.skipFlag = True
                                self.scene.battleBox.state = BattleSettings.stateMove
                        self.scene.battleBox.pressCD = BattleSettings.pressCD
                elif self.scene.battleBox.usePokeBallFlag == True:  # use PokeBall to catch wild Pokemon
                    if self.scene.battleBox.ableToRandom and self.scene.battleBox.pokeCaptureCnt < 3:   # 3 turn in total
                        self.scene.battleBox.pokeBallX = BattleSettings.pokeBallCoorX
                        self.scene.battleBox.pokeBallY = BattleSettings.pokeBallCoorY
                        randNum = randint(0, 3) # the Probability for successfully catch is 0.75 for one turn
                        if randNum != 3:
                            self.scene.battleBox.pokeCaptureCnt += 1
                            self.scene.battleBox.ableToRandom = False
                            self.scene.battleBox.ballAnimation = True
                        else:
                            self.scene.battleBox.determin = False
                        
                    if not self.scene.battleBox.determin:   # catchinf failed
                        if keys[pygame.K_f]:
                            self.scene.battleBox.ableToRandom = True
                            self.scene.battleBox.ballAnimation = False
                            self.scene.battleBox.usePokeBallFlag = False
                            self.scene.battleBox.captureFlag = False
                            self.scene.battleBox.determin = True
                            self.scene.battleBox.pokeCaptureCnt = 0
                            self.scene.battleBox.capture = True

                            self.scene.battleBox.currentAnimationCount = 0
                            self.scene.battleBox.changeFlag = True
                            self.scene.battleBox.skipFlag = True
                            self.scene.battleBox.state = BattleSettings.stateMove
                            self.scene.battleBox.pressCD = BattleSettings.pressCD
                    elif self.scene.battleBox.pokeCaptureCnt >= 3 and self.scene.battleBox.ableToRandom == True:    # catching successed
                        self.scene.battleBox.captureFlag = True
                        if keys[pygame.K_RETURN] and self.scene.battleBox.pressCD == 0:
                            player.add_pokemon(self.scene.battleBox.enePokemon)
                            self.scene.battleBox.ballAnimation = False
                            self.scene.battleBox.usePokeBallFlag = False
                            self.scene.battleBox.captureFlag = False
                            self.scene.battleBox.determin = True
                            self.scene.battleBox.pokeCaptureCnt = 0
                            self.scene.battleBox.isFinished = True
                else:   # bag subslection
                    if keys[pygame.K_w]:
                        self.scene.battleBox.bagSelectID = max(0, self.scene.battleBox.bagSelectID - 1)
                        self.scene.battleBox.bagSelectCD = BattleSettings.bagSelectCD
                    if keys[pygame.K_s]:
                        self.scene.battleBox.bagSelectID = min(2, self.scene.battleBox.bagSelectID + 1)
                        self.scene.battleBox.bagSelectCD = BattleSettings.bagSelectCD
                    if keys[pygame.K_f]:
                        if self.scene.battleBox.bagSelectID == 2:
                            self.scene.battleBox.state = BattleSettings.stateAct
                            self.scene.battleBox.bagSelectID = 0
                        if self.scene.battleBox.bagSelectID == ItemID.posion and player.bag[ItemID.posion] > 0:
                            self.scene.battleBox.usePosionFlag = True
                            self.scene.battleBox.pokeSelectID = 0
                        if self.scene.battleBox.canCaptureFlag == True:
                            self.scene.battleBox.canCaptureFlag = False
                        elif self.scene.battleBox.bagSelectID == ItemID.pokeBall and player.bag[ItemID.pokeBall] > 0:
                            if player.encounter == True:
                                if player.pokemonNum >= 6:
                                    self.scene.battleBox.canCaptureFlag = True
                                else:
                                    self.scene.battleBox.usePokeBallFlag = True
                                    player.bag[ItemID.pokeBall] -= 1
                        self.scene.battleBox.pressCD = BattleSettings.pressCD

        if self.scene.battleBox.state == BattleSettings.statePoke: # exchange two Pokemons while battling
            if self.scene.battleBox.pokeSelectCD == 0 and self.scene.battleBox.pressCD == 0:
                if keys[pygame.K_w]:
                    self.scene.battleBox.pokeSelectID = max(1, self.scene.battleBox.pokeSelectID - 1)
                    self.scene.battleBox.pokeSelectCD = BattleSettings.pokeSelectCD
                if keys[pygame.K_s]:
                    self.scene.battleBox.pokeSelectID = min(6, self.scene.battleBox.pokeSelectID + 1)
                    self.scene.battleBox.pokeSelectCD = BattleSettings.pokeSelectCD
                if keys[pygame.K_f]:
                    if self.scene.battleBox.pokeSelectID == 6:
                        if not self.scene.battleBox.defeated:
                            self.scene.battleBox.state = BattleSettings.stateAct
                    elif player.pokemons[self.scene.battleBox.pokeSelectID] is not None and player.pokemons[self.scene.battleBox.pokeSelectID].HP > 0:
                        tempPokemon = player.pokemons[0]
                        player.pokemons[0] = player.pokemons[self.scene.battleBox.pokeSelectID]
                        player.pokemons[self.scene.battleBox.pokeSelectID] = tempPokemon

                        if self.scene.battleBox.defeated:
                            self.scene.battleBox.attacker = self.scene.battle.attacker(player.pokemons[0], self.scene.battleBox.enePokemon)
                            self.scene.battleBox.cnt = 0
                            self.scene.battleBox.direction = 1 - self.scene.battleBox.attacker * 2
                            self.scene.battleBox.defeated = False
                        self.scene.battleBox.moveSelectID = 0
                        self.scene.battleBox.changeFlag = True
                        self.scene.battleBox.skipFlag = True
                        self.scene.battleBox.frePokemon = player.pokemons[0]
                        self.scene.battleBox.freStat = player.pokemons[0].get_battle_info()
                        self.scene.battleBox.frePokemonImg = pygame.transform.scale(player.pokemons[0].frontImage,
                                                                    (BattleSettings.playerWidth, BattleSettings.playerHeight))
                        self.scene.battleBox.state = BattleSettings.stateMove
                    self.scene.battleBox.pressCD = BattleSettings.pressCD

        if self.scene.battleBox.state == BattleSettings.stateEscape:    # choose to escape
            if player.encounter == True:    # can only escape when encounter wild Pokemon
                self.scene.battleBox.isFinished = True
            else:
                if keys[pygame.K_f] and self.scene.battleBox.pressCD == 0:
                    self.scene.battleBox.state = BattleSettings.stateAct
                    self.scene.battleBox.pressCD = BattleSettings.pressCD

        if self.scene.battleBox.isFinished == True and keys[pygame.K_RETURN]:   # battle finished
            if self.scene.battleWith is not None:
                self.scene.battleWith.ableToBattle = False
                for pokemon in self.scene.battleWith.pokemons:
                    if pokemon is not None:
                        if pokemon.HP > 0:
                            self.scene.battleWith.ableToBattle = True
                if not self.scene.battleWith.ableToBattle:
                    self.scene.battleWith.speed = 0
                self.scene.battleWith.battling = False
                self.scene.battleWith = None
            if self.scene.battleBox.beat == True:   # player beat enemy
                for ID in range(6):
                    if player.pokemons[ID] is not None:
                        player.pokemons[ID].expUp(self.scene.battleBox.exp[ID])
                if self.scene.battleBox.npcTrainer is not None:
                    player.money += 3000
                    if self.scene.battleBox.npcTrainer.BOSSFlag:    # if defeat the BOSS
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_ENDGAME))  # event queue
                else:
                    player.money += 1000
                self.scene.battleBox.beat = False
                self.scene.battleBox.exp = []
            if self.scene.battleBox.defeatAll == True:
                player.money //= 2
                self.scene.battleBox.defeatAll = False
                player.battleFailCD = BattleSettings.battleCD

            self.scene.battleBox.state = BattleSettings.stateAct
            self.scene.battleBox.moveSelectCD = 0
            self.scene.battleBox.actSelectCD = 0
            self.scene.battleBox = None
            player.battling = False
            player.encounter = False
            player.encounterCD = BattleSettings.encounterCD
            self.battleFlag = False
            
            self.bgm.update(self.scene.state)
            

    def triggers(self, player:Player.Player, keys):
        self.talking_trigger(player, keys)
        self.shopping_trigger(player, keys)
        self.submenu_trigger(player, keys)
        self.battle_trigger(player, keys)

    def events(self, player:Player.Player, keys):
        if self.talkingFlag == True:
            self.event_talking(player, keys)
        if self.shoppingFlag == True:
            self.event_shopping(player, keys)
        if self.subMenuFlag == True:
            self.event_submenu(player, keys)
        if self.battleFlag == True:
            self.event_battle(player, keys)

    def event_queue(self, player:Player.Player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.state == GameState.MAIN_MENU:
                    self.flush_scene(GameState.GAME_PLAY_ORIGIN, player, 0, 0)
                if event.key == pygame.K_ESCAPE and self.state == GameState.MAIN_MENU:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_RETURN and self.state == GameState.END_GAME:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == GameState.GAME_PLAY_ORIGIN:
                    self.flush_scene(GameState.GAME_PLAY_CITY, player, 0, 0)
                if event.key == pygame.K_ESCAPE and self.state == GameState.GAME_PLAY_ORIGIN:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

            # triggers
            if event.type == GameEvent.EVENT_DIALOG:
                self.talkingFlag = True
            if event.type == GameEvent.EVENT_SHOP:
                self.shoppingFlag = True
            if event.type == GameEvent.EVENT_SUBMENU:
                self.subMenuFlag = True
            if event.type == GameEvent.EVENT_BATTLE:
                self.bgm.update(GameState.GAME_PLAY_BOSS)
                self.battleFlag = True
            if event.type == GameEvent.EVENT_SWITCH:    # switch scene
                if player.GOTO == GameState.GAME_PLAY_HOSPITAL:
                    self.flush_scene(GameState.GAME_PLAY_HOSPITAL, player, 0, 0)
                if player.GOTO == GameState.GAME_PLAY_CITY:
                    self.flush_scene(GameState.GAME_PLAY_CITY, player, player.xspawn, player.yspawn)
                if player.GOTO == GameState.GAME_PLAY_GYM:
                    self.flush_scene(GameState.GAME_PLAY_GYM, player, 0, 0)
                if player.GOTO == GameState.GAME_PLAY_WILD:
                    self.flush_scene(GameState.GAME_PLAY_WILD, player, player.xspawn, player.yspawn)
                if player.GOTO == GameState.GAME_PLAY_SHOP:
                    self.flush_scene(GameState.GAME_PLAY_SHOP, player, 0, 0)
                player.spawn()
            if event.type == GameEvent.EVENT_ENDGAME:   # end game
                self.flush_scene(GameState.END_GAME, player, 0, 0)

    def flush_scene(self, GOTO:GameState, player:Player.Player, Initial_X, Initial_Y):  # switch scene
        if GOTO == GameState.GAME_PLAY_ORIGIN:
            self.scene = Scene.OriginScene(self.window, Initial_X, Initial_Y)
        else:
            if GOTO == GameState.GAME_PLAY_CITY:
                self.scene = Scene.CityScene(self.window, Initial_X, Initial_Y)
            if GOTO == GameState.GAME_PLAY_GYM:
                self.scene = Scene.GymScene(self.window, Initial_X, Initial_Y)
            if GOTO == GameState.GAME_PLAY_HOSPITAL:
                self.scene = Scene.HospitalScene(self.window, 0, 0)
            if GOTO == GameState.GAME_PLAY_WILD:
                self.scene = Scene.WildScene(self.window, 0, 0)
            if GOTO == GameState.GAME_PLAY_SHOP:
                self.scene = Scene.ShopScene(self.window, 0, 0)
            if GOTO == GameState.END_GAME:
                self.scene = Scene.EndGameScene(self.window, 0, 0)
            self.bgm.update(GOTO)
            player.colliSys = Attributes.Collidable(self.scene)
        self.state = GOTO

    def update_camera(self, player:Player.Player):  # fix the player to the middle
        if player.rect.x > WindowSettings.width // 2:
            self.scene.cameraX += player.speed
            if self.scene.cameraX <= self.get_width() - WindowSettings.width:
                player.fix_middle(player.speed, 0)
            else:
                self.scene.cameraX = self.get_width() - WindowSettings.width
        if player.rect.x < WindowSettings.width // 2:
            self.scene.cameraX -= player.speed
            if self.scene.cameraX >= 0:
                player.fix_middle(-player.speed, 0)
            else:
                self.scene.cameraX = 0
        if player.rect.y > WindowSettings.height // 2:
            self.scene.cameraY += player.speed
            if self.scene.cameraY <= self.get_height() - WindowSettings.height:
                player.fix_middle(0, player.speed)
            else:
                self.scene.cameraY = self.get_height() - WindowSettings.height
        if player.rect.y < WindowSettings.height // 2:
            self.scene.cameraY -= player.speed
            if self.scene.cameraY >= 0:
                player.fix_middle(0, -player.speed)
            else:
                self.scene.cameraY = 0

    def update_npc(self):
        for npc in self.scene.npcsNormal:
            npc.update(self.scene.cameraX, self.scene.cameraY)
        for npc in self.scene.npcsTrader:
            npc.update(self.scene.cameraX, self.scene.cameraY)
        for npc in self.scene.npcsTrainer:
            npc.update(self.scene.cameraX, self.scene.cameraY)
    def update_obstacle(self):
        if self.scene.obstacles is not None:
            for obstacle in self.scene.obstacles:
                obstacle.update(self.scene.cameraX, self.scene.cameraY)
    def update_hospital(self):
        if self.scene.hospital is not None:
            for hospital in self.scene.hospital:
                hospital.update(self.scene.cameraX, self.scene.cameraY)
    def update_gym(self):
        if self.scene.gym is not None:
            for gym in self.scene.gym:
                gym.update(self.scene.cameraX, self.scene.cameraY)
    def update_shop(self):
        if self.scene.shop is not None:
            for shop in self.scene.shop:
                shop.update(self.scene.cameraX, self.scene.cameraY)
    def update_citystation(self):
        if self.scene.citystation is not None:
            for citystation in self.scene.citystation:
                citystation.update(self.scene.cameraX, self.scene.cameraY)
    def update_wildstation(self):
        if self.scene.wildstation is not None:
            for wildstation in self.scene.wildstation:
                wildstation.update(self.scene.cameraX, self.scene.cameraY)
    def update_gymbg(self):
        if self.scene.background is not None:
            for bg in self.scene.background:
                bg.update(self.scene.cameraX, self.scene.cameraY)
    def update_walls(self):
        if self.scene.walls is not None:
            for wall in self.scene.walls:
                wall.update(self.scene.cameraX, self.scene.cameraY)
    def update_doors(self):
        if self.scene.doors is not None:
            for door in self.scene.doors:
                door.update(self.scene.cameraX, self.scene.cameraY)
    def update_stones(self):
        if self.scene.stones is not None:
            for stone in self.scene.stones:
                stone.update(self.scene.cameraX, self.scene.cameraY)
    def update_grass(self):
        if self.scene.grasses is not None:
            for grass in self.scene.grasses:
                grass.update(self.scene.cameraX, self.scene.cameraY)
    def update_portal(self):
        if self.scene.portal is not None:        
            for portal in self.scene.portal:
                portal.update(self.scene.cameraX, self.scene.cameraY)

    # update every object with the camera that fixes the player to the midle
    def update(self, player:Player.Player):
        self.update_camera(player)
        self.update_npc()
        self.update_obstacle()
        self.update_grass()
        self.update_hospital()
        self.update_portal()
        self.update_gym()
        self.update_shop()
        self.update_citystation()
        self.update_wildstation()
        self.update_gymbg()
        self.update_walls()
        self.update_doors()
        self.update_stones()
        self.update_portal()

    def render(self):
        self.scene.render()