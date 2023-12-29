from hashlib import md5

md5hash = "f95b70fdc3088560732a5ac135644506"

with open("/usr/share/wordlists/rockyou.txt", "rb") as f:
    while True:
        payload = f.readline().strip()
        print(f"[*] Processing {payload}")
        pwd = md5(payload).hexdigest()
        if pwd == md5:
            print(payload.decode())
            break
