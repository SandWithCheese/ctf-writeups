from PIL import Image
from itertools import cycle


def xor(a, b):
    return [i ^ j for i, j in zip(a, cycle(b))]


with open("enc.txt", "rb") as f:
    enc = f.read()
    key = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
    dec = bytearray(xor(enc, key))
    with open("dec.png", "wb") as f:
        f.write(dec)
