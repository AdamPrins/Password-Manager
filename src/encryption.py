# first raw edit
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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

if __name__ == "__main__":
    ciphTxT = (encrypt("i hate mushrooms but broccooli is cool", "super_bad_password"))
    print(decrypt(ciphTxT, "super_bad_password"))
