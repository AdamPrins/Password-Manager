import random
import os
import json
import base64
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encrypt(plaintext, key: str) -> str:
    key = pad(key.encode(), AES.block_size)

    if(isinstance(plaintext, str)):
        plaintext = pad(plaintext.encode(), AES.block_size)
    else:
        plaintext = pad(plaintext, AES.block_size)

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

def file_encrypter(file_name: str, key: str):
    lines = ''
    with open(file_name, 'r') as json_file:
        for line in json_file:
            line = line.encode()
            line = encrypt(line, key)
            lines += line

    with open(file_name, 'w') as output:
        for line in lines:
            output.write(line)

def file_decrypter(file_name: str, key: str):
    lines = ''
    with open(file_name, 'r') as inputy:
        for line1 in inputy:
            line1 = decrypt(line1, key)
            lines += (line1)

    arr = file_name.split("/")

    with open('temp_' + str(arr[-1]), 'w') as tempf:
        for line in lines:
            tempf.write(line)
    with open('temp_' + str(arr[-1]), 'r') as tempf2:
        data = json.load(tempf2)
    os.remove('temp_' + str(arr[-1]))
    return data

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
