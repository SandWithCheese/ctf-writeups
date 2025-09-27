#!/usr/bin/env python3
import re, sys, pathlib

# read the posts
src = pathlib.Path("posts.txt").read_text(errors="ignore")

# capture {"data":"<hex>","chunk":"<name>"}
# works even if there is other text around it
pat = re.compile(r'{"data":"([0-9a-fA-F]+)","chunk":"([^"]+)"}')

chunks = {}
for m in pat.finditer(src):
    hexdata, chunk = m.group(1).lower(), m.group(2)
    chunks[chunk] = hexdata

if not chunks:
    print("[!] No JSON posts with data/chunk found in posts.txt")
    sys.exit(1)


# sort by numeric suffix of the chunk name, e.g. 0.txt.enc.000011 -> 11
def chunk_index(c):
    m = re.search(r"(\d+)$", c)
    return int(m.group(1)) if m else -1


ordered = [chunks[k] for k in sorted(chunks, key=chunk_index)]

# build two variants:
#  - as-is (what was sent)
#  - reversed-hex-per-chunk (undo a prior 'rev' on the hex string)
as_is = bytes().join(bytes.fromhex(h) for h in ordered)
revd = bytes().join(bytes.fromhex(h[::-1]) for h in ordered)

open("cipher_as_is.bin", "wb").write(as_is)
open("cipher_rev.bin", "wb").write(revd)

print(f"[+] Parsed {len(ordered)} chunks")
print("[+] Wrote cipher_as_is.bin and cipher_rev.bin")
