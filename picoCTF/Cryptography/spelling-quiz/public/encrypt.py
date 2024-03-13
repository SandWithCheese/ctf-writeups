import random
import os

files = [
    os.path.join(path, file)
    for path, dirs, files in os.walk(".")
    for file in files
    if file.split(".")[-1] == "txt"
]

alphabet = list("abcdefghijklmnopqrstuvwxyz")
random.shuffle(shuffled := alphabet[:])
# shuffled is shuffled alphabet
dictionary = dict(zip(alphabet, shuffled))
# dictionary pairs the original alphabet with the shuffled alphabet

for filename in files:
    text = open(filename, "r").read()
    encrypted = "".join([dictionary[c] if c in dictionary else c for c in text])
    open(filename, "w").write(encrypted)

# kurchicine
# gocnfwnwtr
# kurchine = gocnfwtr
# malfeasor
# sxlyrxaic
# malfesor = sxlyric
# kurchinemalfeso = gocnfwtrsxlyri
