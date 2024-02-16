# -*- coding:utf-8 -*-

import pygame
import random
import copy

from GameLogic import *
from Design import *
from Settings import *
from Items import *


class Scene:
    def __init__(self, window) -> None:
        self.window = window
        self.type = ""

    def draw_block(self, x, y, width, height, color):
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, color, (0, 0, width, height))
        self.window.blit(rect_surface, (x, y))

    def draw_text(self, text, x, y, fontColor, fontSize, fontType):
        font = pygame.font.Font(fontType, fontSize)
        surface = font.render(text, True, fontColor)
        self.window.blit(surface, (x, y))

    def tap(self):
        pass

    def render(self):
        pass


class MainMap(Scene):
    def __init__(self, window, areaID, player) -> None:
        pygame.mixer.music.load(Music.map[areaID])
        pygame.mixer.music.set_volume(Music.volume[areaID])
        pygame.mixer.music.play(-1)

        self.mainmapType = 0
        self.obstacles = []  # 这个要录入地图文件的时候一并录入
        self.enemyList = []  # 这个要录入地图文件的时候一并录入
        self.npcList = []  # 这个要录入地图文件的时候一并录入

        self.type = "map"
        self.window = window
        self.areaID = areaID
        self.music = Music.map[areaID]
        self.items = {}
        # 树
        self.items["Tree"] = pygame.sprite.Group()
        tree = pygame.image.load(MapPath.treeOnGround)
        tree = pygame.transform.scale(
            tree, (MapSettings.treeWidth, MapSettings.treeHeight))
        for i in range(MapSettings.groundYnum):
            for j in range(MapSettings.groundXnum):
                if BushGrassFlowerTreeMatrix.map[self.areaID][i][j] == 4:
                    self.items["Tree"].add(Trees(
                        tree, MapSettings.square * j, MapSettings.square * i - MapSettings.treeDeltaY))
        # 各种地砖
        self.items["Ground"] = pygame.sprite.Group()
        groundImg = [0] + [pygame.transform.scale(pygame.image.load(imgPath), (MapSettings.ground, MapSettings.ground))
                           for imgPath in MapPath.ground[1:]]
        for i in range(MapSettings.groundYnum):
            for j in range(MapSettings.groundXnum):
                if GroundMatrix.map[self.areaID][i][j] != 0:
                    self.items["Ground"].add(Grounds(
                        groundImg[GroundMatrix.map[self.areaID][i][j]], MapSettings.ground * j, MapSettings.ground * i))
        # bush
        self.items["Bush"] = pygame.sprite.Group()
        bush = pygame.transform.scale(pygame.image.load(
            MapPath.bush), (MapSettings.square, MapSettings.square))
        for i in range(MapSettings.groundYnum):
            for j in range(MapSettings.groundXnum):
                if BushGrassFlowerTreeMatrix.map[self.areaID][i][j] == 1:
                    self.items["Bush"].add(
                        Bushes(bush, MapSettings.square * j, MapSettings.square * i))
        # grass
        self.items["Grass"] = pygame.sprite.Group()
        grass = pygame.transform.scale(pygame.image.load(
            MapPath.grass), (MapSettings.square, MapSettings.square))
        for i in range(MapSettings.groundYnum):
            for j in range(MapSettings.groundXnum):
                if BushGrassFlowerTreeMatrix.map[self.areaID][i][j] == 2:
                    self.items["Grass"].add(
                        Grasses(grass, MapSettings.square * j, MapSettings.square * i))
        # flower
        self.items["Flower"] = pygame.sprite.Group()
        flower = pygame.transform.scale(pygame.image.load(
            MapPath.flower), (MapSettings.square, MapSettings.square))
        for i in range(MapSettings.groundYnum):
            for j in range(MapSettings.groundXnum):
                if BushGrassFlowerTreeMatrix.map[self.areaID][i][j] == 3:
                    self.items["Flower"].add(
                        Flowers(flower, MapSettings.square * j, MapSettings.square * i))

        # board
        self.items["Board"] = pygame.sprite.Group()
        for boardID in BoardDetail.map:
            if BoardDetail.map[boardID]["area"] == self.areaID:
                sur_scale = BoardDetail.map[boardID]["sur_scale"]
                surface = pygame.transform.scale(pygame.image.load(
                    BoardDetail.map[boardID]["surface"]), sur_scale)
                self.items["Board"].add(Boards(surface,
                                               MapSettings.square *
                                               BoardDetail.map[boardID]["x"] + (
                                                   MapSettings.square - sur_scale[0]) // 2,
                                               MapSettings.square *
                                               (BoardDetail.map[boardID]
                                                ["y"] + 1) - sur_scale[1],
                                               boardID))

        # bell
        self.items["Bell"] = pygame.sprite.Group()
        bellImg = pygame.transform.scale(
            pygame.image.load(BellSettings.img), BellSettings.scale)
        for bellID in BellDetail.map:
            if BellDetail.map[bellID]["area"] == self.areaID:
                self.items["Bell"].add(Bells(bellImg,
                                             MapSettings.square *
                                             BellDetail.map[bellID]["x"],
                                             MapSettings.square *
                                             BellDetail.map[bellID]["y"],
                                             bellID))

        # special things
        self.items["Special"] = pygame.sprite.Group()
        for specialID in SpecialDetail.map:
            if SpecialDetail.map[specialID]["area"] == self.areaID:
                width, height, rect_height, rect_width = \
                    SpecialDetail.map[specialID]["width"], SpecialDetail.map[specialID]["height"],\
                    SpecialDetail.map[specialID]["rect_height"], SpecialDetail.map[specialID]["rect_width"]
                self.items["Special"].add(Specials(pygame.transform.scale(pygame.image.load(SpecialDetail.map[specialID]["img"]), (width, height)),
                                                   MapSettings.square *
                                                   SpecialDetail.map[specialID]["x"],
                                                   MapSettings.square *
                                                   SpecialDetail.map[specialID]["y"],
                                                   width, height, rect_width, rect_height))

        # shop
        self.items["Shop"] = pygame.sprite.Group()
        for shopID in ShopDetail.map:
            if ShopDetail.map[shopID]["area"] == self.areaID:
                width, height = FigureSettings.width, FigureSettings.height
                self.items["Shop"].add(Shops(pygame.transform.scale(pygame.image.load(ShopDetail.map[shopID]["surface"]), (width, height)),
                                             MapSettings.square *
                                             ShopDetail.map[shopID]["x"],
                                             MapSettings.square *
                                             ShopDetail.map[shopID]["y"],
                                             shopID))

        # enemy
        self.items["Enemy"] = pygame.sprite.Group()
        for enemyID in EnemyDetail.map:
            enemy = EnemyDetail.map[enemyID]
            heve_been_beaten = player.info.get_info("enemy")
            if enemy["area"] == self.areaID and enemyID not in heve_been_beaten:
                width, height = FigureSettings.width, FigureSettings.height
                self.items["Enemy"].add(Enemies(pygame.transform.scale(pygame.image.load(enemy["surface"]), (width, height)),
                                                MapSettings.square *
                                                enemy["x"],
                                                MapSettings.square *
                                                enemy["y"] - (FigureSettings.height -
                                                              MapSettings.square),
                                                enemyID))

    def render(self):
        drawLayer = [[], [], []]
        for entry in self.items:
            for item in self.items[entry]:
                drawLayer[item.layer].append(item)
        return drawLayer


