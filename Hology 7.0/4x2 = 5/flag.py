from itertools import permutations, combinations
from hashlib import sha512
from tqdm import tqdm

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

chars = b"aes?its_4E5!%7"

i = 0
possible = []
for perm in permutations(chars, 3):
    a, b, c = perm
    i += 1
    if perm not in possible:
        possible.append(perm)

possible_hashes = []
for a, b, c in possible:
    key = bytes([a, b, c])
    hash_value = sha512(key).digest()[:32]

    if hash_value not in possible_hashes:
        possible_hashes.append(hash_value)

plaintext = b"bbbbbbbbbbbbbbbb"
for comb in tqdm(combinations(possible_hashes, 4)):
    for key in comb:
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext)
        if ciphertext.hex() == "5191361fb39838f1175b897258bff838":
            print(key)
            print(ciphertext.hex())
            break
    else:
        continue
    break


print(len(possible_hashes))
