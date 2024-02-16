# -*- coding:utf-8 -*-

import pygame
import sys

import User
from Settings import *



class LoginScene:
    def __init__(self, window):
        # -1:None 0:Esc 1:Register 2:signIn
        self.loginState = 0
        self.chooseState = -1
        # -1:None 0:Esc 1:Username 2:Password
        self.signInState = -1
        # -1:None 0:Esc 1:Username 2:Nickname 3:Password
        self.registerState = -1
        self.WHITE = (255, 255, 255)
        # test
        self.BLACK = (250, 240, 240)
        # self.BLACK = (255, 240, 240)
        # self.BLACK = (0, 0, 0)
        self.window = window
        self.username = ""
        self.password = ""
        self.nickname = ""
        # 0:None 1:Success 2:Failed
        self.registerEnterState = 0
        # 0:None 1:Success 2:Failed
        self.signInEnterState = 0

    def user_have_login(self):
        if self.signInEnterState == 1:
            return True
        return False

    def get_user(self):
        return self.username

    def draw_text(self, text, color, x, y, fontSize = LoginSettings.wordSize, fontType = BasicSettings.fontPathSong, ifBold = False):
        font = pygame.font.Font(fontType, fontSize)
        font.set_bold(ifBold)
        surface = font.render(text, True, color)
        self.window.blit(surface, (x, y))

    def tap(self, event):
        if self.loginState == 0:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_1:
                self.loginState = 1
                self.registerState = -1
                self.username = ""
                self.password = ""
                self.nickname = ""
                self.registerEnterState = 0
            elif event.key == pygame.K_2:
                self.loginState = 2
                self.signInState = -1
                self.username = ""
                self.password = ""
                self.signInEnterState = 0

        elif self.loginState == 1:
            if event.key == pygame.K_UP:
                if self.registerState < 1:
                    self.registerState = 1
                elif self.registerState > 1:
                    self.registerState -= 1
            elif event.key == pygame.K_DOWN:
                if self.registerState < 1:
                    self.registerState = 3           # 最底下的状态
                elif self.registerState < 3:
                    self.registerState += 1
            elif event.key == pygame.K_ESCAPE:
                self.loginState = 0
            elif event.key == pygame.K_RETURN:
                if self.username != "" and self.nickname != "" and self.password != "":
                    respond = User.register(self.username, self.nickname, self.password)
                    if respond == True:
                        self.registerEnterState = 1
                    elif respond == False:
                        self.registerEnterState = 2
            elif event.key == pygame.K_BACKSPACE:
                if self.registerEnterState == 0:
                    if self.registerState == 1:
                        self.username = self.username[:-1]
                    if self.registerState == 2:
                        self.nickname = self.nickname[:-1]
                    if self.registerState == 3:
                        self.password = self.password[:-1]
            else: 
                if self.registerEnterState == 0:
                    char = event.unicode
                    if char.isupper() or char.islower() or char.isdigit():
                        if self.registerState == 1:
                            self.username += char
                        if self.registerState == 2:
                            self.nickname += char
                        if self.registerState == 3:
                            self.password += char

        elif self.loginState == 2:
            if event.key == pygame.K_UP:
                if self.signInState < 1:
                    self.signInState = 1
                elif self.signInState > 1:
                    self.signInState -= 1
            elif event.key == pygame.K_DOWN:
                if self.signInState < 1:
                    self.signInState = 2             # 最底下的状态
                elif self.signInState < 2:
                    self.signInState += 1
            elif event.key == pygame.K_ESCAPE:
                self.loginState = 0
            elif event.key == pygame.K_RETURN:
                if self.username != "" and self.password != "":
                    respond = User.signIn(self.username, self.password)
                    if respond == True:
                        self.signInEnterState = 1
                    elif respond == False:
                        self.signInEnterState = 2
            elif event.key == pygame.K_BACKSPACE:
                if self.signInEnterState == 0:
                    if self.signInState == 1:
                        self.username = self.username[:-1]
                    if self.signInState == 2:
                        self.password = self.password[:-1]
            else:
                if self.signInEnterState == 0:
                    char = event.unicode
                    if char.isupper() or char.islower() or char.isdigit():
                        if self.signInState == 1:
                            self.username += char
                        if self.signInState == 2:
                            self.password += char

    def LongBlack(self, color, number):
        p = max(0, 1 - number / 5)
        return (color[0] * p, color[1] * p, color[2] * p)

    def render(self):
        bg = pygame.image.load(LoginSettings.bg)
        self.window.blit(bg, (0, 0))
        if self.loginState == 0:
            pygame.display.set_caption("Choose~")
            self.draw_text("喜欢您来！请按键选择接下来去哪儿~", self.BLACK, LoginSettings.wordStartX, LoginSettings.wordStartY, ifBold = True)  
            self.draw_text("- 1: 注册", self.BLACK, LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.wordDeltaY * 1.5) 
            self.draw_text("- 2: 登录", self.BLACK, LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.wordDeltaY * 1.5 * 2)  
            self.draw_text("- Esc: 退出", self.BLACK, LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.wordDeltaY *1.5 * 3)  

        elif self.loginState == 1:
            suffix = "" if self.registerEnterState == 0 else "    成功！" if self.registerEnterState == 1 else "  用户名已存在！请返回上页后重新进入"
            self.draw_text("注册", self.BLACK, LoginSettings.titleStartX, LoginSettings.titleStartY,
                           LoginSettings.titleSize, ifBold = True)
            self.draw_text(suffix, self.BLACK, LoginSettings.titleStartX + LoginSettings.suffixDeltaX,
                           LoginSettings.titleStartY + LoginSettings.suffixDeltaY, LoginSettings.suffixSize)
            self.draw_text("用户名: " + self.username, self.LongBlack(self.BLACK, len(self.username)), LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY)
            self.draw_text("昵称: " + self.nickname, self.LongBlack(self.BLACK, len(self.nickname)), LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY + LoginSettings.wordDeltaY)
            self.draw_text("密码: " + self.password, self.LongBlack(self.BLACK, len(self.password)), LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY + LoginSettings.wordDeltaY * 2)
            if self.registerState < 1:
                pygame.display.set_caption("Register~")
            elif self.registerState == 1:
                pygame.display.set_caption("Register/username~")
                self.draw_text("> ", self.BLACK, LoginSettings.signX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY)
            elif self.registerState == 2:
                pygame.display.set_caption("Register/nickname~")
                self.draw_text("> ", self.BLACK, LoginSettings.signX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY + LoginSettings.wordDeltaY)  
            elif self.registerState == 3:
                pygame.display.set_caption("Register/password~")
                self.draw_text("> ", self.BLACK, LoginSettings.signX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY + LoginSettings.wordDeltaY * 2)
            self.draw_text("按上下键切换输入栏", self.BLACK, LoginSettings.tipsStartX,
                           LoginSettings.tipsStartY, LoginSettings.tipsSize, BasicSettings.fontPathKai)
            self.draw_text("按Esc返回上页", self.BLACK, LoginSettings.tipsStartX,
                           LoginSettings.tipsStartY + LoginSettings.tipsDeltaY, LoginSettings.tipsSize, BasicSettings.fontPathKai)
            self.draw_text("填完所有信息后按回车确认", self.BLACK, LoginSettings.tipsStartX,
                           LoginSettings.tipsStartY + LoginSettings.tipsDeltaY * 2, LoginSettings.tipsSize, BasicSettings.fontPathKai)

        elif self.loginState == 2:
            suffix = "" if self.signInEnterState == 0 else "    成功！" if self.signInEnterState == 1 else "  用户名或密码错误！请返回上页后重新进入"
            self.draw_text("登录", self.BLACK, LoginSettings.titleStartX, LoginSettings.titleStartY,
                           LoginSettings.titleSize, ifBold = True)
            self.draw_text(suffix, self.BLACK, LoginSettings.titleStartX + LoginSettings.suffixDeltaX,
                           LoginSettings.titleStartY + LoginSettings.suffixDeltaY, LoginSettings.suffixSize)
            self.draw_text("用户名: " + self.username, self.LongBlack(self.BLACK, len(self.username)), LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY)
            self.draw_text("密码: " + self.password, self.LongBlack(self.BLACK, len(self.password)), LoginSettings.wordStartX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY + LoginSettings.wordDeltaY)
            if self.signInState < 1:
                pygame.display.set_caption("SignIn~")
            elif self.signInState == 1:
                pygame.display.set_caption("SignIn/username~")
                self.draw_text("> ", self.BLACK, LoginSettings.signX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY)
            elif self.signInState == 2:
                pygame.display.set_caption("SignIn/password~")
                self.draw_text("> ", self.BLACK, LoginSettings.signX, 
                           LoginSettings.wordStartY + LoginSettings.titleDeltaY + LoginSettings.wordDeltaY)
            self.draw_text("按上下键切换输入栏", self.BLACK, LoginSettings.tipsStartX,
                           LoginSettings.tipsStartY, LoginSettings.tipsSize, BasicSettings.fontPathKai)
            self.draw_text("按Esc返回上页", self.BLACK, LoginSettings.tipsStartX,
                           LoginSettings.tipsStartY + LoginSettings.tipsDeltaY, LoginSettings.tipsSize, BasicSettings.fontPathKai)
            self.draw_text("填完所有信息后按回车确认", self.BLACK, LoginSettings.tipsStartX,
                           LoginSettings.tipsStartY + LoginSettings.tipsDeltaY * 2, LoginSettings.tipsSize, BasicSettings.fontPathKai)