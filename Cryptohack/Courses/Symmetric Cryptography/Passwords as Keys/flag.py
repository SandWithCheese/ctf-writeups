import requests
import hashlib
from Crypto.Cipher import AES

with open("/usr/share/dict/words") as f:
    words = [w.strip() for w in f.readlines()]


url = "https://aes.cryptohack.org/passwords_as_keys/"

s = requests.Session()

flag = s.get(url=f"{url}encrypt_flag/").json()["ciphertext"]
flag = bytes.fromhex(flag)

for word in words:
    key = hashlib.md5(word.encode()).hexdigest()
    key = bytes.fromhex(key)
    cipher = AES.new(key, AES.MODE_ECB)
    if b"crypto" in cipher.decrypt(flag):
        # print(word)
        print(cipher.decrypt(flag).decode())
        break
