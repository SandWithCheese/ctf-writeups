#!/usr/bin/env python3
import subprocess, re, sys, os, binascii, tempfile

SCAP = "challenge.scap" if len(sys.argv) < 2 else sys.argv[1]
OUT_PLAINTEXT = "0.txt.recovered"
OUT_CIPHERTEXT = "enc.bin"

# From the execve you pasted (exact hex):
KEYHEX = "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945"
IVHEX = "524956415445204b45592d2d2d2d2d0a"


def die(msg):
    print(f"[!] {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd):
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def get_execve_lines():
    """
    Try a narrow curl-only filter first; if nothing comes back, sweep all execve args.
    We only ever parse lines that contain 'curl' AND a -d { ... } payload.
    """
    fmt = r"%evt.time %evt.args"
    filters = [
        # 1) Most targeted
        ["sysdig", "-r", SCAP, "-p", fmt, "proc.name=curl and evt.type=execve"],
        # 2) Some traces name the process 'curl' in exeline only
        [
            "sysdig",
            "-r",
            SCAP,
            "-p",
            fmt,
            "evt.type=execve and (proc.exeline contains curl)",
        ],
        # 3) Last-resort broad sweep (can be noisy)
        ["sysdig", "-r", SCAP, "-p", fmt, "evt.type=execve"],
    ]
    lines = []
    for cmd in filters:
        try:
            out = run(cmd)
        except subprocess.CalledProcessError as e:
            continue
        # Keep only lines that clearly look like our curl POST with JSON
        for ln in out.splitlines():
            if (
                "curl " in ln
                and "-X POST" in ln
                and "-d" in ln
                and "{" in ln
                and '"data"' in ln
                and '"chunk"' in ln
            ):
                lines.append(ln)
        if lines:
            return lines
    return lines


def parse_posts(lines):
    posts = {}
    # Accept both quoted/unquoted -d spacing, any arg order
    rx = re.compile(
        r'(?s)-d\s*\{[^{}]*?"data"\s*:\s*"([0-9a-fA-F]+)".*?"chunk"\s*:\s*"([^"]+)"[^{}]*\}'
    )
    for ln in lines:
        m = rx.search(ln)
        if not m:
            continue
        hexdata, chunkname = m.group(1).lower(), m.group(2)
        m2 = re.search(r"(\d{6})$", chunkname)
        key = m2.group(1) if m2 else chunkname
        posts[key] = hexdata
    return posts


def rebuild_cipher(posts, workdir):
    if not posts:
        die("No POSTed chunks were found.")
    parts = []
    for key in sorted(posts, key=lambda k: (len(k), k)):
        revhex = posts[key][::-1]  # attacker used `rev`
        try:
            parts.append(binascii.unhexlify(revhex))
        except binascii.Error:
            die(f"Chunk {key}: invalid hex after reversing.")
    enc = b"".join(parts)
    enc_path = os.path.join(workdir, OUT_CIPHERTEXT)
    with open(enc_path, "wb") as f:
        f.write(enc)
    return enc_path


def decrypt(enc_path, out_plain):
    try:
        subprocess.check_call(
            [
                "openssl",
                "enc",
                "-d",
                "-aes-256-cfb",
                "-K",
                KEYHEX,
                "-iv",
                IVHEX,
                "-in",
                enc_path,
                "-out",
                out_plain,
            ]
        )
    except subprocess.CalledProcessError as e:
        die("OpenSSL decryption failed (likely missing or misordered chunks).")


def main():
    if not os.path.exists(SCAP):
        die(f"Missing scap: {SCAP}")
    print(f"[*] Reading: {SCAP}")
    lines = get_execve_lines()
    print(f"[*] Found {len(lines)} curl execve lines likely containing POSTs")

    posts = parse_posts(lines)
    if not posts:
        die('No JSON posts with "data"/"chunk" found in curl args.')
    print(f"[*] Extracted {len(posts)} chunks: {', '.join(sorted(posts))}")

    # Quick gap check
    nums = sorted([int(k) for k in posts if k.isdigit()])
    if nums:
        missing = [f"{n:06d}" for n in range(nums[0], nums[-1] + 1) if n not in nums]
        if missing:
            print(f"[!] Missing {len(missing)} chunk(s): {', '.join(missing)}")

    workdir = tempfile.mkdtemp(prefix="rebuild_")
    print(f"[*] Rebuilding ciphertext in {workdir}")
    enc_path = rebuild_cipher(posts, workdir)
    print(f"[+] Built ciphertext: {enc_path} ({os.path.getsize(enc_path)} bytes)")

    print("[*] Decrypting via OpenSSL AES-256-CFB…")
    out_plain = os.path.abspath(OUT_PLAINTEXT)
    decrypt(enc_path, out_plain)
    print(f"[+] Decrypted → {out_plain}")
    try:
        head = run(["head", "-n", "10", out_plain])
        print("----- preview -----")
        print(head.rstrip("\n"))
        print("-------------------")
    except Exception:
        pass
    print(f"[*] Ciphertext kept at: {enc_path}")


if __name__ == "__main__":
    main()
