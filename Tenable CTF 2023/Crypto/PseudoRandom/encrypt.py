import random
import time
import datetime
import base64

from Crypto.Cipher import AES

flag = b"find_me"
iv = b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"

for i in range(0, 16 - (len(flag) % 16)):
    flag += b"\0"

ts = time.time()
print(ts)

print(
    "Flag Encrypted on %s"
    % datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
)
seed = round(ts * 1000)
print(seed)

random.seed(seed)

key = []
for i in range(0, 16):
    key.append(random.randint(0, 255))

key = bytearray(key)


cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(flag)

print(base64.b64encode(ciphertext).decode("utf-8"))

# Flag Encrypted on 2023-08-02 10:27
# lQbbaZbwTCzzy73Q+0sRVViU27WrwvGoOzPv66lpqOWQLSXF9M8n24PE5y4K2T6Y