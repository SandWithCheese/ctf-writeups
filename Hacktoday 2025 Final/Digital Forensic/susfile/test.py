#!/usr/bin/env python3
import re
import olefile  # pip install olefile

PATH = "extracted/vbaProject.bin"
ole = olefile.OleFileIO(PATH)


def sid_for(path_list):
    de = ole._find(path_list)  # may return SID (int) or DirEntry
    if isinstance(de, int):
        return de
    else:
        return ole.direntries.index(de)


rows = []
for p in ole.listdir(streams=True):  # e.g., ['VBA','ThisWorkbook']
    full = "/".join(p)
    if not full.startswith("VBA/"):
        continue
    if full in ("VBA/dir", "VBA/_VBA_PROJECT"):
        continue

    sid = sid_for(p)  # 0-based index into direntries
    idx = sid + 1  # oledump prints 1-based

    data = b""
    try:
        data = ole.openstream(p).read()
    except Exception:
        pass

    # Heuristic: treat as "has code" only if it contains a Sub/Function
    has_code = bool(re.search(rb"\b(Sub|Function)\b", data))
    size = len(data)
    tag = "M" if has_code else "m"
    rows.append((idx, tag, size, full))

for idx, tag, size, full in sorted(rows, key=lambda r: r[0]):
    print(f"{idx:3d}: {tag}  {size:7d}  {full}")
