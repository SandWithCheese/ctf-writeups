from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1] :]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode("ascii")
    else:
        return plaintext.decode("ascii")


shared_secret = 1547922466740669851136899009270554812141325611574971428561894811681012510829813498961168330963719034921137405736161582760628870855358912091728546731744381382987669929718448423076919613463237884695314172139247244360699127770351428964026451292014069829877638774839374984158095336977179683450837507011404610904412301992397725594661037513152497857482717626617522302677408930050472100106931529654955968569601928777990379536458959945351084885704041496571582522945310187
iv = "737561146ff8194f45290f5766ed6aba"
ciphertext = "39c99bf2f0c14678d6a5416faef954b5893c316fc3c48622ba1fd6a9fe85f3dc72a29c394cf4bc8aff6a7b21cae8e12c"

print(decrypt_flag(shared_secret, iv, ciphertext))
