from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

with open("flag.enc", "rb") as f:
    data = f.read()
    iv = data[:16]
    ciphertext = data[16:]

for i in range(256):
    key = bytes([i]) * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    header = "137 80 78 71 13 10 26 10".split(" ")
    header = bytes([int(x) for x in header])
    if plaintext.startswith(header):
        with open("flag.png", "wb") as f:
            f.write(plaintext)
        break
