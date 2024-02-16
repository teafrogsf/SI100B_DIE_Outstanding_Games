# -*- coding:utf-8 -*-

import pygame
import json

from Info import *
from Settings import *

def load_users():
    with open(BasicSettings.userfile, "r") as file:
        return json.load(file)

def save_users(users):
    with open(BasicSettings.userfile, "w") as file:
        json.dump(users, file)

def register(username, nickname, password):
    users = load_users()
    if username in users:
        return False
    else:
        users[username] = Info().info
        users[username]["basic"]["nickname"] = nickname
        users[username]["basic"]["password"] = password
        save_users(users)
        return True
    
def signIn(username, password):
    users = load_users()
    if username not in users:
        return False
    else:
        if users[username]["basic"]["password"] == password:
            return True
        else:
            return False
        
class User:
    def __init__(self, username):
        users = load_users()
        self.info = Info(info = users[username])
        # print(self.info)
        self.username = username

    def saveInfo(self, info):
        users = load_users()
        users[self.username] = info.info
        self.info = info
        save_users(users)