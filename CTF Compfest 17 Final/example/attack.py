#!/usr/bin/env python3
"""
Per-challenge attack loop (independent process per challenge)

Features:
- Hot-reloads .env each tick (if python-dotenv installed)
- Per-target solver with timeout
- Exponential backoff for failing/patched hosts
- Deterministic (fixed) jitter before submission
- Multiple submits per tick (ATTACKS_PER_TICK), spaced to fit tick window
- Per-submit timeout guard (PER_SUBMIT_TIMEOUT_SECONDS) -> abort remaining submits on overrun
- JWT caching across ticks to reduce auth load
"""
import os
import sys
import time
import math
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Set, Optional
import aiohttp

# optional dependency for auto-reload .env
try:
    from dotenv import load_dotenv

    HAVE_DOTENV = True
except Exception:
    HAVE_DOTENV = False

# ---------- Logging ----------
logger = logging.getLogger("per_chall_attack")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(fmt)
logger.addHandler(sh)
# file handler added in get_config()

# ---------- State ----------
_next_attempt_tick: Dict[str, int] = {}
_failed_counts: Dict[str, int] = {}
_seen_flags_in_tick: Set[str] = set()


# ---------- Config helpers ----------
def reload_env(env_file: str = ".env") -> None:
    """Reload .env into process environment if python-dotenv is available."""
    if HAVE_DOTENV and Path(env_file).exists():
        load_dotenv(env_file, override=True)


def get_config() -> Dict[str, object]:
    """Return current config dict (reloads env and ensures file logger)."""
    reload_env()
    cfg = {
        "API_HOST": os.getenv("CTF_API_HOST", "https://api.ctf-compfest.com"),
        "TEAM_JWT": os.getenv("CTF_TEAM_JWT"),
        "EMAIL": os.getenv("CTF_EMAIL"),
        "PASSWORD": os.getenv("CTF_PASSWORD"),
        "TICK_SECONDS": int(os.getenv("TICK_SECONDS", "300")),
        "JITTER_SECONDS": float(os.getenv("JITTER_SECONDS", "10")),  # fixed delay
        "MAX_CONCURRENT": int(os.getenv("MAX_CONCURRENT", "8")),
        "SOLVER_CMD": os.getenv("SOLVER_CMD", "python3"),
        "SOLVER_PATH": os.getenv("SOLVER_PATH", "dist/solver.py"),
        "ENEMIES_FILE": os.getenv("ENEMIES_FILE", "enemys-ip.txt"),
        "ATTACK_LOG": os.getenv("ATTACK_LOG", "attack.log"),
        "BACKOFF_BASE_TICKS": int(os.getenv("BACKOFF_BASE_TICKS", "1")),
        "BACKOFF_MAX_TICKS": int(os.getenv("BACKOFF_MAX_TICKS", "12")),
        "SOLVER_TIMEOUT": int(os.getenv("SOLVER_TIMEOUT", "30")),
        "ATTACKS_PER_TICK": int(os.getenv("ATTACKS_PER_TICK", "1")),
        "SUBMIT_SAFETY_MARGIN_SECONDS": float(
            os.getenv("SUBMIT_SAFETY_MARGIN_SECONDS", "5")
        ),
        "PER_SUBMIT_TIMEOUT_SECONDS": float(
            os.getenv("PER_SUBMIT_TIMEOUT_SECONDS", "25")
        ),
    }
    # ensure file handler for logger uses current ATTACK_LOG
    log_path = Path(cfg["ATTACK_LOG"])
    if not log_path.parent.exists() and str(log_path.parent) != ".":
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # remove file handlers pointing to a different file
    for h in list(logger.handlers):
        if isinstance(h, logging.FileHandler):
            try:
                if os.path.realpath(h.baseFilename) != str(log_path.resolve()):
                    logger.removeHandler(h)
                    try:
                        h.close()
                    except Exception:
                        pass
            except Exception:
                logger.removeHandler(h)
                try:
                    h.close()
                except Exception:
                    pass

    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        fh = logging.FileHandler(str(log_path))
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return cfg


