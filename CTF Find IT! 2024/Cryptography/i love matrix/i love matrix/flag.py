import numpy as np
from itertools import product

enc2_result = []
i = 1
while True:
    try:
        file_path = "./data/encrypted_flag" + str(i) + ".txt"
        matrix = np.loadtxt(file_path).reshape(4, 1)
        enc2_result.append(matrix)
        i += 1
    except OSError:
        break

print(len(enc2_result))

v = np.loadtxt("./data/v.txt", dtype=complex)
w = np.loadtxt("./data/w.txt", dtype=complex)


enc2_key = np.dot(w, np.dot(np.diag(v), np.linalg.inv(w)))
enc2_key = np.real(enc2_key)
enc2_key_inv = np.linalg.inv(enc2_key)

print(f"enc2_key: {enc2_key}")
print(f"enc2_key_inv: {enc2_key_inv}")

all_possible_vectors = []

for i in range(10):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                all_possible_vectors.append(
                    np.dot(enc2_key, np.array([i, j, k, l]).reshape(4, 1))
                )

original_enc2_result = []
i = 0
for res in enc2_result:
    for vector in all_possible_vectors:
        if np.allclose(res, vector % 26):
            original_enc2_result.append(np.round(np.dot(enc2_key_inv, vector)))
            print(i)

    i += 1
print(f"original_enc2_result: {original_enc2_result}")
print(len(original_enc2_result))

flag = ""
for res in original_enc2_result:
    for val in res:
        flag += str(int(val[0]))

print(f"flag: {flag}")
print(len(flag) % 4 == 0)
original_flag = flag

possible_10_part = product(range(10), repeat=4)
for part in possible_10_part:
    flag = flag[:40] + "".join(map(str, part)) + flag[40:]
    int_flag = int(flag)
    byte_flag = int_flag.to_bytes((int_flag.bit_length() + 7) // 8, "big")

    def enc1(message, key):
        return bytes([message[i] ^ key[i % len(key)] for i in range(len(message))])

    known_original = b"FindITCTF{"
    recovered_key = bytes(
        [known_original[i] ^ byte_flag[i] for i in range(len(known_original))]
    )

    decrypted_flag = enc1(byte_flag, recovered_key)
    try:
        decrypted_flag = decrypted_flag.decode()
        print(f"decrypted_flag: {decrypted_flag}")
    except UnicodeDecodeError:
        pass

    flag = original_flag
