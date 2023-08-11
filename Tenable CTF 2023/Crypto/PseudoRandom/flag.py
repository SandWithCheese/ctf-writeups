# 1690943220000 - 1690943280000
# 1690986420000 - 1690986480000

from Crypto.Cipher import AES
import random
import base64
import datetime

iv = b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
flag = "lQbbaZbwTCzzy73Q+0sRVViU27WrwvGoOzPv66lpqOWQLSXF9M8n24PE5y4K2T6Y"
flag = base64.b64decode(flag)
print(flag)

count = 0
for seed in range(1690986420000, 1690986480000):
    random.seed(seed)
    # print(
    #     "Flag Encrypted on %s"
    #     % datetime.datetime.fromtimestamp(seed // 1000).strftime("%Y-%m-%d %H:%M")
    # )

    key = []
    for i in range(0, 16):
        key.append(random.randint(0, 255))

    key = bytearray(key)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(flag)

    if b"flag" in plaintext:
        print(plaintext)
        break

    count += 1
    print(count)
