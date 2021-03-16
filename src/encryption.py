import random
import os
import json
from ui import View
from tkinter import *
from tkinter import ttk
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encrypt(plaintext: str, key: str) -> bytes:
    key = pad(key.encode(), AES.block_size)
    plaintext = pad(plaintext.encode(), AES.block_size)
    iV = get_random_bytes(AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv=iV)
    result = cipher.encrypt(plaintext)
    return iV + result

def decrypt(ciphertext: bytes, key: str) -> str:
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


if __name__ == "__main__":

    #writePassword("test", "123", "www.google.com", "My favourite website")
    #writePassword("test", "123", "www.gmail.com")
    #print(getEntryFromWebsite("www.google.com"))
    #ciphTxT = (encrypt("i hate mushrooms but broccooli is cool", "super_bad_password"))
    #print(decrypt(ciphTxT, "super_bad_password"))
    #print(generateSalt())
    root = Tk()
    root.resizable(width=0, height=0)
    root.title('Password Manager')
    ui = View(root)

    mainloop()

