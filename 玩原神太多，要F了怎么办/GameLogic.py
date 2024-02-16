# -*- coding:utf-8 -*-

import Settings
import Design
import random
import copy


def collidate(player, items):
    ifCollide = False
    meetObstacle = False
    collideType = []
    collideID = {}
    for entry in items:
        if entry == "Ground":       # 一条优化语句，不是很优美
            continue
        thisTypeCollide = False
        curID = []
        for item in items[entry]:
            if player.rect.colliderect(item.rect):
                if item.isObstacle or item.canInteract:
                    thisTypeCollide = True
                    if item.ID != "":
                        curID.append(item.ID)
                if item.isObstacle:
                    meetObstacle = True
        if thisTypeCollide == True:
            collideType.append(entry)
            collideID[entry] = curID
            ifCollide = True
    return ifCollide, collideType, collideID, meetObstacle


class Execute:
    def __init__(self) -> None:
        pass


class ExeClose(Execute):
    pass


class ExeOpenShop(Execute):
    pass


class ExePage(Execute):
    def __init__(self, page) -> None:
        super().__init__()
        self.page = page

    def exe(self):
        return self.page


class ExeMoney(Execute):
    def __init__(self, number, ifChange=False, useRate=False) -> None:
        super().__init__()
        self.number = number
        self.ifChange = ifChange
        self.useRate = useRate

    def catMoneyBuff(self, player):
        rate = 1.0
        unit = player.info.get_info("unit")
        for cat in unit:
            if cat != None:
                rate *= Design.CatCake.es[cat]["gold"] / 100
        return rate

    def exe(self, player):
        if self.ifChange:
            player.info.modify("money", self.number)
        else:
            number = self.number if self.useRate == False else int(
                self.number * player.info.get_info("gold") / 100 * self.catMoneyBuff(player))
            currentMoney = player.info.get_info("money")
            player.info.modify("money", currentMoney + number)
        return player


class ExeProcess(Execute):
    def __init__(self, entry, detail) -> None:
        super().__init__()
        self.entry = entry
        self.detail = detail

    def exe(self, player):
        if id not in player.info.get_info(self.entry):
            player.info.modify(self.entry, self.detail, ifExtend=True)
        return player


class ExeTP(Execute):
    def __init__(self, x, y, dir=1, area=-1) -> None:
        super().__init__()
        self.x, self.y = x * Settings.MapSettings.ground + \
            3, y * Settings.MapSettings.ground + 14
        self.dir = dir
        self.area = area

    def exe(self, player):
        player.info.modify("state", 0)
        player.rect.topleft = (self.x, self.y)
        player.updateInfoXY()
        if self.area != -1:
            player.info.modify("area", self.area)
        player.info.modify("direction", self.dir)
        return player


class ExeAttribute(Execute):
    def __init__(self, entry, value, ifPlus=True) -> None:
        super().__init__()
        self.entry = entry
        self.value = value
        self.ifPlus = ifPlus

    def exe(self, player):
        currentValue = player.info.get_info(self.entry)
        player.info.modify(self.entry, currentValue + self.value)
        return player


class ExeBattle(Execute):
    def __init__(self, winPage, losePage) -> None:
        super().__init__()
        self.winPage = winPage
        self.losePage = losePage

    def exe(self, ifWin):
        if ifWin == True:
            return self.winPage
        else:
            return self.losePage


class ExeSave(Execute):
    def __init__(self) -> None:
        super().__init__()

    def exe(self, player):
        player.save()


class ExeRefresh(Execute):
    def __init__(self) -> None:
        super().__init__()

    def exe(self):
        pass


'''
did=xxx
obj="self/enemy"
dic={
        "hp":{"apply":"hp","whose":"self/cake","num": xxx }
    }
前三个为按照自己/敌人的某一属性的百分比伤害
fix为固定伤害
'''


class ExeSkill(Execute):
    def __init__(self, did, obj, dic):
        super().__init__()
        self.did = did
        self.obj = obj
        self.dic = dic
        for key in dic.keys():
            self.key = key
            break

    def get_id(self, i, isAll, length):
        if isAll == True:
            return (i+length) % length
        else:
            return i

    def random_float(self):
        return random.randint(950, 1050)/1000

    def exe(self, nowCake, nowEnemy, cakeList, enemyList, whoseRound, isAll):
        operateList = {"cake": None, "self": None}

        if whoseRound == "PLAYER ROUND":
            if self.obj == "self":
                operateList["cake"] = copy.copy(cakeList)
                operateList["self"] = copy.copy(cakeList)
            else:
                operateList["cake"] = copy.copy(cakeList)
                operateList["self"] = copy.copy(enemyList)
        else:
            if self.obj == "self":
                operateList["cake"] = copy.copy(enemyList)
                operateList["self"] = copy.copy(enemyList)
            else:
                operateList["cake"] = copy.copy(enemyList)
                operateList["self"] = copy.copy(cakeList)

        operateObj = {"cake": nowCake,
                      "self": self.get_id(nowEnemy+self.did, isAll, len(operateList["self"]))}

        for key in self.dic.keys():
            if key == "hp":
                apply = self.dic[key]["apply"]
                whose = self.dic[key]["whose"]
                num = self.dic[key]["num"]
                if num < 0:
                    atk = 0
                    if apply == "fix":
                        atk = num
                    else:
                        atk = operateList[whose][operateObj[whose]
                                                 ].attribute[apply]*num

                    realAtk = int(
                        atk*atk/(atk-operateList["self"][operateObj["self"]].attribute["def"])*self.random_float())
                    if realAtk >= 0:
                        realAtk = -1

                    '''
                    realAtk = int(
                        (atk+0.5*operateList["self"][operateObj["self"]].attribute["def"])*self.random_float())
                    if realAtk >= 0:
                        realAtk = -1
                     '''
                    operateList["self"][operateObj["self"]
                                        ].attribute[key] += realAtk
                else:
                    if operateList["self"][operateObj["self"]].attribute["hp"] <= 0:
                        operateList["self"][operateObj["self"]
                                            ].attribute["hp"] = 0
                    else:
                        if apply == "fix":
                            operateList["self"][operateObj["self"]
                                                ].attribute[key] += int(num)
                        else:
                            operateList["self"][operateObj["self"]].attribute[key] += int(
                                operateList[whose][operateObj[whose]].attribute[apply]*num)

                if operateList["self"][operateObj["self"]].attribute["hp"] <= 0:
                    operateList["self"][operateObj["self"]].attribute["hp"] = 0

                if operateList["self"][operateObj["self"]].attribute["hp"] > operateList["self"][operateObj["self"]].attribute["fullHp"]:
                    operateList["self"][operateObj["self"]
                                        ].attribute["hp"] = operateList["self"][operateObj["self"]].attribute["fullHp"]
            else:
                apply = self.dic[key]["apply"]
                whose = self.dic[key]["whose"]
                num = self.dic[key]["num"]
                if apply == "fix":
                    operateList["self"][operateObj["self"]
                                        ].attribute[key] += int(num)
                else:
                    operateList["self"][operateObj["self"]].attribute[key] += int(
                        operateList[whose][operateObj[whose]].attribute[apply]*num)

        return [cakeList, enemyList]


'''
atk*atk/(atk+目标def）
再乘一个randomint（950,1050）/1000的随机浮动
'''
