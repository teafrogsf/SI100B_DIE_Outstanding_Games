import sys
import pygame
import random
from Settings import *
from typing import *


class Blackjack:
    def __init__(self, player, window, fontSize: int = BattleSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255)):
        # 加载背景音乐和图片
        self.background_image = pygame.image.load(r".\assets\cards\55.png")
        self.background_image = pygame.transform.scale(self.background_image, (1280, 720))
        self.back_image = pygame.transform.scale(pygame.image.load(r".\assets\cards\56.png"), (PlayerSettings.backwidth,
                                                                                               PlayerSettings.backheight))
        self.card_images = [pygame.transform.scale(pygame.image.load(img), (PlayerSettings.cardswidth,
                                                                            PlayerSettings.cardsheight)) for img in
                            GamePath.card_images]
        self.moneyImage = pygame.transform.scale(pygame.image.load(GamePath.player_Money),
                                                 (PlayerSettings.heartWidth, PlayerSettings.heartHeight))

        self.window = window
        self.isFinished = False
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)
        self.player = player
        self.money = 0

        # 发牌
        self.handcard = [[], []]

    def deal_card(self, handcard):
        index = random.randint(0, 51)
        if self.card_images[index]:
            card = self.card_images[index]
            self.card_images[index] = None
            #############
            if index < 4:
                handcard.append('A')
            elif index < 20:
                handcard.append(10)
            elif index < 24:
                handcard.append(9)
            elif index < 28:
                handcard.append(8)
            elif index < 32:
                handcard.append(7)
            elif index < 36:
                handcard.append(6)
            elif index < 40:
                handcard.append(5)
            elif index < 44:
                handcard.append(4)
            elif index < 48:
                handcard.append(3)
            else:
                handcard.append(2)
            ############
            return card
        else:
            return self.deal_card(handcard)

    # 显示牌
    def show_card(self, card, x, y):
        self.window.blit(card, (x, y))

    def get_score(self, handcard: list):  # 计算分数
        score = 0
        for num in handcard:
            if type(num) == int:
                score += num
        A_count = handcard.count('A')
        score += A_count
        for _ in range(A_count):
            if score + 10 <= 21:
                score += 10
        return score

    def get_result(self):  # 获取游戏结果
        player_score = self.get_score(self.handcard[0])
        dealer_score = self.get_score(self.handcard[1])
        if player_score > 21 and dealer_score <= 21:
            self.window.blit(self.moneyImage, (570, 290))
            self.window.blit(self.font.render('U fail!               - 15', True, self.fontColor),
                             (400, 300))
            self.money = -15
            self.isFinished = True
        if player_score <= 21 and dealer_score > 21:
            self.window.blit(self.moneyImage, (570, 290))
            self.window.blit(self.font.render('U win!                + 15', True, self.fontColor),
                             (400, 300))
            self.money = 15
            self.isFinished = True
        if player_score > 21 and dealer_score > 21:
            self.window.blit(self.font.render('Tie game! Play again~', True, self.fontColor),
                             (400, 300))
            self.isFinished = True
        if player_score <= 21 and dealer_score <= 21 and self.isFinished:
            if player_score < dealer_score:
                self.window.blit(self.moneyImage, (570, 290))
                self.window.blit(self.font.render('U fail!               - 15', True, self.fontColor),
                                 (400, 300))
                self.money = -15
            if player_score > dealer_score:
                self.window.blit(self.moneyImage, (570, 290))
                self.window.blit(self.font.render('U win!                + 15', True, self.fontColor),
                                 (400, 300))
                self.money = 15
            if player_score == dealer_score:
                self.window.blit(self.font.render('Tie game! Play again~', True, self.fontColor),
                                 (400, 300))

    def run_game(self):
        # 玩家和庄家发牌
        m1 = self.deal_card(self.handcard[0])
        m2 = self.deal_card(self.handcard[1])
        m3 = self.deal_card(self.handcard[0])
        m4 = self.deal_card(self.handcard[1])
        player_cards = [m1, m3]
        dealer_cards = [m2, m4]
        running = True
        self.window.blit(self.background_image, (0, 0))
        n1 = 0
        n2 = 0
        self.show_card(self.back_image, 100, 100)
        self.show_card(self.back_image, 350, 100)

        while running:

            # 显示玩家和庄家的牌
            self.show_card(player_cards[0], 100, 500)
            self.show_card(player_cards[1], 350, 500)
            # 处理玩家操作
            if not self.isFinished:
                self.window.blit(self.font.render('Press T to draw a card', True, (0, 0, 0)),
                                 (800, 300))
                self.window.blit(self.font.render('Press f to flop all cards', True, (0, 0, 0)),
                                 (800, 350))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # 检测按键按下事件
                    if event.key == pygame.K_t and not self.isFinished:
                        player_cards.append(self.deal_card(self.handcard[0]))
                        n1 += 1
                        dealer_choice = random.randint(0, 1)
                        if dealer_choice == 1:
                            dealer_cards.append(self.deal_card(self.handcard[1]))
                            n2 += 1
                            self.show_card(self.back_image, (350 + 250 * n2), 100)
                        else:
                            pass
                        self.show_card(player_cards[-1], (350 + 250 * n1), 500)

                    elif event.key == pygame.K_f and not self.isFinished:
                        dealer_choice = random.randint(0, 1)
                        if dealer_choice == 1:
                            dealer_cards.append(self.deal_card(self.handcard[1]))
                            n2 += 1
                            self.show_card(self.back_image, (350 + 250 * n2), 100)
                        self.isFinished = True

                    elif event.key == pygame.K_RETURN and self.isFinished:
                        self.player.attr_update(addCoins=self.money)
                        running = False

            # 计算点数并判断输赢
            self.get_result()
            # 处理游戏结束
            if self.isFinished:
                for i in range(len(dealer_cards)):
                    self.show_card(dealer_cards[i - 1], (100 + 250 * i), 100)
                self.window.blit(self.font.render('Press ENTER to continue', True, self.fontColor),
                                 (WindowSettings.width // 2 - 200, WindowSettings.height - 65))

            pygame.display.flip()
