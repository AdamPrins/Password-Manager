import random
import os
import json
import base64
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encrypt(plaintext: str, key: str) -> str:
    key = pad(key.encode(), AES.block_size)
    plaintext = pad(plaintext.encode(), AES.block_size)
    iV = get_random_bytes(AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv=iV)
    result = cipher.encrypt(plaintext)
    return base64.b64encode(iV + result).decode("utf-8")

def decrypt(ciphertext: str, key: str) -> str:

    ciphertext = base64.b64decode(ciphertext)

    key = pad(key.encode(), AES.block_size)
    iV = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iV)
    result = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return result.decode()

def generateSalt() -> str:
    chars=[]
    for i in range(16):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)

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