# ---------- Helpers ----------
def read_enemies(path: str) -> List[str]:
    p = Path(path)
    if not p.exists():
        logger.warning("Enemies file %s not found", path)
        return []
    lines = []
    for raw in p.read_text().splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    # dedupe while preserving order
    seen, out = set(), []
    for t in lines:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def note_failure(target: str, current_tick: int, cfg: Dict[str, object]) -> None:
    base = cfg["BACKOFF_BASE_TICKS"]
    mx = cfg["BACKOFF_MAX_TICKS"]
    c = _failed_counts.get(target, 0) + 1
    _failed_counts[target] = c
    skip = base * (2 ** (c - 1))
    if skip > mx:
        skip = mx
    _next_attempt_tick[target] = current_tick + skip
    logger.info(
        "Target %s failure=%d -> skip %d ticks (next=%d)",
        target,
        c,
        skip,
        _next_attempt_tick[target],
    )


def note_success(target: str) -> None:
    _failed_counts.pop(target, None)
    _next_attempt_tick.pop(target, None)


# ---------- Solver execution ----------
async def run_solver(target: str, cfg: Dict[str, object]) -> List[str]:
    """Run solver subprocess for a single target; kill on timeout/cancel."""
    if ":" not in target:
        logger.debug("Malformed target (no colon): %s", target)
        return []
    host, port = target.split(":", 1)
    solver_file = Path(cfg["SOLVER_PATH"])
    if not solver_file.exists():
        logger.error("Solver not found at %s", solver_file)
        return []
    proc = await asyncio.create_subprocess_exec(
        cfg["SOLVER_CMD"],
        str(solver_file),
        host,
        port,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=cfg["SOLVER_TIMEOUT"]
        )
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except Exception:
            pass
        await proc.wait()
        logger.warning("Solver timeout for %s", target)
        return []
    except asyncio.CancelledError:
        try:
            proc.kill()
        except Exception:
            pass
        await proc.wait()
        raise
    if proc.returncode != 0:
        logger.debug(
            "Solver returned non-zero (%d) for %s; stderr: %s",
            proc.returncode,
            target,
            stderr.decode(errors="ignore").strip(),
        )
        return []
    out = stdout.decode(errors="ignore").strip()
    if not out:
        return []
    flags = [line.strip() for line in out.splitlines() if line.strip()]
    return flags


# ---------- API helpers ----------
async def authenticate(session: aiohttp.ClientSession, cfg: Dict[str, object]) -> str:
    """Authenticate and return JWT token."""
    jwt = cfg["TEAM_JWT"]
    if jwt:
        return jwt
    if not cfg["EMAIL"] or not cfg["PASSWORD"]:
        raise RuntimeError("Missing TEAM_JWT and no EMAIL/PASSWORD")
    url = f"{cfg['API_HOST'].rstrip('/')}/api/v2/authenticate"
    payload = {"email": cfg["EMAIL"], "password": cfg["PASSWORD"]}
    async with session.post(url, json=payload, timeout=20) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Auth failed {resp.status}: {await resp.text()}")
        j = await resp.json()
        token = j.get("data")
        if not token:
            raise RuntimeError("Auth didn't return token")
        return token


