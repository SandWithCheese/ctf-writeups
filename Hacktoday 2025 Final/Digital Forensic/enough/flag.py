#!/usr/bin/env python3
# decrypt_ransom.py
# Usage: python3 decrypt_ransom.py keyfile.bin encrypted.enc output.bin

import sys
from pathlib import Path


def rol(b, n):
    return ((b << n) & 0xFF) | (b >> (8 - n))


def ror(b, n):
    return ((b >> n) & 0xFF) | ((b << (8 - n)) & 0xFF)


def read_key(path):
    k = open(path, "rb").read()
    if len(k) != 32:
        raise SystemExit("Key file must be 32 bytes")
    return list(k)


def decrypt_block(block, key, chunk_offset):
    """Decrypts a single block of bytes (bytearray) inplace.
    block: bytearray of length N
    key: list of 32 ints (0-255)
    chunk_offset: integer (lVar5 at start of this block)
    """
    N = len(block)
    uVar2 = chunk_offset & 0xFFFFFFFF
    # Reverse order of transforms (10 -> 1)
    for idx in range(N):
        # J: XOR with ((idx & 7) + key[(idx*7 + uVar2) & 0x1f])
        val = block[idx]
        vj = ((idx & 7) + key[((idx * 7) + uVar2) & 0x1F]) & 0xFF
        val ^= vj

        # I: was rotr by 3 => undo with rol by 3
        val = rol(val, 3)

        # H: XOR with ((idx & 0xf) * 0x11 + 0xb)
        vh = (((idx & 0xF) * 0x11) + 0xB) & 0xFF
        val ^= vh

        # G: was val += (idx*3 + chunk_offset) => undo with subtraction
        addv = ((idx * 3) + (chunk_offset & 0xFF)) & 0xFF
        val = (val - addv) & 0xFF

        # F: XOR with key[(~uVar2 - idx) & 0x1f]
        # Note: ~uVar2 in C is bitwise not of 32-bit value; but indexing used &0x1f.
        # Use Python: (~uVar2 - idx) & 0x1f
        vf = key[((~uVar2 - idx) & 0x1F)] & 0xFF
        val ^= vf

        # E: was rotr by 2 => undo with rol by 2
        val = rol(val, 2)

        # D: XOR with (idx*13 + 7)
        vd = ((idx * 13) + 7) & 0xFF
        val ^= vd

        # C: was rol by 3 (left rotate) => undo with ror by 3
        val = ror(val, 3)

        # B: XOR with (chunk_offset + idx)
        vb = ((chunk_offset & 0xFF) + (idx & 0xFF)) & 0xFF
        val ^= vb

        # A: XOR with key[(uVar2 + idx) & 0x1f]
        va = key[((uVar2 + idx) & 0x1F)] & 0xFF
        val ^= va

        block[idx] = val
    return block


def decrypt_file(keyfile, encfile, outfile):
    key = read_key(keyfile)
    chunk_offset = 0  # lVar5 initial
    with open(encfile, "rb") as fi, open(outfile, "wb") as fo:
        while True:
            block = bytearray(fi.read(0x1000))
            if not block:
                break
            decrypt_block(block, key, chunk_offset)
            fo.write(block)
            chunk_offset += len(block)
    print("Decrypted ->", outfile)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 decrypt_ransom.py keyfile.bin encrypted.enc out.bin")
        sys.exit(1)
    decrypt_file(sys.argv[1], sys.argv[2], sys.argv[3])
