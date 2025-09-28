#!/usr/bin/env python3
from PIL import Image
import sys, statistics, math

# CONFIG
IMG_PATH = "ZoomUpdaterPatch3.1.3.2.exe.png"  # <-- set to "ZoomUpdaterPatch3.1.3.2.exe.png" if you prefer
# If your file has a different name, change it here or pass via argv
if len(sys.argv) > 1:
    IMG_PATH = sys.argv[1]

im = Image.open(IMG_PATH).convert("RGB")
W, H = im.size
px = im.load()


# Detect yellow trace per column: pick the highest (smallest y) pixel that looks "yellow enough"
# Yellow heuristic: high R and G, low B relative to R/G, and brightness above a threshold.
def is_yellow(r, g, b):
    # robust to anti-aliasing glow; tune if needed
    return r > 150 and g > 150 and b < 80 and abs(r - g) < 40


trace_y = []
for x in range(W):
    y_hit = None
    # Scan vertically; the trace is thin, so first match from top is good
    for y in range(H):
        r, g, b = px[x, y]
        if is_yellow(r, g, b):
            y_hit = y
            break
    # Fallback: if no yellow in this column, try sampling a few rows and pick brightest
    if y_hit is None:
        # Search a small band: pick min y where r+g-b is max
        best = None
        for y in range(0, H, max(1, H // 200)):
            r, g, b = px[x, y]
            score = r + g - b
            if best is None or score > best[0]:
                best = (score, y)
        y_hit = best[1]
    trace_y.append(y_hit)


# Smooth the y to reduce occasional spikes
def median_filter(data, k=5):
    half = k // 2
    out = []
    for i in range(len(data)):
        win = data[max(0, i - half) : min(len(data), i + half + 1)]
        out.append(int(statistics.median(win)))
    return out


trace_y = median_filter(trace_y, k=5)

# Cluster into two levels (0/1) using simple 2-means (no deps)
low = min(trace_y)
high = max(trace_y)
c0, c1 = low, high
for _ in range(20):
    g0 = [y for y in trace_y if abs(y - c0) <= abs(y - c1)]
    g1 = [y for y in trace_y if abs(y - c1) < abs(y - c0)]
    if not g0 or not g1:
        break
    c0n = int(statistics.median(g0))
    c1n = int(statistics.median(g1))
    if c0n == c0 and c1n == c1:
        break
    c0, c1 = c0n, c1n
# Map: nearer to top (smaller y) is logical 1 (or 0). Try both later.
top = min(c0, c1)
bot = max(c0, c1)

raw_bits = []
for y in trace_y:
    bit = 1 if abs(y - top) < abs(y - bot) else 0
    raw_bits.append(bit)

# Determine bit-cell width via run-length peaks
runs = []
cur = raw_bits[0]
cnt = 1
for b in raw_bits[1:]:
    if b == cur:
        cnt += 1
    else:
        runs.append(cnt)
        cur = b
        cnt = 1
runs.append(cnt)

# The most common small run length is likely the bit-cell width
# (ignore very small spikes < 2 pixels wide)
candidates = {}
for r in runs:
    if r >= 2:
        candidates[r] = candidates.get(r, 0) + 1
# choose top few candidates
cand_sorted = sorted(candidates.items(), key=lambda kv: kv[1], reverse=True)
bit_width_guesses = [w for (w, _) in cand_sorted[:8]]


def sample_bits(bits, cell):
    out = []
    i = 0
    N = len(bits)
    while i + cell <= N:
        # majority vote within the cell
        chunk = bits[i : i + cell]
        out.append(1 if sum(chunk) >= len(chunk) / 2 else 0)
        i += cell
    return out


def bits_to_ascii(bits, msb_first=True):
    s = []
    for i in range(0, len(bits) - 7, 8):
        byte = bits[i : i + 8]
        if not msb_first:
            byte = list(reversed(byte))
        val = 0
        for b in byte:
            val = (val << 1) | b
        if 32 <= val <= 126:
            s.append(chr(val))
        else:
            s.append(".")
    return "".join(s)


print(f"[i] Image: {IMG_PATH} {W}x{H}")
print(f"[i] Top level (y): {top}, Bottom level (y): {bot}")
print("[i] Top bit-width guesses (run-length):", bit_width_guesses[:5])

# Try a sweep around each guessed width and both bit orders
tested = set()
for base in bit_width_guesses[:5]:
    for cell in range(max(2, base - 2), base + 3):
        for msb in (True, False):
            key = (cell, msb)
            if key in tested:
                continue
            tested.add(key)
            dec = bits_to_ascii(sample_bits(raw_bits, cell), msb_first=msb)
            # heuristic: if "flag{" or "ctf{" appears, highlight
            score = dec.count("flag{") + dec.count("ctf{") + dec.count("FLAG{")
            if score > 0:
                print(f"\n[+] *** HIT: cell={cell}, msb_first={msb} ***")
                print(dec)
            # also print a few top candidates for manual inspection
            elif base == bit_width_guesses[0] and cell in (base - 1, base, base + 1):
                print(f"\n[?] cell={cell}, msb_first={msb}")
                print(dec[:200])
print(
    "\n[i] If nothing obvious, try zooming the image (bicubic), re-run, or send me the script's stdout."
)
