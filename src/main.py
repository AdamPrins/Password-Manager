import random
import os
import json
from ui import View
from tkinter import *
from tkinter import ttk

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

if __name__ == "__main__":


    ui = View()

    ui.masterkey_popup()

    root = Tk()
    root.resizable(width=0, height=0)
    root.title('Password Manager')

    ui.main_popup(root)

    try:
        mainloop()
    except:
        pass
