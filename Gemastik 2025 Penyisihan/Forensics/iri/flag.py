import base64
import hashlib
from Crypto.Cipher import AES

CIPHER_KEY = "aewfoijdc887xc6qwj21t"

class AESCipher:
    def __init__(self, key: str):
        self.bs = 16
        self.key = hashlib.sha256(key.encode()).digest()
        print(self.key)

    def _unpad(self, s: bytes) -> bytes:
        return s[: -s[-1]]

    def decrypt(self, enc_b64: str) -> str:
        try:
            enc = base64.b64decode(enc_b64)
            iv = enc[: AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = self._unpad(cipher.decrypt(enc[AES.block_size :]))
            return decrypted.decode("utf-8", errors="ignore")
        except Exception as e:
            return f"[DECRYPTION ERROR] {e}"


cipher = AESCipher(CIPHER_KEY)


print("[+] Extracting TrevorC2 traffic...")

with open("beacons.txt", "r") as f:
    for line in f:
        if line.strip() == "":
            continue
        inner = base64.b64decode(line.strip()[4:]).decode()
        print("[CLIENT → SERVER]", cipher.decrypt(inner))

with open("responses.txt", "r") as f:
    for line in f:
        if line.strip() == "":
            continue
        print("[SERVER → CLIENT]", cipher.decrypt(line.strip()[7:]))