async def submit_flags(
    session: aiohttp.ClientSession, jwt: str, cfg: Dict[str, object], flags: List[str]
) -> Dict[str, str]:
    """Single submit call with internal 429 backoff. (External per-submit timeout wraps this.)"""
    if not flags:
        return {}
    url = f"{cfg['API_HOST'].rstrip('/')}/api/v2/submit"
    headers = {"Authorization": f"Bearer {jwt}"} if jwt else {}
    payload = {"flags": flags}
    backoff, attempt = 1.0, 0
    while True:
        attempt += 1
        try:
            async with session.post(
                url, json=payload, headers=headers, timeout=30
            ) as resp:
                txt = await resp.text()
                if resp.status == 200:
                    try:
                        j = await resp.json()
                        data = j.get("data", [])
                        return {item.get("flag"): item.get("verdict") for item in data}
                    except Exception:
                        logger.exception("Failed to parse submit response: %s", txt)
                        return {}
                elif resp.status == 429:
                    logger.warning(
                        "Submit rate-limited (429). backoff %.1fs (attempt %d)",
                        backoff,
                        attempt,
                    )
                    await asyncio.sleep(backoff)
                    backoff = min(backoff * 2, 60.0)
                    continue
                elif resp.status in (401, 403):
                    logger.warning(
                        "Submit auth failed %d; will force re-auth next tick.",
                        resp.status,
                    )
                    return {}
                else:
                    logger.error("Submit failed %d: %s", resp.status, txt)
                    return {}
        except Exception as e:
            logger.exception("Submit error: %s", e)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60.0)
            if backoff > 60:
                return {}