class Command(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.text = ""
        self.type = "command"

    def tap(self, event):
        if event.key == pygame.K_RETURN:
            if self.text != "":
                word = self.text.split()
                self.text = ""
                return word
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            if len(self.text) > CommandSettings.textLimit:
                return []
            char = event.unicode
            if char.isupper() or char.islower() or char.isdigit() or char == '-' or char == ' ' or char == '=' or char == '_':
                self.text += char
        return []

    def render(self):
        # render block
        self.draw_block(CommandSettings.blockX, CommandSettings.blockY,
                        CommandSettings.blockWidth, CommandSettings.blockHeight, CommandSettings.blockColor)

        self.draw_text("> " + self.text + '|', CommandSettings.wordX, CommandSettings.wordY,
                       CommandSettings.wordColor, CommandSettings.wordSize, BasicSettings.fontPathLucida)


class Menu(Scene):
    def __init__(self, window) -> None:
        super().__init__(window)
        self.catergory = 0
        self.leftHand = True
        self.rightChooseR = 0
        self.rightChooseC = 0
        self.deep = 0
        self.LRSkill = 0

    def tap(self, event, player):
        if self.leftHand:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                cats = player.info.get_info("cat")
                skills = player.info.get_info("skill")
                if self.catergory == 1 and len(cats) != 0 or self.catergory == 2 and len(skills) != 0 or self.catergory == 3:
                    self.leftHand = False
                    self.deep = 0
                    self.rightChooseR = 0
                    self.rightChooseC = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.catergory > 0:
                    self.catergory -= 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.catergory < len(MenuSettings.catergory) - 1:
                    self.catergory += 1
        else:
            if self.catergory == 0 or self.catergory == 2 and self.deep == 1:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.leftHand = True
                    self.deep = 0
            elif self.catergory == 1:
                if self.deep == 0:
                    cats = player.info.get_info("cat")
                    cats = [cats[i: i + MenuSettings.catPreviewRowLimit]
                            for i in range(0, len(cats), MenuSettings.catPreviewRowLimit)]
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.rightChooseC == 0:
                            self.leftHand = True
                            self.deep = 0
                        else:
                            self.rightChooseC -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if len(cats) > 0 and self.rightChooseC < len(cats[self.rightChooseR]) - 1:
                            self.rightChooseC += 1
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.rightChooseR > 0:
                            self.rightChooseR -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.rightChooseR < len(cats) - 1:
                            self.rightChooseR += 1
                    elif event.key == pygame.K_RETURN:
                        self.deep = 1
                        self.cat = cats[self.rightChooseR][self.rightChooseC]
                        self.rightChooseC = 0
                        self.rightChooseR = 0
                elif self.deep == 1:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.rightChooseC == 0:
                            self.leftHand = True
                            self.deep = 0
                        else:
                            self.rightChooseC -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.rightChooseC < 1:
                            self.rightChooseC += 1
                    elif event.key == pygame.K_RETURN:
                        AllSkill = player.info.get_info("skill")
                        if len(AllSkill) != 0:
                            self.deep = 2
                            all_cats_skills = player.info.get_info("skillUse")
                            cat_skill = all_cats_skills[self.cat] if self.cat in all_cats_skills else (
                                "", "")
                            self.skill = cat_skill[self.rightChooseC]
                            self.LRSkill = self.rightChooseC
                            self.rightChooseC = 0
                            self.rightChooseR = 0
                elif self.deep == 2:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.leftHand = True
                        self.deep = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.rightChooseR > 0:
                            self.rightChooseR -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        AllSkill = player.info.get_info("skill")
                        if self.rightChooseR < len(AllSkill) - 1:
                            self.rightChooseR += 1
                    elif event.key == pygame.K_RETURN:
                        AllSkill = player.info.get_info("skill")
                        chooseSkill = AllSkill[self.rightChooseR]
                        all_cats_skills = player.info.get_info("skillUse")
                        for cat in all_cats_skills:
                            catSkill = all_cats_skills[cat]
                            for i in range(2):
                                if catSkill[i] == chooseSkill:
                                    all_cats_skills[cat][i] = ""

                        all_cats_skills[self.cat][self.LRSkill] = chooseSkill
                        player.info.modify("skillUse", all_cats_skills)
                        player.save()
                        self.deep = 1
                        self.rightChooseC = 0
                        self.rightChooseR = 0
            elif self.catergory == 2:
                skills = player.info.get_info("skill")
                skills = [skills[i: i + MenuSettings.skillPreviewRowLimit]
                          for i in range(0, len(skills), MenuSettings.skillPreviewRowLimit)]
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.rightChooseC == 0:
                        self.leftHand = True
                        self.deep = 0
                    else:
                        self.rightChooseC -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if len(skills) > 0 and self.rightChooseC < len(skills[self.rightChooseR]) - 1:
                        self.rightChooseC += 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.rightChooseR > 0:
                        self.rightChooseR -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.rightChooseR < len(skills) - 1:
                        self.rightChooseR += 1
                elif event.key == pygame.K_RETURN:
                    self.deep = 1
            elif self.catergory == 3:
                if self.deep == 0:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.rightChooseC == 0:
                            self.leftHand = True
                            self.deep = 0
                        else:
                            self.rightChooseC -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.rightChooseC < 3:
                            self.rightChooseC += 1
                    elif event.key == pygame.K_RETURN:
                        self.deep = 1
                        self.position = self.rightChooseC
                        self.rightChooseC = 0
                        self.rightChooseR = 0
                elif self.deep == 1:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.deep = 0
                        self.leftHand = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.rightChooseR > 0:
                            self.rightChooseR -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        AllCat = player.info.get_info("cat")
                        if self.rightChooseR < len(AllCat) - 1:
                            self.rightChooseR += 1
                    elif event.key == pygame.K_RETURN:
                        unit = player.info.get_info("unit")
                        AllCat = player.info.get_info("cat")
                        if len(AllCat) != 0:
                            chooseCat = AllCat[self.rightChooseR]
                            for i in range(4):
                                if unit[i] == chooseCat:
                                    unit[i] = None
                            unit[self.position] = chooseCat
                            player.info.modify("unit", unit)
                            player.save()
                            self.deep = 0
                            self.rightChooseC = 0
                            self.rightChooseR = 0
        if event.key == pygame.K_ESCAPE:
            player.info.modify("state", 0)
        return player

    def draw_row(self, text, x, fontColor, fontSize, fontType, currentY, deltaY):
        self.draw_text(text, x, currentY, fontColor, fontSize, fontType)
        return currentY + deltaY

    def render(self, player):
        self.draw_block(MenuSettings.bgX, MenuSettings.bgY,
                        MenuSettings.bgWidth, MenuSettings.bgHeight, MenuSettings.bgColor)
        self.draw_block(MenuSettings.lbgX, MenuSettings.lbgY,
                        MenuSettings.lbgWidth, MenuSettings.lbgHeight, MenuSettings.lbgColor)

        if self.leftHand:
            self.draw_block(MenuSettings.leftChooseBlockX, MenuSettings.leftChooseBlockY + MenuSettings.catergoryDeltaY * self.catergory,
                            MenuSettings.leftChooseBlockWidth, MenuSettings.leftChooseBlockHeight, MenuSettings.leftChooseBlockColor)

        for i in range(len(MenuSettings.catergory)):
            entry = MenuSettings.catergory[i]
            self.draw_text(entry, MenuSettings.catergoryX, MenuSettings.catergoryY + MenuSettings.catergoryDeltaY * i,
                           MenuSettings.catergoryColor2 if self.leftHand and self.catergory == i else MenuSettings.catergoryColor,
                           MenuSettings.catergorySize, MenuSettings.catergoryFont)

        if self.catergory == 0:
            nowY = MenuSettings.profileY
            nowY = self.draw_row("昵称: " + player.info.get_info("nickname"), MenuSettings.titleX,
                                 MenuSettings.titleColor, MenuSettings.titleSize, MenuSettings.titleFont,
                                 nowY, MenuSettings.titleDeltaY)
            nowY = self.draw_row("当前地图: " + MapInfo.detail["name"][player.info.get_info("area")], MenuSettings.titleX,
                                 MenuSettings.titleColor, MenuSettings.titleSize, MenuSettings.titleFont,
                                 nowY, MenuSettings.titleDeltaY)
            nowY = self.draw_row("金币: " + str(player.info.get_info("money")), MenuSettings.titleX,
                                 MenuSettings.titleColor, MenuSettings.titleSize, MenuSettings.titleFont,
                                 nowY, MenuSettings.titleDeltaY)
            nowY = self.draw_row("属性加成: ", MenuSettings.titleX,
                                 MenuSettings.titleColor, MenuSettings.titleSize, MenuSettings.titleFont,
                                 nowY, MenuSettings.titleDeltaY)
            nowY = self.draw_row("生命值: " + str(player.info.get_info("hp")), MenuSettings.subtitleX,
                                 MenuSettings.subtitleColor, MenuSettings.subtitleSize, MenuSettings.subtitleFont,
                                 nowY, MenuSettings.subtitleDeltaY)
            nowY = self.draw_row("攻击力: " + str(player.info.get_info("atk")), MenuSettings.subtitleX,
                                 MenuSettings.subtitleColor, MenuSettings.subtitleSize, MenuSettings.subtitleFont,
                                 nowY, MenuSettings.subtitleDeltaY)
            nowY = self.draw_row("防御力: " + str(player.info.get_info("def")), MenuSettings.subtitleX,
                                 MenuSettings.subtitleColor, MenuSettings.subtitleSize, MenuSettings.subtitleFont,
                                 nowY, MenuSettings.subtitleDeltaY)
            nowY = self.draw_row("金币获取率: " + str(player.info.get_info("gold")) + "%", MenuSettings.subtitleX,
                                 MenuSettings.subtitleColor, MenuSettings.subtitleSize, MenuSettings.subtitleFont,
                                 nowY, MenuSettings.subtitleDeltaY)

        elif self.catergory == 1:
            cats = player.info.get_info("cat")
            if len(cats) == 0:
                return
            cats = [cats[i: i + MenuSettings.catPreviewRowLimit]
                    for i in range(0, len(cats), MenuSettings.catPreviewRowLimit)]
            if self.deep == 0:
                if self.leftHand == False:
                    self.draw_block(MenuSettings.catPreviewX + self.rightChooseC * MenuSettings.catPreviewDeltaX - MenuSettings.catPreviewBlockDelta,
                                    MenuSettings.catPreviewY + self.rightChooseR *
                                    MenuSettings.catPreviewDeltaY - MenuSettings.catPreviewBlockDelta,
                                    MenuSettings.catPreviewBlockSize, MenuSettings.catPreviewBlockSize,
                                    MenuSettings.catPreviewBlockColor)

                for i in range(len(cats)):
                    nowX, nowY = MenuSettings.catPreviewX, MenuSettings.catPreviewY + \
                        MenuSettings.catPreviewDeltaY * i
                    for cat in cats[i]:
                        img = pygame.transform.scale(
                            pygame.image.load(CatCake.es[cat]["preview"]),
                            (MenuSettings.catPreviewSize,
                             MenuSettings.catPreviewSize)
                        )
                        self.window.blit(img, (nowX, nowY))
                        self.draw_text(CatCake.es[cat]["name"],
                                       nowX + MenuSettings.catPreviewSize // 2 -
                                       len(CatCake.es[cat]["name"]) *
                                       MenuSettings.catPreviewNameSize // 2,
                                       nowY + MenuSettings.catPreviewNameDistance,
                                       MenuSettings.catPreviewNameColor, MenuSettings.catPreviewNameSize, MenuSettings.catPreviewNameFont)
                        nowX += MenuSettings.catPreviewDeltaX
            elif self.deep == 1:
                cat = self.cat
                img = pygame.transform.scale(
                    pygame.image.load(CatCake.es[cat]["preview"]),
                    (MenuSettings.catWidth, MenuSettings.catHeight)
                )
                self.window.blit(img, (MenuSettings.catX, MenuSettings.catY))

                nowY = MenuSettings.catDetailY
                nowY = self.draw_row("名称: " + CatCake.es[cat]["name"], MenuSettings.catDetailX,
                                     MenuSettings.titleColor, MenuSettings.catTitleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.catTitleDeltaY)
                text = ""
                for flavor in CatCake.es[cat]["flavor"]:
                    text += flavor.value[1] + ("，" if flavor !=
                                               CatCake.es[cat]["flavor"][-1] else "")
                nowY = self.draw_row("口味: " + text, MenuSettings.catDetailX,
                                     MenuSettings.titleColor, MenuSettings.catTitleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.catTitleDeltaY)
                nowY = self.draw_row("数值: ", MenuSettings.catDetailX,
                                     MenuSettings.titleColor, MenuSettings.catTitleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.catTitleSize - MenuSettings.catSubTitleSize)
                nowY = self.draw_row("生命值: " + str(CatCake.es[cat]["hp"]), MenuSettings.catNumX,
                                     MenuSettings.titleColor, MenuSettings.catSubTitleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.catSubTitleDeltaY)
                nowY = self.draw_row("攻击力: " + str(CatCake.es[cat]["atk"]), MenuSettings.catNumX,
                                     MenuSettings.titleColor, MenuSettings.catSubTitleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.catSubTitleDeltaY)
                nowY = self.draw_row("防御力: " + str(CatCake.es[cat]["def"]), MenuSettings.catNumX,
                                     MenuSettings.titleColor, MenuSettings.catSubTitleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.catSubTitleDeltaY)
                nowY = self.draw_row("金币获取率: " + str(CatCake.es[cat]["gold"]), MenuSettings.catNumX,
                                     MenuSettings.titleColor, MenuSettings.catSubTitleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.catSubTitleDeltaY)

                self.draw_text("技能：", 380, 402, (255, 255, 255),
                               32, MenuSettings.titleFont)

                self.draw_block(MenuSettings.catSkillPreviewX + self.rightChooseC * MenuSettings.catSkillPreviewDeltaX - MenuSettings.catSkillPreviewBlockDelta,
                                MenuSettings.catSkillPreviewY - MenuSettings.catSkillPreviewBlockDelta,
                                MenuSettings.catSkillPreviewSize + 2 * MenuSettings.catSkillPreviewBlockDelta,
                                MenuSettings.catSkillPreviewSize + 2 * MenuSettings.catSkillPreviewBlockDelta,
                                MenuSettings.catSkillPreviewBlockColor)

                all_cats_skills = player.info.get_info("skillUse")
                cat_skill = all_cats_skills[cat] if cat in all_cats_skills else [
                    "", ""]
                for i in range(2):
                    if cat_skill[i] == "":
                        self.draw_block(MenuSettings.catSkillPreviewX + i * MenuSettings.catSkillPreviewDeltaX, MenuSettings.catSkillPreviewY,
                                        MenuSettings.catSkillPreviewSize, MenuSettings.catSkillPreviewSize,
                                        MenuSettings.catSkillPreviewNoneColor)
                    else:
                        img = pygame.transform.scale(
                            pygame.image.load(
                                Skills.es[cat_skill[i]]["preview"]),
                            (MenuSettings.catSkillPreviewSize,
                             MenuSettings.catSkillPreviewSize)
                        )
                        self.window.blit(img, (MenuSettings.catSkillPreviewX + i *
                                         MenuSettings.catSkillPreviewDeltaX, MenuSettings.catSkillPreviewY))
                all_cats_skills[cat] = cat_skill
                player.info.modify("skillUse", all_cats_skills)
                player.save()
            elif self.deep == 2:
                self.draw_text(
                    "选择要替换成的技能：", 280, 53, MenuSettings.titleColor, 40, MenuSettings.titleFont)

                self.draw_block(MenuSettings.replaceSkillBlockX, MenuSettings.replaceSkillBlockY + self.rightChooseR * MenuSettings.replaceSkillDeltaY,
                                MenuSettings.replaceSkillBlockWidth, MenuSettings.replaceSkillBlockHeight, MenuSettings.replaceSkillBlockColor)

                all_cats_skills = player.info.get_info("skillUse")
                AllSkill = player.info.get_info("skill")
                count = 0
                for skill in AllSkill:
                    img = pygame.transform.scale(
                        pygame.image.load(Skills.es[skill]["preview"]),
                        (MenuSettings.replaceSkillSize,
                         MenuSettings.replaceSkillSize)
                    )
                    self.window.blit(img, (MenuSettings.replaceSkillX,
                                     MenuSettings.replaceSkillY + count * MenuSettings.replaceSkillDeltaY))
                    self.draw_text(Skills.es[skill]["id"], MenuSettings.replaceSkillIDX,
                                   MenuSettings.replaceSkillY + count * MenuSettings.replaceSkillDeltaY +
                                   MenuSettings.replaceSkillTextDownShift,
                                   MenuSettings.replaceSkillTextColor, MenuSettings.replaceSkillTextSize, MenuSettings.replaceSkillTextFont)
                    self.draw_text(Skills.es[skill]["short_des"], MenuSettings.replaceSkillDescriptionX,
                                   MenuSettings.replaceSkillY + count * MenuSettings.replaceSkillDeltaY +
                                   MenuSettings.replaceSkillTextDownShift,
                                   MenuSettings.replaceSkillTextColor, MenuSettings.replaceSkillTextSize, MenuSettings.replaceSkillTextFont)
                    count += 1

        elif self.catergory == 2:
            skills = player.info.get_info("skill")
            if len(skills) == 0:
                return
            skills = [skills[i: i + MenuSettings.skillPreviewRowLimit]
                      for i in range(0, len(skills), MenuSettings.skillPreviewRowLimit)]
            if self.deep == 0:
                if self.leftHand == False:
                    self.draw_block(MenuSettings.skillPreviewX + self.rightChooseC * MenuSettings.skillPreviewDeltaX - MenuSettings.skillPreviewBlockDelta,
                                    MenuSettings.skillPreviewY + self.rightChooseR *
                                    MenuSettings.skillPreviewDeltaY - MenuSettings.skillPreviewBlockDelta,
                                    MenuSettings.skillPreviewBlockSize, MenuSettings.skillPreviewBlockSize,
                                    MenuSettings.skillPreviewBlockColor)

                for i in range(len(skills)):
                    nowX, nowY = MenuSettings.skillPreviewX, MenuSettings.skillPreviewY + \
                        MenuSettings.skillPreviewDeltaY * i
                    for skill in skills[i]:
                        img = pygame.transform.scale(
                            pygame.image.load(Skills.es[skill]["preview"]),
                            (MenuSettings.skillPreviewSize,
                             MenuSettings.skillPreviewSize)
                        )
                        self.window.blit(img, (nowX, nowY))
                        self.draw_text(Skills.es[skill]["name"],
                                       nowX + MenuSettings.skillPreviewSize // 2 -
                                       len(Skills.es[skill]["name"]) *
                                       MenuSettings.skillPreviewNameSize // 2,
                                       nowY + MenuSettings.skillPreviewNameDistance,
                                       MenuSettings.skillPreviewNameColor, MenuSettings.skillPreviewNameSize, MenuSettings.skillPreviewNameFont)
                        nowX += MenuSettings.skillPreviewDeltaX
            else:
                skill = skills[self.rightChooseR][self.rightChooseC]
                img = pygame.transform.scale(
                    pygame.image.load(Skills.es[skill]["card"]),
                    (MenuSettings.skillWidth, MenuSettings.skillHeight)
                )
                self.window.blit(
                    img, (MenuSettings.skillX, MenuSettings.skillY))

                nowY = MenuSettings.skillDetailY
                nowY = self.draw_row("编号: " + Skills.es[skill]["id"], MenuSettings.skillDetailX,
                                     MenuSettings.titleColor, MenuSettings.titleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.skillDetailDeltaY)
                nowY = self.draw_row("名称: " + Skills.es[skill]["name"], MenuSettings.skillDetailX,
                                     MenuSettings.titleColor, MenuSettings.titleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.skillDetailDeltaY)
                nowY = self.draw_row("技能描述: ", MenuSettings.skillDetailX,
                                     MenuSettings.titleColor, MenuSettings.titleSize, MenuSettings.titleFont,
                                     nowY, MenuSettings.skillDetailDeltaY)

                text = Skills.es[skill]["description"]
                text = [text[i: i + MenuSettings.skillDescriptionLimit]
                        for i in range(0, len(text), MenuSettings.skillDescriptionLimit)]
                for i in range(len(text)):
                    row_text = text[i]
                    nowY = self.draw_row(row_text, MenuSettings.skillDetailX,
                                         MenuSettings.titleColor, MenuSettings.skillDescriptionSize, MenuSettings.titleFont,
                                         nowY, MenuSettings.skillDescriptionRowDistance)

        elif self.catergory == 3:
            if self.deep == 0:
                if self.leftHand == False:
                    self.draw_block(MenuSettings.unitPreviewX + self.rightChooseC * MenuSettings.unitPreviewDeltaX - MenuSettings.unitPreviewChooseDeltaSize / 2,
                                    MenuSettings.unitPreviewY - MenuSettings.unitPreviewChooseDeltaSize / 2,
                                    MenuSettings.unitPreviewSize + MenuSettings.unitPreviewChooseDeltaSize,
                                    MenuSettings.unitPreviewSize + MenuSettings.unitPreviewChooseDeltaSize,
                                    MenuSettings.unitPreviewChooseColor)
                unit = player.info.get_info("unit")
                for i in range(4):
                    self.draw_text(str(i + 1) + "号位", MenuSettings.unitPreviewTextShiftX + MenuSettings.unitPreviewX + i * MenuSettings.unitPreviewDeltaX,
                                   MenuSettings.unitPreviewTextY, MenuSettings.unitPreviewTextColor,
                                   MenuSettings.unitPreviewTextSize, MenuSettings.unitPreviewTextFont)
                    if unit[i] == None:
                        self.draw_block(MenuSettings.unitPreviewX + i * MenuSettings.unitPreviewDeltaX, MenuSettings.unitPreviewY,
                                        MenuSettings.unitPreviewSize, MenuSettings.unitPreviewSize,
                                        MenuSettings.unitPreviewNoneColor)
                    else:
                        img = pygame.transform.scale(
                            pygame.image.load(CatCake.es[unit[i]]["preview"]),
                            (MenuSettings.unitPreviewSize,
                             MenuSettings.unitPreviewSize)
                        )
                        self.window.blit(img, (MenuSettings.unitPreviewX + i *
                                         MenuSettings.unitPreviewDeltaX, MenuSettings.unitPreviewY))
            elif self.deep == 1:
                unit = player.info.get_info("unit")
                AllCat = player.info.get_info("cat")

                self.draw_text(
                    "选择要放置的猫糕：", 280, 53, MenuSettings.titleColor, 40, MenuSettings.titleFont)

                if len(AllCat) != 0:
                    self.draw_block(MenuSettings.replaceCatBlockX, MenuSettings.replaceCatBlockY + self.rightChooseR * MenuSettings.replaceCatDeltaY,
                                    MenuSettings.replaceCatBlockWidth, MenuSettings.replaceCatBlockHeight, MenuSettings.replaceCatBlockColor2)

                self.draw_text("名称", MenuSettings.replaceCatIDX,
                               MenuSettings.replaceCatEntryY,
                               MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                self.draw_text("生命值", MenuSettings.replaceCatAttributeX,
                               MenuSettings.replaceCatEntryY,
                               MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                self.draw_text("攻击力", MenuSettings.replaceCatAttributeX + MenuSettings.replaceCatAttributeDeltaX,
                               MenuSettings.replaceCatEntryY,
                               MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                self.draw_text("防御力", MenuSettings.replaceCatAttributeX + MenuSettings.replaceCatAttributeDeltaX * 2,
                               MenuSettings.replaceCatEntryY,
                               MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                self.draw_text("金币获取率", MenuSettings.replaceCatAttributeX + MenuSettings.replaceCatAttributeDeltaX * 3,
                               MenuSettings.replaceCatEntryY,
                               MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)

                count = 0
                for cat in AllCat:
                    img = pygame.transform.scale(
                        pygame.image.load(CatCake.es[cat]["preview"]),
                        (MenuSettings.replaceCatSize, MenuSettings.replaceCatSize)
                    )
                    self.window.blit(
                        img, (MenuSettings.replaceCatX, MenuSettings.replaceCatY + count * MenuSettings.replaceCatDeltaY))
                    self.draw_text(CatCake.es[cat]["name"], MenuSettings.replaceCatIDX,
                                   MenuSettings.replaceCatY + count * MenuSettings.replaceCatDeltaY +
                                   MenuSettings.replaceCatTextDownShift,
                                   MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                    self.draw_text(str(CatCake.es[cat]["hp"]), MenuSettings.replaceCatAttributeX,
                                   MenuSettings.replaceCatY + count * MenuSettings.replaceCatDeltaY +
                                   MenuSettings.replaceCatTextDownShift,
                                   MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                    self.draw_text(str(CatCake.es[cat]["atk"]), MenuSettings.replaceCatAttributeX + MenuSettings.replaceCatAttributeDeltaX,
                                   MenuSettings.replaceCatY + count * MenuSettings.replaceCatDeltaY +
                                   MenuSettings.replaceCatTextDownShift,
                                   MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                    self.draw_text(str(CatCake.es[cat]["def"]), MenuSettings.replaceCatAttributeX + MenuSettings.replaceCatAttributeDeltaX * 2,
                                   MenuSettings.replaceCatY + count * MenuSettings.replaceCatDeltaY +
                                   MenuSettings.replaceCatTextDownShift,
                                   MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                    self.draw_text(str(CatCake.es[cat]["gold"]) + '%', MenuSettings.replaceCatAttributeX + MenuSettings.replaceCatAttributeDeltaX * 3,
                                   MenuSettings.replaceCatY + count * MenuSettings.replaceCatDeltaY +
                                   MenuSettings.replaceCatTextDownShift,
                                   MenuSettings.replaceCatTextColor, MenuSettings.replaceCatTextSize, MenuSettings.replaceCatTextFont)
                    count += 1

        elif self.catergory == 4:
            nowY = MenuSettings.anchorY
            anchors = player.info.get_info("anchor")
            for anchor in anchors:
                nowY = self.draw_row(anchor, MenuSettings.anchorX,
                                     MenuSettings.anchorColor, MenuSettings.anchorSize, MenuSettings.anchorFont,
                                     nowY, MenuSettings.anchorDeltaY)


class ShoppingMenu(Scene):
    def __init__(self, window, ID) -> None:
        super().__init__(window)
        self.ID = ID
        self.state = 0                                  # 0: 碰到未进入, 1: 进入对话状态, 2: 进入商店页
        self.page = 0
        self.option = 0
        self.choose = 0
        self.enterTime = 0
        self.goods = []

    def tap(self, event, player, *args):
        if self.state == 1:
            if event.key == pygame.K_RETURN:
                for execute in ShopDetail.map[self.ID]["execute"][self.page][self.option]:
                    if isinstance(execute, ExePage):
                        self.page = execute.exe()
                        self.option = 0
                    elif isinstance(execute, ExeClose):
                        self.state = 0
                        player.info.modify("state", 0)
                    elif isinstance(execute, ExeOpenShop):
                        self.state = 2
                        self.choose = 0
                        self.enterTime = 0
                        player.info.modify("state", 5)
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.option > 0:
                    self.option -= 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if self.option + 1 < len(ShopDetail.map[self.ID]["options"][self.page]):
                    self.option += 1
        elif self.state == 2:
            if event.key == pygame.K_ESCAPE:
                player.info.modify("state", 0)
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.choose > 0:
                    self.enterTime = 0
                    self.choose -= 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if self.choose < len(self.goods) - 1:
                    self.enterTime = 0
                    self.choose += 1
            elif event.key == pygame.K_RETURN:
                if self.enterTime == 0 and len(self.goods) != 0:
                    good = self.goods[self.choose]
                    if player.info.get_info("money") >= good["price"]:
                        self.enterTime += 1
                elif self.enterTime == 1:
                    all_shopping_history = player.info.get_info(
                        "shoppingHistory")
                    history = all_shopping_history[self.ID] if self.ID in all_shopping_history else [
                    ]
                    good = self.goods[self.choose]
                    history.append(good["number"])
                    player = ExeAttribute("money", -good["price"]).exe(player)

                    for execute in good["execute"]:
                        if isinstance(execute, ExeAttribute):
                            player = execute.exe(player)
                        elif isinstance(execute, ExeProcess):
                            player = execute.exe(player)

                    all_shopping_history[self.ID] = history
                    player.info.modify("shoppingHistory", all_shopping_history)
                    self.enterTime = 0
                    self.choose = 0
                    player.save()
        return player

    def render(self, player):
        if self.state == 0:
            self.draw_block(BoardSettings.blockX, BoardSettings.blockY,
                            BoardSettings.blockWidth, BoardSettings.blockHeight, BoardSettings.blockColor)
            self.draw_text("按Enter键进入商店", BoardSettings.hintX, BoardSettings.hintY,
                           BoardSettings.hintColor, BoardSettings.hintSize, BoardSettings.hintFont)
        elif self.state == 1:
            rect_surface = pygame.Surface(
                (DialogueSettings.bgWidth, DialogueSettings.bgHeight), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, DialogueSettings.bgColor,
                             (0, 0, DialogueSettings.bgWidth, DialogueSettings.bgHeight))
            pygame.draw.rect(rect_surface, DialogueSettings.chooseColor, (DialogueSettings.chooseX, DialogueSettings.chooseY + DialogueSettings.chooseSpace * self.option,
                                                                          DialogueSettings.chooseWidth, DialogueSettings.chooseHeight))
            self.window.blit(
                rect_surface, (DialogueSettings.bgX, DialogueSettings.bgY))

            img = pygame.transform.scale(
                pygame.image.load(ShopDetail.map[self.ID]["img"][self.page]),
                ShopDetail.map[self.ID]["scale"][self.page]
            )
            self.window.blit(img, ShopDetail.map[self.ID]["imgxy"][self.page])

            text = ShopDetail.map[self.ID]["text"][self.page]
            text = [text[i: i + DialogueSettings.rowLimit]
                    for i in range(0, len(text), DialogueSettings.rowLimit)]
            for i in range(len(text)):
                row_text = text[i]
                self.draw_text(row_text, DialogueSettings.textX, DialogueSettings.textY + i * DialogueSettings.rowSpace,
                               DialogueSettings.textColor, DialogueSettings.textSize, DialogueSettings.textFont)

            options = ShopDetail.map[self.ID]["options"][self.page]
            for i in range(len(options)):
                option = "- " + options[i]
                self.draw_text(option, DialogueSettings.optionX, DialogueSettings.optionY + i * DialogueSettings.optionSpace,
                               DialogueSettings.textColor if i != self.option else DialogueSettings.textColor2,
                               DialogueSettings.textSize, DialogueSettings.textFont)
        elif self.state == 2:
            self.draw_block(MenuSettings.bgX, MenuSettings.bgY,
                            MenuSettings.bgWidth, MenuSettings.bgHeight, MenuSettings.bgColor)

            all_goods = ShopDetail.map[self.ID]["goods"]
            all_shopping_history = player.info.get_info("shoppingHistory")
            history = all_shopping_history[self.ID] if self.ID in all_shopping_history else [
            ]

            def check_premise(good) -> bool:
                for premise in good["premise"]:
                    if premise not in history:
                        return False
                return True
            # 筛掉买过的
            all_goods = [
                good for good in all_goods if good["number"] not in history]
            # all_goods = [all_goods[number] for number in range(
            # len(all_goods)) if number not in history]
            # 按0,1,2排序并筛掉不满足购买前提条件的
            sorted_goods = [[good for good in all_goods if good["sort"]
                             == sort and check_premise(good)] for sort in range(3)]
            nowY = ShopSettings.startY
            self.draw_text("当前金币： " + str(player.info.get_info("money")),
                           ShopSettings.goldX, ShopSettings.goldY,
                           ShopSettings.textColor, ShopSettings.goldSize, ShopSettings.textFont)
            if self.enterTime == 1:
                self.draw_text("再次按回车确认购买",
                               ShopSettings.hintX, ShopSettings.goldY,
                               ShopSettings.textColor, ShopSettings.goldSize, ShopSettings.textFont)
            if max(len(sorted_goods[0]), len(sorted_goods[1]), len(sorted_goods[2])) > 0:
                self.draw_block(ShopSettings.blockX, nowY + self.choose * ShopSettings.deltaY - ShopSettings.blockShift,
                                ShopSettings.blockWidth, ShopSettings.blockHeight,
                                ShopSettings.blockColor if self.enterTime == 0 else ShopSettings.blockColor2)

            self.goods = []
            for sort in range(3):
                goods = sorted_goods[sort]
                for good in goods:
                    img = pygame.transform.scale(
                        pygame.image.load(
                            good["img"] if good["img"] is not None else r".\assets\map\treasure.png"),
                        (ShopSettings.imgSize, ShopSettings.imgSize)
                    )
                    self.window.blit(img, (ShopSettings.imgX, nowY))
                    self.draw_text(ShopDetail.catergory[sort], ShopSettings.caterX, nowY + ShopSettings.textShift,
                                   ShopSettings.textColor, ShopSettings.textSize, ShopSettings.textFont)
                    self.draw_text(good["description"], ShopSettings.descriptionX, nowY + ShopSettings.textShift,
                                   ShopSettings.textColor, ShopSettings.textSize, ShopSettings.textFont)
                    self.draw_text(str(good["price"]) + " 金币", ShopSettings.priceX, nowY + ShopSettings.textShift,
                                   ShopSettings.textColor, ShopSettings.textSize, ShopSettings.textFont)
                    nowY += ShopSettings.deltaY
                    self.goods.append(good)


class Board(Scene):
    def __init__(self, window, ID) -> None:
        super().__init__(window)
        self.type = "board"
        self.ID = ID
        self.window = window
        self.beEnter = False

    def enter(self, player):
        self.beEnter = True

    def tap(self, event, *args):
        pass

    def render(self):
        if self.beEnter == False:
            self.draw_block(BoardSettings.blockX, BoardSettings.blockY,
                            BoardSettings.blockWidth, BoardSettings.blockHeight, BoardSettings.blockColor)
            self.draw_text("按Enter键" + BoardDetail.map[self.ID]["hint"], BoardSettings.hintX, BoardSettings.hintY,
                           BoardSettings.hintColor, BoardSettings.hintSize, BoardSettings.hintFont)


class Dialogue(Board):
    def __init__(self, window, ID) -> None:
        super().__init__(window, ID)
        self.page = 0
        self.option = 0

    def enter(self, player):
        super().enter(player)
        self.page = 0
        self.option = 0

    def tap(self, event, player, *args):
        if event.key == pygame.K_RETURN:
            for execute in BoardDetail.map[self.ID]["execute"][self.page][self.option]:
                if isinstance(execute, ExePage):
                    self.page = execute.exe()
                    self.option = 0
                elif isinstance(execute, ExeClose):
                    self.beEnter = False
                    player.info.modify("state", 0)
                elif isinstance(execute, ExeMoney):
                    player = execute.exe(player)
                elif isinstance(execute, ExeAttribute):
                    player = execute.exe(player)
        elif event.key == pygame.K_w or event.key == pygame.K_UP:
            if self.option > 0:
                self.option -= 1
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            if self.option + 1 < len(BoardDetail.map[self.ID]["options"][self.page]):
                self.option += 1
        return player

    def render(self):
        super().render()
        if self.beEnter:
            rect_surface = pygame.Surface(
                (DialogueSettings.bgWidth, DialogueSettings.bgHeight), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, DialogueSettings.bgColor,
                             (0, 0, DialogueSettings.bgWidth, DialogueSettings.bgHeight))
            pygame.draw.rect(rect_surface, DialogueSettings.chooseColor, (DialogueSettings.chooseX, DialogueSettings.chooseY + DialogueSettings.chooseSpace * self.option,
                                                                          DialogueSettings.chooseWidth, DialogueSettings.chooseHeight))
            self.window.blit(
                rect_surface, (DialogueSettings.bgX, DialogueSettings.bgY))

            # test
            # print(len(BoardDetail.map[self.ID]["img"]))
            img = pygame.transform.scale(
                pygame.image.load(BoardDetail.map[self.ID]["img"][self.page]),
                BoardDetail.map[self.ID]["scale"][self.page]
            )
            self.window.blit(img, BoardDetail.map[self.ID]["imgxy"][self.page])

            text = BoardDetail.map[self.ID]["text"][self.page]
            text = [text[i: i + DialogueSettings.rowLimit]
                    for i in range(0, len(text), DialogueSettings.rowLimit)]
            for i in range(len(text)):
                row_text = text[i]
                self.draw_text(row_text, DialogueSettings.textX, DialogueSettings.textY + i * DialogueSettings.rowSpace,
                               DialogueSettings.textColor, DialogueSettings.textSize, DialogueSettings.textFont)

            options = BoardDetail.map[self.ID]["options"][self.page]
            for i in range(len(options)):
                option = "- " + options[i]
                self.draw_text(option, DialogueSettings.optionX, DialogueSettings.optionY + i * DialogueSettings.optionSpace,
                               DialogueSettings.textColor if i != self.option else DialogueSettings.textColor2,
                               DialogueSettings.textSize, DialogueSettings.textFont)


class BattleSkills(Skills):
    def __init__(self, name):
        self.name = name
        self.description = Skills.es[name]["name"]
        self.r = Skills.es[name]["r"]
        self.pp = Skills.es[name]["pp"]
        self.skillAnimateTime = Skills.es[name]["skillAnimateTime"]
        self.execute = Skills.es[name]["execute"]
        self.imagePath = Skills.es[name]["preview"]
        self.imageScale = (BattleSettings.skillIconX,
                           BattleSettings.skillIconY)

    def get_name(self):
        return str(self.name)


class BattleCatCake(CatCake):
    def __init__(self, name, player, skillList):
        cake = CatCake.es[name]
        self.attribute = {
            "name": name,
            "hp": cake["hp"],
            "pp": 3,
            "atk": cake["atk"],
            "def": cake["def"],
            "fullHp": cake["hp"]
        }

        if player != None:
            playerAttribute = player.info.get_info("basic")
            self.attribute["hp"] += playerAttribute["hp"]
            self.attribute["atk"] += playerAttribute["atk"]
            self.attribute["def"] += playerAttribute["def"]
            self.attribute["fullHp"] += playerAttribute["hp"]

        self.imagePath = CatCake.es[name]["preview"]
        self.imageScale = (BattleSettings.cakeIconX, BattleSettings.cakeIconY)
        if name == "cat_trash":
            if random.randint(1, 100) <= 5:
                self.imagePath = BattleSettings.trashKing
                self.imageScale = (BattleSettings.trashKingIconX,
                                   BattleSettings.trashKingIconY)
                self.attribute["hp"] = 99999
                self.attribute["atk"] = 99999
                self.attribute["def"] = 99999
                self.attribute["fullHp"] = 99999

        # self.skillList存储的是猫的第i个技能，第1个一定是平A

        self.skillList = [BattleSkills("A")]
        self.skillList.append(None)
        self.skillList.append(None)
        if skillList == None:
            AllSkill = player.info.get_info("skillUse")
            if name in AllSkill:
                index = 0
                for skillName in AllSkill[name]:
                    index += 1
                    if skillName == "":
                        skill = None
                    else:
                        skill = BattleSkills(skillName)
                    self.skillList[index] = skill
        else:
            skill1, skill2 = skillList
            if skill1 != None:
                self.skillList[1] = BattleSkills(skill1)
            if skill2 != None:
                self.skillList[2] = BattleSkills(skill2)
        self.buffList = []


class BattleScene(Scene):
    def __init__(self, window, ID, player, enemy) -> None:
        pygame.mixer.music.load(Music.battle)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
        self.round = 0
        self.window = window
        self.ID = ID
        self.background = pygame.image.load(enemy["background"])
        self.background = pygame.transform.scale(
            self.background, (WindowSettings.width, WindowSettings.height))
        playerBasic = player.info.get_info("basic")
        self.cakeList = []
        cakeList = playerBasic["unit"]
        for i in range(len(cakeList)):
            if cakeList[i] == None:
                continue
            cake = BattleCatCake(cakeList[i], player, None)
            self.cakeList.append(cake)
        '''
        enemy的形式还没传递好
        '''
        self.enemyList = []
        for i in range(len(enemy["cakeSurface"])):
            cake = BattleCatCake(
                enemy["cakeSurface"][i], None, enemy["cakeSkill"][i])
            self.enemyList.append(cake)
        # self.enemyList = copy.deepcopy(self.cakeList)
        # self.enemyList.append(copy.deepcopy(self.cakeList[0]))
        # self.enemyList.append(copy.deepcopy(self.cakeList[0]))
        # self.enemyList.append(copy.deepcopy(self.cakeList[0]))
        # self.cakeList.append(copy.deepcopy(self.cakeList[0]))

        # test127
        # self.enemyList = copy.deepcopy(self.enemyList) + copy.deepcopy(self.enemyList)
        '''
        这里先复制一下主角队伍
        '''
        self.preCakeList = []
        self.preEnemyList = []
        self.nowCake = 0
        self.nowSkill = 0
        self.nowEnemy = 0
        self.actEnemy = len(self.enemyList)-1
        self.enemySkill = 0
        self.enemyTarget = 0
        self.battleState = 0
        self.pp = 3
        '''
        初始值为0
        '''
        self.inAttackTimer = 0
        self.inEffectTimer = 0

    def get_cake_pos(self, i):
        return BattleSettings.cakeStartX-i*(BattleSettings.cakeIconX+BattleSettings.iconGap), BattleSettings.cakeStartY

    def get_enemy_pos(self, i):
        return BattleSettings.enemyStartX+i*(BattleSettings.enemyIconX+BattleSettings.iconGap), BattleSettings.enemyStartY

    def get_skill_pos(self, i):
        return BattleSettings.skillStartX+i*(BattleSettings.skillIconX+BattleSettings.skillGap), BattleSettings.skillStartY

    def get_cake_id(self, i):
        return (i+len(self.cakeList)) % len(self.cakeList)

    def get_enemy_id(self, i):
        return (i+len(self.enemyList)) % len(self.enemyList)

    def get_skill_id(self, i, length):
        return (i+length) % length

    def next_state(self):
        self.battleState = (self.battleState+1) % 11

    def cake_attack_end(self):
        if self.inAttackTimer <= self.cakeList[self.nowCake].skillList[self.nowSkill].skillAnimateTime:
            return False
        return True

    def enemy_attack_end(self):
        if self.inAttackTimer <= self.enemySkill.skillAnimateTime:
            return False
        return True

    def effect_end(self):
        if self.inEffectTimer <= BattleSettings.effectAnimateTime:
            return False
        return True

    def check_round(self):
        selfLive = len(self.cakeList)
        enemyLive = len(self.enemyList)
        if selfLive == 0:
            return "LOSE"
        for i in range(len(self.cakeList)):
            cake = self.cakeList[i]
            if cake.attribute["hp"] <= 0:
                selfLive -= 1
                self.cakeList[i].imagePath = CatCake.es[self.cakeList[i].attribute["name"]]["dead"]
                # cake.image = DIEIMAGE
            if cake.attribute["hp"] > cake.attribute["fullHp"]:
                cake.attribute["hp"] = cake.attribute["fullHp"]
        for i in range(len(self.enemyList)):
            enemy = self.enemyList[i]
            if enemy.attribute["hp"] <= 0:
                enemyLive -= 1
                self.enemyList[i].imagePath = CatCake.es[self.enemyList[i].attribute["name"]]["dead"]
                # enemy.image = DIEIMAGE
            if enemy.attribute["hp"] > enemy.attribute["fullHp"]:
                enemy.attribute["hp"] = enemy.attribute["fullHp"]
        # print(enemyLive, selfLive)
        if enemyLive == 0:
            return "WIN"
        if selfLive == 0:
            return "LOSE"

    def get_random_enemy(self):
        i = random.randint(0, len(self.enemyList)-1)
        while self.enemyList[i].attribute["hp"] <= 0:
            i = random.randint(0, len(self.enemyList)-1)
        return i

    def cakeAlive(self, i):
        if self.cakeList[i].attribute["hp"] <= 0:
            return False
        return True

    def cakeDead(self, i):
        return not self.cakeAlive(i)

    def get_next_cake(self):
        self.nowCake = self.get_cake_id(self.nowCake+1)
        while self.cakeDead(self.nowCake):
            self.nowCake = self.get_cake_id(self.nowCake+1)

    def enemyAlive(self, i):
        if self.enemyList[i].attribute["hp"] <= 0:
            return False
        return True

    def enemyDead(self, i):
        return not self.enemyAlive(i)

    def get_next_enemy(self):
        self.actEnemy = self.get_enemy_id(self.actEnemy+1)
        while self.enemyDead(self.actEnemy):
            self.actEnemy = self.get_enemy_id(self.actEnemy+1)

    # 每次按键返回战斗状态： 0 输， 1 继续， 2 赢
    def tap(self, event):
        if event.key == pygame.K_0:
            return 0
        elif event.key == pygame.K_2:
            return 2
        else:
            return 1

    def update(self, events):
        pressL = False
        pressR = False
        pressSpace = False

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    pressL = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    pressR = True
                if event.key == pygame.K_SPACE:
                    pressSpace = True

        # print(self.battleState)

        if self.battleState == 0:
            status = self.check_round()
            if status == "LOSE":
                return 0
            if pressL == True:
                self.nowSkill = self.get_skill_id(
                    self.nowSkill-1, len(self.cakeList[self.nowCake].skillList))
            if pressR == True:
                self.nowSkill = self.get_skill_id(
                    self.nowSkill+1, len(self.cakeList[self.nowCake].skillList))
            if pressSpace == True:
                skill = self.cakeList[self.nowCake].skillList[self.nowSkill]
                if skill != None and skill.pp <= self.pp:
                    self.next_state()

        elif self.battleState == 1:
            self.next_state()

        elif self.battleState == 2:
            if pressL == True:
                self.nowEnemy = self.get_enemy_id(self.nowEnemy-1)
            if pressR == True:
                self.nowEnemy = self.get_enemy_id(self.nowEnemy+1)
            if pressSpace == True:
                self.next_state()

        elif self.battleState == 3:
            self.next_state()

        elif self.battleState == 4:
            cake = self.cakeList[self.nowCake]
            skill = cake.skillList[self.nowSkill]
            self.preCakeList = copy.deepcopy(self.cakeList)
            self.preEnemyList = copy.deepcopy(self.enemyList)
            cakeEffectedList = []
            enemyEffectedList = []
            self.pp -= skill.pp
            if self.pp > 10:
                self.pp = 10
            for execute in skill.execute:
                obj = execute.obj
                if obj == "self":
                    round_i = (self.nowCake+execute.did +
                               len(self.cakeList)) % len(self.cakeList)
                    linear_i = self.nowCake+execute.did

                    if skill.r >= 4:
                        if (round_i, execute.key) in cakeEffectedList:
                            continue
                        else:
                            cakeEffectedList.append((round_i, execute.key))
                    else:
                        if linear_i < 0 or linear_i >= len(self.cakeList):
                            continue
                        elif (linear_i, execute.key) in cakeEffectedList:
                            continue
                        else:
                            cakeEffectedList.append((linear_i, execute.key))
                else:
                    round_i = (self.nowEnemy+execute.did +
                               len(self.enemyList)) % len(self.enemyList)
                    linear_i = self.nowEnemy+execute.did

                    if skill.r >= 4:
                        if (round_i, execute.key) in enemyEffectedList:
                            continue
                        else:
                            enemyEffectedList.append((round_i, execute.key))
                    else:
                        if linear_i < 0 or linear_i >= len(self.enemyList):
                            continue
                        elif (linear_i, execute.key) in enemyEffectedList:
                            continue
                        else:
                            enemyEffectedList.append((linear_i, execute.key))
                self.cakeList, self.enemyList = execute.exe(
                    self.nowCake, self.nowEnemy, self.cakeList, self.enemyList, "PLAYER ROUND", skill.r >= 4)

            # 这里要处理所有的技能伤害与buff

            self.cakeHpDeltaList = []
            self.enemyHpDeltaList = []
            for i in range(len(self.cakeList)):
                cake = self.cakeList[i]
                preCake = self.preCakeList[i]
                deltaHp = cake.attribute["hp"]-preCake.attribute["hp"]
                if deltaHp > 0:
                    self.cakeHpDeltaList.append([i, '+', deltaHp])
                if deltaHp < 0:
                    self.cakeHpDeltaList.append([i, '-', deltaHp])
            for i in range(len(self.enemyList)):
                enemy = self.enemyList[i]
                preEnemy = self.preEnemyList[i]
                deltaHp = enemy.attribute["hp"]-preEnemy.attribute["hp"]
                if deltaHp > 0:
                    self.enemyHpDeltaList.append([i, '+', deltaHp])
                if deltaHp < 0:
                    self.enemyHpDeltaList.append([i, '-', deltaHp])
            self.next_state()

        elif self.battleState == 5:
            if self.cake_attack_end() == True:
                self.inAttackTimer = 0
                self.next_state()

        elif self.battleState == 6:
            if self.effect_end() == True:
                self.inEffectTimer = 0
                state = self.check_round()
                # state = "WIN"
                if state == "WIN":
                    return 2
                if state == "LOSE":
                    return 0
                self.get_next_enemy()
                self.next_state()

        elif self.battleState == 7:
            '''
            self.enemySkill = BattleSkills("A")
            self.enemyTarget = 0
            self.next_state()
            '''
            # print(len(self.cakeList), self.nowEnemy)
            cake = self.enemyList[self.actEnemy]
            skill1 = None
            skill2 = None
            if len(cake.skillList) >= 2:
                if cake.skillList[1] != None:
                    skill1 = cake.skillList[1].get_name()
            if len(cake.skillList) >= 3:
                if cake.skillList[2] != None:
                    skill2 = cake.skillList[2].get_name()
            '''
            if cake.skillList[0] == Skills.es["A"]:
                print(1)
            if skill1 == Skills.es["skill_ice"]:
                print(1)
            '''
            ally_minx = 100000
            ally_mini = -1
            injured = 0
            # print(skill1)
            if len(self.cakeList) == 1:
                aoe_center = 0
            elif len(self.cakeList) <= 3:
                aoe_center = 1
            else:
                if int(self.cakeList[0].attribute["hp"] <= 0) > int(self.cakeList[3].attribute["hp"] <= 0):
                    aoe_center = 2
                else:
                    aoe_center = 1
            for i in range(len(self.enemyList)):
                if self.enemyList[i].attribute["hp"] > 0 and self.enemyList[i].attribute["hp"] < self.enemyList[i].attribute["fullHp"]:
                    injured += 1
            for i in range(len(self.cakeList)):
                target = self.cakeList[i]
                if target.attribute["hp"] > 0:
                    if ally_minx > target.attribute["hp"]:
                        ally_mini = i
                        ally_minx = target.attribute["hp"]
                if target.attribute["hp"] > 0 and target.attribute["hp"] < 0.25 * target.attribute["fullHp"]:
                    self.enemySkill = BattleSkills("A")
                    self.enemyTarget = i
                    self.next_state()
                    return 1
                target = self.cakeList[i]
                if target.attribute["hp"] > 0:
                    if ally_minx > target.attribute["hp"]:
                        ally_mini = i
                        ally_minx = target.attribute["hp"]
            if cake.attribute["pp"] < 2:
                self.enemySkill = BattleSkills("A")
                self.enemyTarget = ally_mini
                self.next_state()
                return 1
            if skill1 == "skill_ice":
                self.enemySkill = BattleSkills(skill1)
                self.enemyTarget = 0
                self.next_state()
                return 1
            if skill2 == "skill_ice":
                self.enemySkill = BattleSkills(skill2)
                self.enemyTarget = 0
                self.next_state()
                return 1
            Apro = 1000
            skill1pro = 0
            skill2pro = 0
            if skill1 == "skill_red":
                skill1pro = 1500 + 500 * self.round
            if skill1 == "skill_pink" or skill1 == "skill_cyan":
                skill1pro = 1500 + 500 * max(0, 5 - self.round)
            if skill1 == "skill_yellow":
                skill1pro = 1500 * injured
            if skill2 == "skill_red":
                skill2pro = 1500 + 500 * self.round
            if skill2 == "skill_pink" or skill2 == "skill_cyan":
                skill2pro = 1500 + 500 * max(0, 5 - self.round)
            if skill2 == "skill_yellow":
                skill1pro = 1500 * injured
            totalpro = Apro + skill1pro + skill2pro
            randresult = random.randint(1, totalpro)
            if randresult <= skill1pro:
                self.enemySkill = BattleSkills(skill1)
                if skill1 == "skill_red":
                    self.enemyTarget = aoe_center
                else:
                    self.enemyTarget = 0
                self.next_state()
                return 1
            if randresult <= skill1pro + skill2pro:
                self.enemySkill = BattleSkills(skill2)
                if skill2 == "skill_red":
                    self.enemyTarget = aoe_center
                else:
                    self.enemyTarget = 0
                self.next_state()
                return 1
            self.enemySkill = BattleSkills("A")
            self.enemyTarget = ally_mini
            self.next_state()
            return 1

        elif self.battleState == 8:
            self.preCakeList = copy.deepcopy(self.cakeList)
            self.preEnemyList = copy.deepcopy(self.enemyList)
            cakeEffectedList = []
            enemyEffectedList = []
            self.actEnemy = self.get_random_enemy()
            skill = self.enemySkill
            for execute in self.enemySkill.execute:
                obj = execute.obj
                if obj == "enemy":
                    round_i = (self.enemyTarget+execute.did +
                               len(self.cakeList)) % len(self.cakeList)
                    linear_i = self.enemyTarget+execute.did

                    if skill.r >= 4:
                        if (round_i, execute.key) in cakeEffectedList:
                            continue
                        else:
                            cakeEffectedList.append((round_i, execute.key))
                    else:
                        if linear_i < 0 or linear_i >= len(self.cakeList):
                            continue
                        elif (linear_i, execute.key) in cakeEffectedList:
                            continue
                        else:
                            cakeEffectedList.append((linear_i, execute.key))
                else:
                    round_i = (self.enemyTarget+execute.did +
                               len(self.enemyList)) % len(self.enemyList)
                    linear_i = self.enemyTarget+execute.did

                    if skill.r >= 4:
                        if (round_i, execute.key) in enemyEffectedList:
                            continue
                        else:
                            enemyEffectedList.append((round_i, execute.key))
                    else:
                        if linear_i < 0 or linear_i >= len(self.enemyList):
                            continue
                        elif (linear_i, execute.key) in enemyEffectedList:
                            continue
                        else:
                            enemyEffectedList.append((linear_i, execute.key))
                self.cakeList, self.enemyList = execute.exe(
                    self.actEnemy, self.enemyTarget, self.cakeList, self.enemyList, "ENEMY ROUND", skill.r >= 4)

            # 这里要处理所有的技能伤害与buff

            self.cakeHpDeltaList = []
            self.enemyHpDeltaList = []
            for i in range(len(self.cakeList)):
                cake = self.cakeList[i]
                preCake = self.preCakeList[i]
                deltaHp = cake.attribute["hp"]-preCake.attribute["hp"]
                if deltaHp > 0:
                    self.cakeHpDeltaList.append([i, '+', deltaHp])
                if deltaHp < 0:
                    self.cakeHpDeltaList.append([i, '-', deltaHp])
            for i in range(len(self.enemyList)):
                enemy = self.enemyList[i]
                preEnemy = self.preEnemyList[i]
                deltaHp = enemy.attribute["hp"]-preEnemy.attribute["hp"]
                if deltaHp > 0:
                    self.enemyHpDeltaList.append([i, '+', deltaHp])
                if deltaHp < 0:
                    self.enemyHpDeltaList.append([i, '-', deltaHp])
            self.next_state()

        elif self.battleState == 9:
            if self.enemy_attack_end() == True:
                self.inAttackTimer = 0
                self.next_state()

        elif self.battleState == 10:
            if self.effect_end() == True:
                self.inEffectTimer = 0
                state = self.check_round()
                if state == "WIN":
                    return 2
                if state == "LOSE":
                    return 0
                self.get_next_cake()
                self.next_state()

        return 1

    def render(self):
        self.window.blit(self.background, (0, 0))

        for i in range(len(self.cakeList)):
            cake = self.cakeList[i]
            cakeImage = pygame.transform.scale(
                pygame.image.load(cake.imagePath), cake.imageScale)
            self.window.blit(cakeImage, self.get_cake_pos(i))
            hpLeft, hpTop = self.get_cake_pos(i)
            self.draw_text(str(cake.attribute["hp"])+" / "+str(cake.attribute["fullHp"]), hpLeft, hpTop-BattleSettings.hpSize-25,
                           BattleSettings.hpColor, BattleSettings.hpSize, BattleSettings.hpFont)
            # 画血条
            hpBrickImage = pygame.image.load(BattleSettings.hpBrickPath)
            hpBrickImage = pygame.transform.scale(hpBrickImage, (int(
                BattleSettings.hpBrickX*(cake.attribute["hp"]/cake.attribute["fullHp"])), BattleSettings.hpBrickY))
            hpBrickLeft, hpBrickTop = self.get_cake_pos(i)
            self.window.blit(hpBrickImage, (hpBrickLeft,
                             hpBrickTop-4-BattleSettings.hpBrickY))

            hpBarImage = pygame.image.load(BattleSettings.hpBarPath)
            hpBarImage = pygame.transform.scale(
                hpBarImage, (BattleSettings.hpBarX, BattleSettings.hpBarY))
            hpBarLeft, hpBarTop = self.get_cake_pos(i)
            self.window.blit(hpBarImage, (hpBarLeft-3,
                             hpBarTop-2-BattleSettings.hpBarY))
            # 画atk和def
            if cake.attribute["atk"] > 10000:
                continue
            attributeLeft, attributeTop = self.get_cake_pos(i)
            self.draw_text("atk:"+str(cake.attribute["atk"]), attributeLeft, attributeTop+BattleSettings.cakeIconY+2,
                           BattleSettings.attributeColor, BattleSettings.attributeSize, BattleSettings.attributeFont)
            self.draw_text("def:"+str(cake.attribute["def"]), attributeLeft, attributeTop+BattleSettings.cakeIconY+32,
                           BattleSettings.attributeColor, BattleSettings.attributeSize, BattleSettings.attributeFont)

        for i in range(len(self.enemyList)):
            enemy = self.enemyList[i]
            enemyImage = pygame.transform.scale(
                pygame.image.load(enemy.imagePath), enemy.imageScale)
            enemyImage = pygame.transform.flip(enemyImage, True, False)
            self.window.blit(enemyImage, self.get_enemy_pos(i))
            hpLeft, hpTop = self.get_enemy_pos(i)
            self.draw_text(str(enemy.attribute["hp"])+" / "+str(enemy.attribute["fullHp"]), hpLeft, hpTop-BattleSettings.hpSize-25,
                           BattleSettings.hpColor, BattleSettings.hpSize, BattleSettings.hpFont)
            # 画血条
            hpBrickImage = pygame.image.load(BattleSettings.hpBrickPath)
            hpBrickImage = pygame.transform.scale(hpBrickImage, (int(
                BattleSettings.hpBrickX*(enemy.attribute["hp"]/enemy.attribute["fullHp"])), BattleSettings.hpBrickY))
            hpBrickLeft, hpBrickTop = self.get_enemy_pos(i)
            self.window.blit(hpBrickImage, (hpBrickLeft,
                             hpBrickTop-4-BattleSettings.hpBrickY))

            hpBarImage = pygame.image.load(BattleSettings.hpBarPath)
            hpBarImage = pygame.transform.scale(
                hpBarImage, (BattleSettings.hpBarX, BattleSettings.hpBarY))
            hpBarLeft, hpBarTop = self.get_enemy_pos(i)
            self.window.blit(hpBarImage, (hpBarLeft-3,
                             hpBarTop-2-BattleSettings.hpBarY))
            # 画atk和def
            attributeLeft, attributeTop = self.get_enemy_pos(i)
            self.draw_text("atk:"+str(enemy.attribute["atk"]), attributeLeft, attributeTop+BattleSettings.cakeIconY+2,
                           BattleSettings.attributeColor, BattleSettings.attributeSize, BattleSettings.attributeFont)
            self.draw_text("def:"+str(enemy.attribute["def"]), attributeLeft, attributeTop+BattleSettings.cakeIconY+32,
                           BattleSettings.attributeColor, BattleSettings.attributeSize, BattleSettings.attributeFont)

        for i in range(len(self.cakeList[self.nowCake].skillList)):
            skill = self.cakeList[self.nowCake].skillList[i]
            if skill == None:
                empty = pygame.image.load(BattleSettings.emptySkill)
                empty = pygame.transform.scale(
                    empty, (BattleSettings.skillIconX, BattleSettings.skillIconY))
                empty.set_alpha(BattleSettings.emptyAlpha)
                self.window.blit(empty, self.get_skill_pos(i))
            else:
                skillImage = pygame.transform.scale(
                    pygame.image.load(skill.imagePath), skill.imageScale)
                self.window.blit(skillImage, self.get_skill_pos(i))
                # 画pp描述
                if skill.name != "A":
                    skillPpLeft, skillPpTop = self.get_skill_pos(i)
                    skillPpImage = pygame.image.load(
                        BattleSettings.ppPath[skill.pp])
                    skillPpImage = pygame.transform.scale(
                        skillPpImage, (BattleSettings.ppX, BattleSettings.ppY))
                    self.window.blit(skillPpImage, (skillPpLeft, skillPpTop))
                # 写技能描述
                skillDescriptionLeft, skillDescriptionTop = self.get_skill_pos(
                    i)
                self.draw_text(skill.description, int(skillDescriptionLeft+75-len(skill.description)*9*1.5),
                               skillDescriptionTop+155, BattleSettings.skillColor, BattleSettings.skillSize, BattleSettings.skillFont)

        # 顶部白字提示绘制
        hint = "按 空格键 确认你的选择与操作"
        hpLeft, hpTop = self.get_cake_pos(i)
        self.draw_text(hint, BattleSettings.hintStartX, BattleSettings.hintStartY,
                       BattleSettings.hintColor, BattleSettings.hpSize, BattleSettings.hpFont)

        # pp条绘制
        if self.pp > 10:
            self.pp = 10
        energyBarImage = pygame.image.load(BattleSettings.energyBarPath)
        self.window.blit(
            energyBarImage, (BattleSettings.energyBarStartX, BattleSettings.energyBarStartY))
        energyBrickImage = pygame.image.load(BattleSettings.energyBrickPath)
        for i in range(self.pp):
            self.window.blit(energyBrickImage, (BattleSettings.energyBrickStartX +
                             i*(BattleSettings.energyBrickX+BattleSettings.energyBrickGap), BattleSettings.energyBrickStartY))

        # player的猫糕选择框
        # print(self.battleState)
        nowCakeLeft, nowCakeTop = self.get_cake_pos(self.nowCake)
        if self.cakeList[self.nowCake].attribute["atk"] > 10000:
            pygame.draw.rect(self.window, (0, 0, 0), (nowCakeLeft, nowCakeTop,
                             BattleSettings.trashKingIconX, BattleSettings.trashKingIconY), 3)
        else:
            pygame.draw.rect(self.window, (0, 0, 0), (nowCakeLeft, nowCakeTop,
                             BattleSettings.cakeIconX, BattleSettings.cakeIconY), 3)

        # 技能选择框
        nowSkillLeft, nowSkillTop = self.get_skill_pos(self.nowSkill)
        pygame.draw.rect(self.window, (0, 0, 0), (nowSkillLeft, nowSkillTop,
                         BattleSettings.skillIconX, BattleSettings.skillIconY), 3)

        # 对象选择框
        skill = self.cakeList[self.nowCake].skillList[self.nowSkill]
        if skill != None:
            r = skill.r
            faceSelf = True
            for execute in skill.execute:
                if execute.obj == "enemy":
                    faceSelf = False
                    break
            if faceSelf == False:
                for i in range(-int(r//2), int(r//2)+1, 1):
                    nowEnemy = self.get_enemy_id(self.nowEnemy+i)
                    if r < 4:
                        nowEnemy = self.nowEnemy+i
                        if nowEnemy < 0 or nowEnemy >= len(self.enemyList):
                            continue
                    nowEnemyLeft, nowEnemyTop = self.get_enemy_pos(nowEnemy)
                    pygame.draw.rect(self.window, (150, 150, 150), (nowEnemyLeft, nowEnemyTop,
                                                                    BattleSettings.enemyIconX, BattleSettings.enemyIconY), 3)
                nowEnemyLeft, nowEnemyTop = self.get_enemy_pos(self.nowEnemy)
                pygame.draw.rect(self.window, (0, 0, 0), (nowEnemyLeft, nowEnemyTop,
                                                          BattleSettings.enemyIconX, BattleSettings.enemyIconY), 3)

        # 阶段0 选技能 技能框是黑的 选择框只能在技能栏移动
        if self.battleState == 0:
            pass

        # 阶段1 确认所选技能 选中的技能框变红
        if self.battleState >= 1:
            nowSkillLeft, nowSkillTop = self.get_skill_pos(self.nowSkill)
            pygame.draw.rect(self.window, (255, 0, 0), (nowSkillLeft, nowSkillTop,
                                                        BattleSettings.skillIconX, BattleSettings.skillIconY), 3)

        # 阶段2 选攻击对象 正中间的对象是黑色的 其余的是灰色的
        if self.battleState >= 2:
            pass

        # 阶段3 确认所选技能 范围内的所有对象全变红
        if self.battleState >= 3 and self.cakeList[self.nowCake].skillList[self.nowSkill] != None:
            skill = self.cakeList[self.nowCake].skillList[self.nowSkill]
            r = skill.r
            faceSelf = True
            for execute in skill.execute:
                if execute.obj == "enemy":
                    faceSelf = False
                    break
            if faceSelf == False:
                for i in range(-int(r//2), int(r//2)+1, 1):
                    nowEnemy = self.get_enemy_id(self.nowEnemy+i)
                    if r < 4:
                        nowEnemy = self.nowEnemy+i
                        if nowEnemy < 0 or nowEnemy >= len(self.enemyList):
                            continue
                    nowEnemyLeft, nowEnemyTop = self.get_enemy_pos(nowEnemy)
                    pygame.draw.rect(self.window, (255, 0, 0), (nowEnemyLeft, nowEnemyTop,
                                                                BattleSettings.enemyIconX, BattleSettings.enemyIconY), 3)

        # 阶段4 扣血与buff的伤害清算
        if self.battleState == 4:
            pass

        # 阶段5 玩家角色的技能动画
        if self.battleState == 5:
            self.inAttackTimer += 1
            skillName = self.cakeList[self.nowCake].skillList[self.nowSkill].name
            skillImagePath = Skills.es[skillName]["animate"][self.inAttackTimer]
            skillImage = pygame.image.load(skillImagePath)
            skillImage = pygame.transform.scale(
                skillImage, (BattleSettings.cakeIconX, BattleSettings.cakeIconY))

            skill = self.cakeList[self.nowCake].skillList[self.nowSkill]
            for execute in skill.execute:
                obj = execute.obj
                if obj == "self":
                    i = (self.nowCake+execute.did +
                         len(self.cakeList)) % len(self.cakeList)
                    if skill.r < 4:
                        i = self.nowCake+execute.did
                        if i < 0 or i >= len(self.cakeList):
                            continue
                    self.window.blit(skillImage, self.get_cake_pos(i))
                else:
                    i = (self.nowEnemy+execute.did +
                         len(self.enemyList)) % len(self.enemyList)
                    if skill.r < 4:
                        i = self.nowEnemy+execute.did
                        if i < 0 or i >= len(self.enemyList):
                            continue
                    self.window.blit(skillImage, self.get_enemy_pos(i))

        # 阶段6 扣血与buff的动画
        if self.battleState == 6:
            self.inEffectTimer += 1

            # print(self.inEffectTimer)
            # print(self.enemyHpDeltaList)

            for i, sig, deltaHp in self.cakeHpDeltaList:
                riseHpLeft, riseHpTop = self.get_cake_pos(i)
                riseHpTop -= BattleSettings.hpRiseDelatY + \
                    BattleSettings.hpRiseSpeed*self.inEffectTimer
                # print(riseHpLeft, riseHpTop)
                self.draw_text(str(deltaHp), riseHpLeft, riseHpTop,
                               BattleSettings.hpRiseColor[sig], BattleSettings.hpRiseSize, BattleSettings.hpRiseFont)
            for i, sig, deltaHp in self.enemyHpDeltaList:
                riseHpLeft, riseHpTop = self.get_enemy_pos(i)
                riseHpTop -= BattleSettings.hpRiseDelatY + \
                    BattleSettings.hpRiseSpeed*self.inEffectTimer
                self.draw_text(str(deltaHp), riseHpLeft, riseHpTop,
                               BattleSettings.hpRiseColor[sig], BattleSettings.hpRiseSize, BattleSettings.hpRiseFont)
                # print(riseHpLeft, riseHpTop)

        # 阶段7 敌方ai做出判断
        if self.battleState == 7:
            pass

        # 阶段8 扣血与buff的伤害清算
        if self.battleState == 8:
            pass

        # 阶段9 敌方角色的技能动画
        if self.battleState == 9:
            self.inAttackTimer += 1
            skillName = self.enemySkill.name
            skillImagePath = Skills.es[skillName]["animate"][self.inAttackTimer]
            skillImage = pygame.image.load(skillImagePath)
            skillImage = pygame.transform.scale(
                skillImage, (BattleSettings.cakeIconX, BattleSettings.cakeIconY))

            skill = self.enemySkill
            for execute in skill.execute:
                obj = execute.obj
                if obj == "self":
                    i = (self.nowEnemy+execute.did +
                         len(self.enemyList)) % len(self.enemyList)
                    if skill.r < 4:
                        i = self.nowEnemy+execute.did
                        if i < 0 or i >= len(self.enemyList):
                            continue
                    self.window.blit(skillImage, self.get_enemy_pos(i))
                else:
                    i = (self.enemyTarget+execute.did +
                         len(self.cakeList)) % len(self.cakeList)
                    if skill.r < 4:
                        i = self.enemyTarget+execute.did
                        if i < 0 or i >= len(self.cakeList):
                            continue
                    self.window.blit(skillImage, self.get_cake_pos(i))

        # 阶段10 扣血与buff的动画
        if self.battleState == 10:
            self.inEffectTimer += 1

            # print(self.inEffectTimer)
            # print(self.enemyHpDeltaList)
            self.round += 1
            for i, sig, deltaHp in self.cakeHpDeltaList:
                riseHpLeft, riseHpTop = self.get_cake_pos(i)
                riseHpTop -= BattleSettings.hpRiseDelatY + \
                    BattleSettings.hpRiseSpeed*self.inEffectTimer
                # print(riseHpLeft, riseHpTop)
                self.draw_text(str(deltaHp), riseHpLeft, riseHpTop,
                               BattleSettings.hpRiseColor[sig], BattleSettings.hpRiseSize, BattleSettings.hpRiseFont)
            for i, sig, deltaHp in self.enemyHpDeltaList:
                riseHpLeft, riseHpTop = self.get_enemy_pos(i)
                riseHpTop -= BattleSettings.hpRiseDelatY + \
                    BattleSettings.hpRiseSpeed*self.inEffectTimer
                self.draw_text(str(deltaHp), riseHpLeft, riseHpTop,
                               BattleSettings.hpRiseColor[sig], BattleSettings.hpRiseSize, BattleSettings.hpRiseFont)
                # print(riseHpLeft, riseHpTop)


class EnemyDialogue(Dialogue):
    def __init__(self, window, ID) -> None:
        super().__init__(window, ID)
        self.page = 0
        self.option = 0
        self.inBattle = False
        self.status = 1

    def tap(self, event, player, gen_map, *args):
        if self.inBattle == True:
            # self.status = self.battleScene.tap(event)
            if self.status != 1:
                if self.status == 0:
                    self.page = self.exeBattle(False)
                elif self.status == 2:
                    self.page = self.exeBattle(True)
                self.option = 0
                self.inBattle = False
        else:
            if event.key == pygame.K_RETURN:
                for execute in EnemyDetail.map[self.ID]["execute"][self.page][self.option]:
                    if isinstance(execute, ExePage):
                        self.page = execute.exe()
                        self.option = 0
                    elif isinstance(execute, ExeClose):
                        self.beEnter = False
                        player.info.modify("state", 0)
                    elif isinstance(execute, ExeBattle):
                        self.exeBattle = execute.exe
                        self.inBattle = True
                        self.battleScene = BattleScene(
                            self.window, self.ID, player, EnemyDetail.map[self.ID])
                    elif isinstance(execute, ExeMoney):
                        player = execute.exe(player)
                    elif isinstance(execute, ExeSave):
                        execute.exe(player)
                    elif isinstance(execute, ExeProcess):
                        player = execute.exe(player)
                    elif isinstance(execute, ExeRefresh):
                        gen_map(player.info.get_info("area"))
                    elif isinstance(execute, ExeAttribute):
                        player = execute.exe(player)
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.option > 0:
                    self.option -= 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if self.option + 1 < len(EnemyDetail.map[self.ID]["options"][self.page]):
                    self.option += 1
        return player

    def update(self, events):
        if self.inBattle == True:
            self.status = self.battleScene.update(events)
            # print(self.status)
            if self.status != 1:
                if self.status == 0:
                    self.page = self.exeBattle(False)
                elif self.status == 2:
                    self.page = self.exeBattle(True)
                self.option = 0
                self.inBattle = False

    def render(self):
        if self.inBattle:
            self.battleScene.render()
        elif self.beEnter:
            rect_surface = pygame.Surface(
                (DialogueSettings.bgWidth, DialogueSettings.bgHeight), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, DialogueSettings.bgColor,
                             (0, 0, DialogueSettings.bgWidth, DialogueSettings.bgHeight))
            pygame.draw.rect(rect_surface, DialogueSettings.chooseColor, (DialogueSettings.chooseX, DialogueSettings.chooseY + DialogueSettings.chooseSpace * self.option,
                                                                          DialogueSettings.chooseWidth, DialogueSettings.chooseHeight))
            self.window.blit(
                rect_surface, (DialogueSettings.bgX, DialogueSettings.bgY))

            img = pygame.transform.scale(
                pygame.image.load(EnemyDetail.map[self.ID]["img"][self.page]),
                EnemyDetail.map[self.ID]["scale"][self.page]
            )
            self.window.blit(img, EnemyDetail.map[self.ID]["imgxy"][self.page])

            text = EnemyDetail.map[self.ID]["text"][self.page]
            text = [text[i: i + DialogueSettings.rowLimit]
                    for i in range(0, len(text), DialogueSettings.rowLimit)]
            for i in range(len(text)):
                row_text = text[i]
                self.draw_text(row_text, DialogueSettings.textX, DialogueSettings.textY + i * DialogueSettings.rowSpace,
                               DialogueSettings.textColor, DialogueSettings.textSize, DialogueSettings.textFont)

            options = EnemyDetail.map[self.ID]["options"][self.page]
            for i in range(len(options)):
                option = "- " + options[i]
                self.draw_text(option, DialogueSettings.optionX, DialogueSettings.optionY + i * DialogueSettings.optionSpace,
                               DialogueSettings.textColor if i != self.option else DialogueSettings.textColor2,
                               DialogueSettings.textSize, DialogueSettings.textFont)


class BellDialogue(Board):
    def __init__(self, window, ID) -> None:
        super().__init__(window, ID)
        self.page = 0
        self.option = 0

    def enter(self, player):
        super().enter(player)
        self.page = 0
        self.option = 0

    def tap(self, event, player, gen_map, *args):
        if event.key == pygame.K_RETURN:
            for execute in BellDetail.map[self.ID]["execute"][self.page][self.option]:
                if isinstance(execute, ExeTP):
                    to_area = BellDetail.map[self.ID]["destination"]
                    player = ExeTP(BirthInfo.point[to_area][0], BirthInfo.point[to_area][1],
                                   dir=BirthInfo.direction[to_area], area=to_area).exe(player)
                    gen_map(to_area)
                    self.option = 0
                elif isinstance(execute, ExeClose):
                    self.beEnter = False
                    player.info.modify("state", 0)
                elif isinstance(execute, ExeProcess):
                    player = execute.exe(player)
                elif isinstance(execute, ExeAttribute):
                    player = execute.exe(player)
        elif event.key == pygame.K_w or event.key == pygame.K_UP:
            if self.option > 0:
                self.option -= 1
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            if self.option + 1 < len(BellDetail.map[self.ID]["options"][self.page]):
                self.option += 1
        return player

    def render(self):
        self.draw_block(BoardSettings.blockX, BoardSettings.blockY,
                        BoardSettings.blockWidth, BoardSettings.blockHeight, BoardSettings.blockColor)

        if self.beEnter == False:
            self.draw_text("按Enter键" + BellDetail.map[self.ID]["hint"], BoardSettings.hintX, BoardSettings.hintY,
                           BoardSettings.hintColor, BoardSettings.hintSize, BoardSettings.hintFont)
        if self.beEnter:
            rect_surface = pygame.Surface(
                (DialogueSettings.bgWidth, DialogueSettings.bgHeight), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, DialogueSettings.bgColor,
                             (0, 0, DialogueSettings.bgWidth, DialogueSettings.bgHeight))
            pygame.draw.rect(rect_surface, DialogueSettings.chooseColor, (DialogueSettings.chooseX, DialogueSettings.chooseY + DialogueSettings.chooseSpace * self.option,
                                                                          DialogueSettings.chooseWidth, DialogueSettings.chooseHeight))
            self.window.blit(
                rect_surface, (DialogueSettings.bgX, DialogueSettings.bgY))

            img = pygame.transform.scale(
                pygame.image.load(BellDetail.map[self.ID]["img"][self.page]),
                BellDetail.map[self.ID]["scale"][self.page]
            )
            self.window.blit(img, BellDetail.map[self.ID]["imgxy"][self.page])

            text = BellDetail.map[self.ID]["text"][self.page]
            text = [text[i: i + DialogueSettings.rowLimit]
                    for i in range(0, len(text), DialogueSettings.rowLimit)]
            for i in range(len(text)):
                row_text = text[i]
                self.draw_text(row_text, DialogueSettings.textX, DialogueSettings.textY + i * DialogueSettings.rowSpace,
                               DialogueSettings.textColor, DialogueSettings.textSize, DialogueSettings.textFont)

            options = BellDetail.map[self.ID]["options"][self.page]
            for i in range(len(options)):
                option = "- " + options[i]
                self.draw_text(option, DialogueSettings.optionX, DialogueSettings.optionY + i * DialogueSettings.optionSpace,
                               DialogueSettings.textColor if i != self.option else DialogueSettings.textColor2,
                               DialogueSettings.textSize, DialogueSettings.textFont)


class Shopping(Board):
    def __init__(self, window, ID) -> None:
        super().__init__(window, ID)

    def render(self):
        if self.beEnter == False:
            self.draw_text("按Enter键进入商店", BoardSettings.hintX, BoardSettings.hintY,
                           BoardSettings.hintColor, BoardSettings.hintSize, BoardSettings.hintFont)


class Treasure(Dialogue):
    def enter(self, player):
        super().enter(player)
        if self.ID not in player.info.get_info("treasure"):
            self.page = 0
        else:
            self.page = BoardDetail.map[self.ID]["startPage"]
        self.option = 0

    def tap(self, event, player, *args):
        if event.key == pygame.K_RETURN:
            for execute in BoardDetail.map[self.ID]["execute"][self.page][self.option]:
                if isinstance(execute, ExePage):
                    self.page = execute.exe()
                    self.option = 0
                elif isinstance(execute, ExeClose):
                    self.beEnter = False
                    player.info.modify("state", 0)
                elif isinstance(execute, ExeMoney):
                    if self.ID not in player.info.get_info("treasure"):
                        player = execute.exe(player)
                elif isinstance(execute, ExeProcess):
                    player = execute.exe(player)
                elif isinstance(execute, ExeAttribute):
                    player = execute.exe(player)
        elif event.key == pygame.K_w or event.key == pygame.K_UP:
            if self.option > 0:
                self.option -= 1
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            if self.option + 1 < len(BoardDetail.map[self.ID]["options"][self.page]):
                self.option += 1
        return player


class Anchor(Dialogue):
    def enter(self, player):
        super().enter(player)
        if self.ID not in player.info.get_info("anchor"):
            self.page = 0
        else:
            self.page = BoardDetail.map[self.ID]["startPage"]
        self.option = 0

    def tap(self, event, player, *args):
        if event.key == pygame.K_RETURN:
            for execute in BoardDetail.map[self.ID]["execute"][self.page][self.option]:
                if isinstance(execute, ExePage):
                    self.page = execute.exe()
                    self.option = 0
                elif isinstance(execute, ExeClose):
                    self.beEnter = False
                    player.info.modify("state", 0)
                elif isinstance(execute, ExeProcess):
                    player = execute.exe(player)
        elif event.key == pygame.K_w or event.key == pygame.K_UP:
            if self.option > 0:
                self.option -= 1
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            if self.option + 1 < len(BoardDetail.map[self.ID]["options"][self.page]):
                self.option += 1
        return player
