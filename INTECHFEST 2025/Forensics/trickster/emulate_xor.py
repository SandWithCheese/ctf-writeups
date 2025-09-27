# multi_stage_patch.py
from pathlib import Path
from Crypto.Cipher import AES
import struct

# --- 0) Load ciphertext and AES-decrypt exactly like your working attempt ---
ct = Path("projekmatkul-main/libutama.so").read_bytes()

# This is the variant you used that yielded the stub-looking plaintext.
key = b"f8b8c95092dfbbaee917884d866e4401"  # 32 ASCII -> AES-256
iv = b"e54c750c6a8bd188"  # 16 ASCII
# If later we confirm the true key/iv are hex-encoded, we can switch to bytes.fromhex(...)

pt = bytearray(AES.new(key, AES.MODE_CBC, iv).decrypt(ct))
print(f"[i] decrypted len = {len(pt)} bytes")


# --- 1) Scan-and-apply all mini stubs we can find ---
def find(buf, pat, start):
    i = buf.find(pat, start)
    return i


APPLIED = 0
pos = 0
while True:
    # pattern anchor: xor rcx,rcx ; sub rcx, imm32 ; lea rax,[rip+disp32] ; mov rbx, imm64 ; xor [rax+disp8],rbx
    p_xor_rcx = find(pt, bytes.fromhex("48 31 C9"), pos)
    if p_xor_rcx < 0:
        break

    p_sub_rcx = find(pt, bytes.fromhex("48 81 E9"), p_xor_rcx)
    p_lea = find(
        pt, bytes.fromhex("48 8D 05"), p_sub_rcx if p_sub_rcx >= 0 else p_xor_rcx
    )
    p_movrbx = find(pt, bytes.fromhex("48 BB"), p_lea if p_lea >= 0 else p_xor_rcx)
    p_xor_mem = find(
        pt, bytes.fromhex("48 31 58"), p_movrbx if p_movrbx >= 0 else p_xor_rcx
    )

    if min(p_sub_rcx, p_lea, p_movrbx, p_xor_mem) < 0:
        # no complete stub ahead; advance a bit to avoid re-matching the same "48 31 C9"
        pos = p_xor_rcx + 1
        continue

    # Parse fields
    imm32 = struct.unpack_from("<i", pt, p_sub_rcx + 3)[0]
    loop_count = -imm32  # rcx = 0 - imm32 (imm32 is sign-extended), so -(-N)=N
    disp32 = struct.unpack_from("<i", pt, p_lea + 3)[0]
    pos_after_lea = p_lea + 7
    base = pos_after_lea + disp32  # rax after LEA (buffer-relative)

    key_qword_le = struct.unpack_from("<Q", pt, p_movrbx + 2)[0]
    disp8 = pt[p_xor_mem + 3]
    start = base + disp8

    # detect +8 step (common encodings)
    step = +8  # default
    p_after = p_xor_mem + 4
    op6 = pt[p_after : p_after + 6]
    if op6 in (
        bytes.fromhex("48 05 08 00 00 00"),  # add rax, 8
        bytes.fromhex("48 2D F8 FF FF FF"),
    ):  # sub rax, -8 (== add 8)
        step = +8

    need = start + (loop_count - 1) * abs(step) + 8
    print(
        f"[stub @{p_xor_rcx:04x}] loops={loop_count} base=0x{base:x} off=0x{disp8:x} key=0x{key_qword_le:016x} need<= {need}, len={len(pt)}"
    )

    # bounds check & clamp
    if start < 0 or start + 8 > len(pt):
        print(f"  [!] start out of range ({start}); skipping this stub")
        pos = p_xor_rcx + 1
        continue
    max_iters = max(0, (len(pt) - start) // abs(step))
    iters = min(loop_count, max_iters)
    if iters < loop_count:
        print(f"  [!] clamping iterations {loop_count} -> {iters}")

    # apply
    ptr = start
    for _ in range(iters):
        q = struct.unpack_from("<Q", pt, ptr)[0]
        struct.pack_into("<Q", pt, ptr, q ^ key_qword_le)
        ptr += step

    APPLIED += 1
    # advance past this stub so we can find the next one
    pos = p_xor_mem + 4

print(f"[i] applied {APPLIED} stub(s)")
Path("stage2.bin").write_bytes(pt)
print("[i] wrote stage2.bin")
print("    head:", pt[:16].hex(), repr(bytes(pt[:16])))
