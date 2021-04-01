import encryption
import json
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile) 
# encryption.file_encrypter('data.txt', 'master')

# def export_pw(id: int, file_name: str, key: str):
#     with open(file_name, 'r') as f:
#         newData = {}
#         data = encryption.file_decrypter(file_name, key) 
#         print(data)
#         print()  
#         boool = False
#         for items in data['data']:
#             # print(items)
#             for key, item in items.items():
#                 if(key == 'id' and item == id):
#                     # print(item)
#                     boool = True
#                     break
#             if(boool):
#                 for key2, itemmmmmmm in items.items():
#                     if(key2 != 'id'):
#                         print((itemmmmmmm))
#                         item = encryption.decrypt(itemmmmmmm, 'qwerty123')
#                 add = []
#                 add.append(items)
#                 newData['data'] = add
#     print(newData)
#############################################################################################
            
# t1 = (encryption.encrypt('dogshitpooper', 'master'))
# print((t1))
# t2 = encryption.decrypt(t1, 'master')
# print(t2)
# def import_pw():
#Have to change the id for the password imported



export_pw(1, 'data.txt', 'master')












# {"data": [{"id": 1, "title": "jhabHx5aFwSPscypn+mGjhKHWUhgiYnt5JGfchOZWmM=", "username": "dp+YnVS6X/p8MTYawpjMhvQaRgfzYh0nyyfnMlFpncs=", "password": "3lh8naDdfam+GbFg2BTX+QJHt8DR15jQwZMnmMmCF81bvTODl9qaOXNEBdwyyqOY", "url": "kfUW5u4j15ECRoer5RHFaDk9K1y17BRJ3DEHqYc5ByU=", "notes": "OoJZzvDyfM/fg+xmONUUZsOt7mH9iIuGdAe3dbWd0Hw="}]}





















# # def encrypt_file(plaintext: bytes, key: str):
# #     key = pad(key.encode(), AES.block_size)
# #     plaintext = pad(plaintext, AES.block_size)
# #     iV = get_random_bytes(AES.block_size)
# #     cipher = AES.new(key, AES.MODE_CBC, iv=iV)
# #     result = cipher.encrypt(plaintext)
    
# #     return base64.b64encode(iV + result).decode("utf-8")

# # def decrypt_file(ciphertext: str, key: str): #not done
# #     ciphertext = base64.b64decode(ciphertext)

# #     key = pad(key.encode(), AES.block_size)
# #     iV = ciphertext[:AES.block_size]
# #     ciphertext = ciphertext[AES.block_size:]
# #     cipher = AES.new(key, AES.MODE_CBC, iV)
# #     result = unpad(cipher.decrypt(ciphertext), AES.block_size)
# #     return (result.decode())

# def file_encrypter(file_name: str, key: str):
#     lines = ''
#     with open(file_name, 'r') as json_file:
#         for line in json_file:
#             line = line.encode()
#             line = encryption.encrypt(line, key)
#             lines += line

#     with open(file_name, 'w') as output:
#         for line in lines:
#             output.write(line)

# def file_decrypter(file_name: str, key: str):
#     lines = ''
#     with open(file_name, 'r') as inputy:
#         for line1 in inputy:
#             line1 = encryption.decrypt(line1, key)
#             lines += (line1)
#     return lines

# file_encrypter('data.txt', 'master')
# print(file_decrypter('data.txt', 'master'))
