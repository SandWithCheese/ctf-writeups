import json, re, binascii, sys
from collections import defaultdict

# Chunks that were hex-reversed before exfil (from the capture):
REVERSED = {
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
}
# If your capture shows others, add them above.

chunks = {}
with open("chunks.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)
        name = obj["chunk"]
        data = obj["data"]
        if name in REVERSED:
            print(f"Reversing {name}")
            # print(data)
            data = data[::-1]  # reverse the hex string
            # print(data)
        chunks[name] = binascii.unhexlify(data)


# Sanity: order by numeric suffix and warn for gaps
order = sorted(chunks, key=lambda x: int(re.search(r"(\d{6})$", x).group(1)))
print(order)
missing = []
if order:
    first = int(re.search(r"(\d{6})$", order[0]).group(1))
    last = int(re.search(r"(\d{6})$", order[-1]).group(1))
    have = {int(re.search(r"(\d{6})$", k).group(1)) for k in order}
    missing = [i for i in range(first, last + 1) if i not in have]
    if missing:
        sys.stderr.write(f"[!] Missing chunk indices: {missing}\n")

with open("cipher.bin", "wb") as out:
    for k in order:
        out.write(chunks[k])
print(
    f"Wrote cipher.bin ({sum(len(v) for v in chunks.values())} bytes) from {len(order)} chunks."
)
