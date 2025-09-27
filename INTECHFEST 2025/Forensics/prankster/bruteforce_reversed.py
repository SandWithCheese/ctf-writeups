import json, re, binascii, sys
from collections import defaultdict
from itertools import permutations
import os
from tqdm import tqdm

FILES = [
    "0.txt.enc.000000",
    "0.txt.enc.000001",
    "0.txt.enc.000002",
    "0.txt.enc.000003",
    "0.txt.enc.000004",
    "0.txt.enc.000005",
    "0.txt.enc.000006",
    "0.txt.enc.000007",
    "0.txt.enc.000008",
    "0.txt.enc.000009",
    "0.txt.enc.000010",
    "0.txt.enc.000011",
    "0.txt.enc.000012",
    "0.txt.enc.000013",
    "0.txt.enc.000014",
]


for i in tqdm(range(pow(2, len(FILES)))):
    perm = [False] * len(FILES)
    for j in range(len(FILES)):
        if i & (1 << j):
            perm[j] = True

    chunks = {}
    with open("chunks.jsonl", "r") as f:
        for line in f:
            obj = json.loads(line)
            name = obj["chunk"]
            data = obj["data"]
            if name in perm:
                data = data[::-1]  # reverse the hex string
            chunks[name] = binascii.unhexlify(data)

    order = sorted(chunks, key=lambda x: int(re.search(r"(\d{6})$", x).group(1)))
    with open(f"bruteforce_results/cipher_combination_{i:05d}.bin", "wb") as out:
        for k in order:
            out.write(chunks[k])

    os.system(
        f"openssl enc -d -aes-256-cfb -K 2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945 -iv 524956415445204b45592d2d2d2d2d0a -in bruteforce_results/cipher_combination_{i:05d}.bin -out bruteforce_results/cipher_combination_{i:05d}.txt"
    )

    # If the decrypted file has INTECHFEST in it, print the combination ID
    with open(f"bruteforce_results/cipher_combination_{i:05d}.txt", "rb") as f:
        data = f.read()

    if b"INTECH" in data:
        print(f"Combination {i:05d} has INTECHFEST")
    else:
        os.remove(f"bruteforce_results/cipher_combination_{i:05d}.txt")
        os.remove(f"bruteforce_results/cipher_combination_{i:05d}.bin")

# # Chunks that were hex-reversed before exfil (from the capture):
# REVERSED = {
#     "0.txt.enc.000001",
#     "0.txt.enc.000002",
#     "0.txt.enc.000003",
#     "0.txt.enc.000006",
#     "0.txt.enc.000008",
#     "0.txt.enc.000009",
#     "0.txt.enc.000010",
#     "0.txt.enc.000013",
#     "0.txt.enc.000014",
# }
# # If your capture shows others, add them above.


# # Sanity: order by numeric suffix and warn for gaps
# order = sorted(chunks, key=lambda x: int(re.search(r"(\d{6})$", x).group(1)))
# print(order)
# missing = []
# if order:
#     first = int(re.search(r"(\d{6})$", order[0]).group(1))
#     last = int(re.search(r"(\d{6})$", order[-1]).group(1))
#     have = {int(re.search(r"(\d{6})$", k).group(1)) for k in order}
#     missing = [i for i in range(first, last + 1) if i not in have]
#     if missing:
#         sys.stderr.write(f"[!] Missing chunk indices: {missing}\n")

# with open("cipher.bin", "wb") as out:
#     for k in order:
#         print(chunks[k].hex())
#         out.write(chunks[k])
# print(
#     f"Wrote cipher.bin ({sum(len(v) for v in chunks.values())} bytes) from {len(order)} chunks."
# )
