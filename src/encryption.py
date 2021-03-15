import random
import os
import json
from ui import View
from tkinter import *
from tkinter import ttk

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def getEntryFromWebsite(website):
    list = []
    with open('data.txt') as json_file:
        data = json.load(json_file)
        for p in data['data']:
            if p['website'] == website:
                list.append(p)

    return list

def getEntryFromUsername(username):
    list = []
    with open('data.txt') as json_file:
        data = json.load(json_file)
        for p in data['data']:
            if p['username'] == username:
                list.append(p)

    return list

def getEntryFromInfo(info):
    list = []
    with open('data.txt') as json_file:
        data = json.load(json_file)
        for p in data['data']:
            if p['info'] == info:
                list.append(p)

    return list


def generateSalt() -> str:
    chars=[]
    for i in range(16):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)


if __name__ == "__main__":

    #writePassword("test", "123", "www.google.com", "My favourite website")
    #writePassword("test", "123", "www.gmail.com")
    #print(getEntryFromWebsite("www.google.com"))

    #print(generateSalt())
    root = Tk()
    root.resizable(width=0, height=0)
    ui = View(root)

    mainloop()