# ---------- Tick processing ----------
async def process_tick(
    tick_num: int,
    session: aiohttp.ClientSession,
    cfg: Dict[str, object],
    cached_jwt: Optional[str],
) -> Optional[str]:
    """
    Process one tick. Returns updated cached_jwt (may be same as input or newly obtained).
    """
    tick_start = time.time()
    enemies = read_enemies(cfg["ENEMIES_FILE"])
    if not enemies:
        logger.info("Tick %d: no enemies listed", tick_num)
        return cached_jwt

    sem = asyncio.Semaphore(cfg["MAX_CONCURRENT"])
    found_flags: List[str] = []

    async def worker(target: str):
        if target in _next_attempt_tick and tick_num < _next_attempt_tick[target]:
            return
        async with sem:
            try:
                flags = await run_solver(target, cfg)
            except Exception:
                logger.exception("Solver crashed for %s", target)
                flags = []
            if not flags:
                note_failure(target, tick_num, cfg)
                return
            note_success(target)
            for f in flags:
                if f not in _seen_flags_in_tick:
                    _seen_flags_in_tick.add(f)
                    found_flags.append(f)

    await asyncio.gather(*(worker(t) for t in enemies))

    if not found_flags:
        logger.info("Tick %d: no flags", tick_num)
        return cached_jwt

    # FIXED (non-random) jitter from .env
    jitter = float(cfg["JITTER_SECONDS"])
    logger.info(
        "Tick %d: found %d flags, waiting fixed jitter=%.2fs before first submit",
        tick_num,
        len(found_flags),
        jitter,
    )
    await asyncio.sleep(jitter)

    # compute remaining time in this tick (from tick_start)
    elapsed = time.time() - tick_start
    tick_window = float(cfg["TICK_SECONDS"])
    safety = float(cfg["SUBMIT_SAFETY_MARGIN_SECONDS"])
    remaining = tick_window - elapsed - safety
    if remaining < 0:
        logger.warning(
            "Tick %d: not enough time left after jitter (remaining=%.2fs, safety=%.2fs). Submitting immediately.",
            tick_num,
            remaining,
            safety,
        )
        remaining = 0.0

    # number of submits we will perform (cannot exceed number of flags)
    desired_submits = int(cfg["ATTACKS_PER_TICK"])
    submit_count = max(1, min(desired_submits, len(found_flags)))

    # split flags into submit_count balanced chunks
    chunk_size = math.ceil(len(found_flags) / submit_count)
    chunks = [
        found_flags[i : i + chunk_size] for i in range(0, len(found_flags), chunk_size)
    ]
    if len(chunks) > submit_count:
        # merge trailing small chunks into last
        merged = []
        for c in chunks[: submit_count - 1]:
            merged.append(c)
        last = []
        for c in chunks[submit_count - 1 :]:
            last.extend(c)
        merged.append(last)
        chunks = merged

    # spacing between submits so last submit is inside the tick:
    # spread over (submit_count-1) gaps; if only 1 submit, no spacing used.
    intervals = max(1, submit_count - 1)
    spacing = remaining / intervals if intervals > 0 else 0.0
    logger.info(
        "Tick %d: will perform %d submit(s); spacing=%.2fs (safety=%.2fs, remaining=%.2fs)",
        tick_num,
        submit_count,
        spacing,
        safety,
        remaining,
    )

    # choose JWT: env-provided preferred; else cached; else auth now
    jwt_to_use = cfg.get("TEAM_JWT") or cached_jwt
    if not jwt_to_use:
        try:
            jwt_to_use = await authenticate(session, cfg)
        except Exception as e:
            logger.exception("Authentication failed before submit: %s", e)
            return None  # can't submit and no token cached

    per_submit_timeout = float(cfg["PER_SUBMIT_TIMEOUT_SECONDS"])

    # perform submissions with per-submit timeout guard
    for idx, batch in enumerate(chunks):
        if not batch:
            continue

        logger.info(
            "Tick %d: submitting batch %d/%d (size=%d)",
            tick_num,
            idx + 1,
            submit_count,
            len(batch),
        )

        try:
            # hard cap the total time we spend on this submit (including internal retries/backoff)
            results = await asyncio.wait_for(
                submit_flags(session, jwt_to_use, cfg, batch),
                timeout=per_submit_timeout,
            )
        except asyncio.TimeoutError:
            logger.warning(
                "Tick %d: submit batch %d timed out after %.2fs — aborting remaining submits this tick.",
                tick_num,
                idx + 1,
                per_submit_timeout,
            )
            break  # abort remaining submits this tick

        # handle auth failure case (submit returned empty because 401/403)
        if not results and (cfg.get("TEAM_JWT") is None):
            logger.info(
                "Tick %d: submit returned no results; attempting re-auth once.",
                tick_num,
            )
            try:
                jwt_to_use = await authenticate(session, cfg)
                cached_jwt = jwt_to_use
                # Optionally retry this same batch once after re-auth (guarded by timeout again)
                try:
                    results = await asyncio.wait_for(
                        submit_flags(session, jwt_to_use, cfg, batch),
                        timeout=per_submit_timeout,
                    )
                except asyncio.TimeoutError:
                    logger.warning(
                        "Tick %d: re-auth submit batch %d timed out after %.2fs — aborting remaining submits.",
                        tick_num,
                        idx + 1,
                        per_submit_timeout,
                    )
                    break
            except Exception:
                logger.exception(
                    "Tick %d: re-auth failed; aborting remaining submits.", tick_num
                )
                break

        # log verdicts (if any)
        for f, v in results.items():
            logger.info("Tick %d: %s -> %s", tick_num, f, v)

        # sleep spacing before next submit (if any)
        if idx < len(chunks) - 1 and spacing > 0:
            logger.debug(
                "Tick %d: sleeping %.2fs before next submit", tick_num, spacing
            )
            await asyncio.sleep(spacing)

    return cached_jwt


# ---------- Main loop ----------
async def main_loop():
    tick_num = 0
    cached_jwt: Optional[str] = None
    async with aiohttp.ClientSession() as session:
        while True:
            cfg = get_config()  # reload environment each tick
            start = time.time()
            try:
                cached_jwt = await process_tick(tick_num, session, cfg, cached_jwt)
            except Exception as e:
                logger.exception("Error on tick %d: %s", tick_num, e)
            tick_num += 1
            _seen_flags_in_tick.clear()
            elapsed = time.time() - start
            to_sleep = max(0, cfg["TICK_SECONDS"] - elapsed)
            logger.info("Tick %d finished; sleeping %.1fs", tick_num - 1, to_sleep)
            await asyncio.sleep(to_sleep)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Exiting.")
