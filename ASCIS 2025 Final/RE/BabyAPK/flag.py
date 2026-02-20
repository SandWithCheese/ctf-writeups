import hashlib
import base64

from Crypto.Cipher import AES  # pip install pycryptodome


def hex_to_bytes(s: str) -> bytes:
    return bytes.fromhex(s)


def pkcs7_unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    # naive but fine for CTF
    return data[:-pad_len]


def derive_aes_key():
    # From MainActivity:
    # part1 = hex "736563725f70617274" -> "secr_part"
    # part2 = key_part_res from strings.xml -> "k3yRe5"
    # part3 = "1.0.0"
    part1 = "secr_part"
    part2 = "k3yRe5"
    part3 = "1.0.0"

    combined = (part1 + part2 + part3).encode("utf-8")
    return hashlib.sha256(combined).digest()  # 32-byte AES-256 key


def decrypt_sha256_target():
    key = derive_aes_key()

    # IV from hex: "2557127f6697dca3b9b02c85bc94d1ff"
    iv = hex_to_bytes("2557127f6697dca3b9b02c85bc94d1ff")

    # Ciphertext from Base64 in MainActivity
    ct_b64 = (
        "Rh5g13iNfXguQWeoMU9vVc1pvK6oC6/4zLm1aW8nqq/KWQ+GbYACDvBQ9pa75Vy6"
        "Rpah4UJunK5WRgwlmE/fcWEPrIKyyh6c/diJrXOGQW8="
    )
    ct = base64.b64decode(ct_b64)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    pt = pkcs7_unpad(pt)

    # This should be the expected SHA-256 hex of the correct 8-digit passkey
    sha256_target = pt.decode("utf-8")
    print("[*] Decrypted SHA-256 target:", sha256_target)
    return sha256_target


def find_passkey(sha256_target: str):
    print("[*] Brute forcing 8-digit passkey...")
    for i in range(100_000_000):
        candidate = f"{i:08d}"  # 00000000 .. 99999999
        h = hashlib.sha256(candidate.encode("utf-8")).hexdigest()
        if h == sha256_target:
            print("[+] Found passkey:", candidate)
            return candidate
    return None


def derive_flag(passkey: str) -> str:
    sha1_hex = hashlib.sha1(passkey.encode("utf-8")).hexdigest()
    flag = f"CSCV2025{{{sha1_hex}}}"
    return flag


def main():
    sha256_target = decrypt_sha256_target()
    passkey = find_passkey(sha256_target)

    if not passkey:
        print("[-] Passkey not found")
        return

    flag = derive_flag(passkey)
    print("[+] Flag:", flag)


if __name__ == "__main__":
    main()
