from itertools import permutations
from tqdm import tqdm


def encrypt(msg, key):
    keylen = len(key)

    m = ""
    for i in key:
        j = i
        while j < len(msg):
            m += msg[j]
            j += keylen

    return m


with open("pesan.txt", "r") as f:
    m = f.read().strip()
    print("Message:", m)

with open("rahasia.txt", "r") as f:
    secret = f.read().strip()
    print("Secret:", secret)

assert len(m) == len(secret)


def check_similarity(m, secret):
    score = 0
    for i in range(len(m)):
        if m[i] == secret[i]:
            score += 1
    return score


key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
keylen = len(key)
max_score = 0
enc = ""
for perm in tqdm(permutations(key)):
    if list(perm) == [2, 8, 7, 1, 4, 0, 9, 3, 6, 5]:
        print("Found key:", perm)

    message = encrypt(m, list(perm))
    score = check_similarity(message, secret)
    if score >= max_score:
        max_score = score
        best_key = perm
        enc = message
        print("Best key:", best_key)
        print("Max score:", max_score)
        print("Encrypted message:", message)


def decrypt(enc_msg, key):
    keylen = len(key)
    msg_len = len(enc_msg)

    original_msg = [""] * msg_len

    enc_index = 0

    for i in key:
        col_start = i
        row = 0
        while col_start + row * keylen < msg_len and enc_index < len(enc_msg):
            original_msg[col_start + row * keylen] = enc_msg[enc_index]
            enc_index += 1
            row += 1

    return "".join(original_msg)


print("Encrypted message:", message)
print("Decrypted message:", decrypt(secret, best_key))
