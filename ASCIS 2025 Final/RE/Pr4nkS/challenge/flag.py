#!/usr/bin/env python3
from pathlib import Path
import string

# 1) Put ALL /get_latest_version bodies here (one per line)
CANDIDATE_KEYS = [
    "013a633584255c0d78589be545425531",
    "0a0e086d2926ed9cdf424060b4072b12",
    "0f66a9a6d4e56c63859829f6ea7366ef",
    "1d35d6ae010ceeb177e5de035417a3e7",
    "21710c789ff220099911fb06b20ebb1d",
    "2789c3b92e34ec454f449e5f224cf30d",
    "32d83bb6f3ad985fd4bc655b3d9acbe2",
    "4929df08b84ec071a84272449da8c96b",
    "6094bf5cb32d4d56f3f326d53f2cb3be",
    "621d1bfa0a9292d9c0e595902a9c3f76",
    "660479632a9fd95a762573c0abc5239b",
    "675a3d1a19508430e2fa3bb679158d45",
    "6d029d849a9581041ba5181c69b77cf1",
    "7402e9613104514de3ba51ef72e00c94",
    "79eeb31d16154cc17b58b13fb04fd670",
    "802a44e15e9586a463e96f7847aa0786",
    "83f569da507b8174ef0041deb557b32f",
    "93e41c6e20911b9b36bc7ce94edc677e",
    "97b6829e82c3a76cfc546f5df31ea004",
    "9f8e38b55c3677f0929a6500be0997bb",
    "a6b1de489e2b535c45388eb5509d77a9",
    "a6b727764515284e4446e42e611ca023",
    "b0a0e6f7387ce0f2369d71d23e45465b",
    "c62777a27a768bce69ac9e2701c51195",
    "cb8865c2e9062745acb456e121727016",
    "d2612038b6a32a75474e2db76ed15a7c",
    "d77d8f66ccf252738b208a8bb5e1716e",
    "da412b6b6b4e86239cbdbccb0861bede",
    "e26010f82227a55127ec5aa9154410ca",
    "ea225ece75398462e891a202b1e8ff26",
    "ea57b44baa8e25c53488900406ecc3d7",
    "f46edce63f791f9f1d1edc6226d04fa7",
]


def rc4_ksa(key: bytes):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    return S


def rc4_prga(S, n):
    i = j = 0
    out = bytearray()
    for _ in range(n):
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        out.append(S[(S[i] + S[j]) & 0xFF])
    return bytes(out)


def rc4(key: bytes, data: bytes) -> bytes:
    S = rc4_ksa(key)
    ks = rc4_prga(S, len(data))
    return bytes(d ^ k for d, k in zip(data, ks))


def score(buf: bytes) -> float:
    # crude "how printable" score for first 256 bytes
    window = buf[:256]
    printable = sum(1 for b in window if chr(b) in string.printable)
    return printable / max(1, len(window))


def main():
    data = Path("update.bin").read_bytes()

    out_dir = Path("decrypted_candidates")
    out_dir.mkdir(exist_ok=True)

    for k in CANDIDATE_KEYS:
        key_bytes = k.encode("ascii")  # IMPORTANT: use ASCII string as RC4 key
        dec = rc4(key_bytes, data)

        # Quick heuristics
        head = dec[:64]
        s = score(dec)
        print(f"[+] Key {k}: score={s:.2f}, head={head[:16].hex()}")

        # If it looks promising (high printable ratio or 'MZ', 'PK', 'flag{', etc),
        # dump it for manual inspection.
        if dec.startswith(b"MZ") or dec.startswith(b"PK") or b"flag{" in dec or s > 0.7:
            out_file = out_dir / f"update_dec_{k}.bin"
            out_file.write_bytes(dec)
            print(f"    -> dumped to {out_file}")


if __name__ == "__main__":
    main()
