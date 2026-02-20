#!/usr/bin/env python3
import socket
import sys
import binascii
import hashlib

from Crypto.Cipher import AES  # pip install pycryptodome

# ==========================
#  Challenge-specific config
# ==========================

HOST = "spawner.cscv.vn"
PORT = 33329

PHRASES = [
    b"One Ring to rule them all",
    b"One Ring to find them",
    b"One Ring to bring them all",
    b"and in the darkness bind them",
]

HEX_CHARS = b"0123456789abcdef"


# ================
#  Netcat wrapper
# ================


def recv_all_lines(sock):
    sock.settimeout(5.0)
    data = b""
    while True:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if b"FLAG:" in data:
                # server exits right after printing FLAG
                break
        except socket.timeout:
            break
    return data.decode(errors="ignore")


def connect_and_get_data():
    s = socket.create_connection((HOST, PORT))
    text = recv_all_lines(s)
    s.close()
    return text


# ================
#  Parsing helpers
# ================


def parse_from_text(text: str):
    """
    Expect lines like:
        q = <int>
        c1 = <int>
        c2 = <int>
        c3 = <int>
        c4 = <int>
        FLAG: <hex>
    """
    q = None
    cs = []
    flag_hex = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("q"):
            q = int(line.split("=", 1)[1].strip())
        elif line.startswith("c"):
            # c1 = ....
            parts = line.split("=", 1)
            val = int(parts[1].strip())
            cs.append(val)
        elif line.startswith("FLAG"):
            flag_hex = line.split(":", 1)[1].strip()

    if q is None or len(cs) != 4 or flag_hex is None:
        print("[!] Failed to parse server output:")
        print(text)
        raise ValueError("Could not parse q, 4 ciphertexts, and FLAG.")

    return q, cs, flag_hex


# ==========================
#  Message structure checks
# ==========================


def is_hex_bytes(b: bytes) -> bool:
    return all(ch in HEX_CHARS for ch in b)


def classify_message_bytes(m_bytes: bytes):
    """
    Returns:
      ("pure_hex", None)        if exactly 64 hex chars
      ("phrase_hex", phrase)    if phrase + 64 hex chars
      None                      if invalid
    """
    # pure hex: 64 bytes, all hex chars
    if len(m_bytes) == 64 and is_hex_bytes(m_bytes):
        return ("pure_hex", None)

    for phrase in PHRASES:
        Lp = len(phrase)
        if len(m_bytes) == Lp + 64 and m_bytes.startswith(phrase):
            hex_part = m_bytes[Lp:]
            if is_hex_bytes(hex_part):
                return ("phrase_hex", phrase)

    return None


# ==========================
#  Core math / reconstruction
# ==========================


def int_to_bytes(n: int) -> bytes:
    if n == 0:
        return b"\x00"
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, "big")


def recover_messages_from_x(q: int, cs: list[int], x: int):
    """
    Given q, list of c_i, and scalar x (which is a^{-1} mod q),
    compute m_i = (x * c_i mod q) - 1, convert to bytes, and
    check structure.

    Returns:
        list of tuples (m_int, m_bytes, kind, phrase_or_None)
    or raises ValueError if any message is invalid.
    """
    res = []
    for c in cs:
        m_int = (x * c) % q
        if m_int == 0:
            # then m = -1, impossible given generation
            raise ValueError("Invalid x: m_int == 0 (m = -1).")

        m_int = m_int - 1  # m = x*c mod q - 1

        m_bytes = int_to_bytes(m_int)
        classification = classify_message_bytes(m_bytes)
        if classification is None:
            raise ValueError("Invalid message structure for given x.")
        kind, phrase = classification
        res.append((m_int, m_bytes, kind, phrase))

    return res


# ==========================
#  AES key / IV / decryption
# ==========================


def derive_key_iv(messages_bytes: list[bytes]):
    """
    Reproduce Rust:
        key_material = m1_bytes || m2_bytes || m3_bytes || m4_bytes
        h = Sha256(key_material)
        aes_key = h[0..16]
        iv = h[16..32]
    """
    key_material = b"".join(messages_bytes)
    h = hashlib.sha256(key_material).digest()
    aes_key = h[:16]
    iv = h[16:32]
    return aes_key, iv


def aes_cbc_decrypt(cipher_hex: str, key: bytes, iv: bytes) -> bytes:
    ct = binascii.unhexlify(cipher_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    # PKCS#7 padding strip
    pad = pt[-1]
    if 1 <= pad <= 16 and pt.endswith(bytes([pad]) * pad):
        pt = pt[:-pad]
    return pt


# ==========================
#  X recovery stub (HNP)
# ==========================


def find_x(q: int, cs: list[int]) -> int:
    """
    This is the nontrivial part: solve for x = (s*(p+1))^{-1} mod q.

    From the Rust code we know:
        c_i mod q = a * (m_i + 1)   with a = s * (p+1) mod q
        => m_i = (x * c_i mod q) - 1 where x = a^{-1} mod q

    Each m_i (as bytes) is either:
        - 64 ASCII hex chars
        - phrase + 64 ASCII hex chars (phrase in PHRASES above)

    So x must be such that *all four* m_i satisfy that structure.

    Implement your Hidden Number Problem / lattice attack here.
    When done, return x as an integer in [1, q-1].

    For now this raises, so you can:
      - print(q, cs) and solve x in a separate Sage script, then
      - hard-code x here or pipe it in.
    """
    raise NotImplementedError("You need to implement the HNP / lattice solver for x.")


# ==========================
#  Main flow
# ==========================


def main():
    print(f"[+] Connecting to {HOST}:{PORT} ...")
    text = connect_and_get_data()
    print("[+] Raw server output:")
    print(text)

    q, cs, flag_hex = parse_from_text(text)
    print("[+] Parsed q:", q)
    print("[+] Parsed c's:", cs)
    print("[+] Parsed FLAG ciphertext:", flag_hex)

    # --- Solve for x (this is the only missing piece) ---
    x = find_x(q, cs)
    print("[+] Found x =", x)

    # --- Recover messages ---
    msgs = recover_messages_from_x(q, cs, x)
    m_bytes_list = []

    print("[+] Recovered messages:")
    for idx, (m_int, m_bytes, kind, phrase) in enumerate(msgs, start=1):
        print(f"  m{idx}: kind={kind}, len={len(m_bytes)}, phrase={phrase!r}")
        print(f"      bytes={m_bytes!r}")
        m_bytes_list.append(m_bytes)

    # --- Derive AES key & IV ---
    aes_key, iv = derive_key_iv(m_bytes_list)
    print(f"[+] AES key = {aes_key.hex()}")
    print(f"[+] IV      = {iv.hex()}")

    # --- Decrypt flag ---
    flag_pt = aes_cbc_decrypt(flag_hex, aes_key, iv)
    print(f"[+] Flag plaintext (raw): {flag_pt!r}")
    try:
        print("[+] Flag string:", flag_pt.decode())
    except UnicodeDecodeError:
        pass


if __name__ == "__main__":
    main()
