# -*- coding:utf-8 -*-

import pygame
import sys

import User
import Login
import Player
import SceneManager
from Settings import *

# 登录界面


def login(window, clock):

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LogIn = Login.LoginScene(window)

    pygame.display.set_caption("Welcome~")

    Flag = False

    pygame.mixer.music.load(Music.login)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while True:

        clock.tick(BasicSettings.loginFps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                LogIn.tap(event)

        window.fill(WHITE)

        LogIn.render()

        if LogIn.user_have_login():
            pygame.mixer.music.stop()
            return LogIn.get_user()

        pygame.display.flip()


# 游戏运行
def run_game(window, clock, username):

    user = User.User(username)

    # pygame.display.set_caption(WindowSettings.name)
    pygame.display.set_caption("Hello user " + user.username)

    window.fill(SceneSettings.waterColor)

    sceneManager = SceneManager.SceneManager(window, user)
    sceneManager.gen_player()
    sceneManager.gen_map(user.info.get_info("area"))

    # 让player状态回归state0
    sceneManager.player.info.modify("state", 0)
    sceneManager.player.save()

    sceneManager.render()

    while True:

        clock.tick(BasicSettings.gameFps)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                sceneManager.player.info.modify("state", 0)
                sceneManager.player.save()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                sceneManager.tap(event)

        # 用水色做底
        window.fill(SceneSettings.waterColor)

        keys = pygame.key.get_pressed()

        sceneManager.update(keys, events)
        sceneManager.render()

        pygame.display.flip()


# 游戏整体初始化，进入login界面，进入rungame界面
def main():
    pygame.init()

    window = pygame.display.set_mode((WindowSettings.width,
                                      WindowSettings.height))

    clock = pygame.time.Clock()

    # 调试时注释

    user = login(window, clock)
    run_game(window, clock, user)

    # run_game(window, clock, "admin")


if __name__ == "__main__":
    main()
