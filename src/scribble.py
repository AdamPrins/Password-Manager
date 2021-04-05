import encryption
import json
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile)
# encryption.file_encrypter('data.txt', 'master')

def getByID(id):
    # creates file if not exists
    with open('data.txt', 'a') as json_file:
        pass

    # gets data from file if its there
    with open('data.txt') as json_file:
        try:
            data = encryption.file_decrypter('data.txt', 'tempkey')
            arr = data['data']
            for i in range(len(arr)):
                if(arr[i]['id'] == id):
                    return arr[i]
        except Exception as e:
            print(e)

def export_pw(id: int, file_name: str, key: str, pin: str):
    data = encryption.file_decrypter("data.txt", key)
    the_pw = getByID(id)

    #Decrypting data with masterkey
    for k, i in the_pw.items():
        if(k == 'id'):
            the_pw[k] = -1
        else:
            the_pw[k] = encryption.decrypt(i, key)

    #Encrypting Data with the pin
    for k, i in the_pw.items():
        if (k != 'id'):
            the_pw[k] = encryption.encrypt(i, pin)

    path = os.getcwd() + "/exportedpasswords/"

    if not os.path.exists(path):
        os.makedirs(path)
    #Adding encrypted password to a seperate file
    with open(path + file_name, 'a') as wf:
        json.dump(the_pw, wf)
    encryption.file_encrypter(path + file_name, pin)

####################################################################################################################################################################################
#Have to change the id for the password imported
def import_pw(file_name: str, key: str, pin: str):
    data = encryption.file_decrypter('data.txt', key)

    # Not sure why but this gets overwritten in the function...
    origkey = key

    # Decrypting encrypted data with pin
    new_data = encryption.file_decrypter(file_name, pin)
    for k, i in new_data.items():
        if(k != 'id'):
            new_data[k] = encryption.decrypt(i, pin)

    #Encrypting Data with the key
    for k, i in new_data.items():
        if(k != 'id'):
            new_data[k] = encryption.encrypt(i, key)

    #Deriving new id
    new_id = 0
    for items in data['data']:
        for key, item in items.items():
            if (key =='id'):
                if(item > new_id):
                    new_id = item
    new_id += 1

    #appending new id and the imported password to the main database
    new_data['id'] = new_id
    data['data'].append(new_data)


    with open('data.txt', 'w') as wf:
        json.dump(data, wf)

    encryption.file_encrypter('data.txt', origkey)
    return new_data
    #os.remove(file_name)

##################################################################################################################################################################################
# export_pw(3, 'data.txt', 'tempkey', 'the_pin')
#(import_pw('data_share.txt', 'tempkey', 'the_pin'))
