import subprocess
from string import printable


hashmap = dict()
for i in range(256):
    for j in range(256):
        payload = chr(i) + chr(j) + "g"
        with open("test.txt", "w") as f:
            f.write(payload)

        subprocess.run(["./netcompressor", "test.txt"])

        with open("test.netcomp", "rb") as f:
            brute = f.read()
            if brute == (bytes.fromhex("ca") + "g".encode()):
                print(payload)
                exit()

        if brute != payload.encode() and brute not in hashmap.values():
            hashmap[payload] = brute

print(hashmap.keys())
