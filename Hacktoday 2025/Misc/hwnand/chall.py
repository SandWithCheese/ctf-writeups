from z3 import *
import string
import time
import sys
from flag import flag


spec = """
ISA:
- 4 register 8-bit
- 256 byte memori instruksi
  - 128 pertama adalah program user
  - 128 kedua adalah kode kernel
- 256 byte memori data
  - 128 pertama dapat diakses user
  - 128 kedua khusus untuk kernel

Instruksi:
rdtsc rX (khusus kernel)
  0000'00rr
putc rX (khusus kernel)
  0000'01rr
ldi rX, imm
  0000'10rr
syscall
  0000'110x
- akan lompat ke lokasi kernel 130. Alamat kembali akan disimpan di r0.
- kode kernel menangani syscall sesuai r1, lalu sysret kembali ke r0.
- r1 == 0: exit()
- r1 == 1: time() -> mengembalikan rdtsc di r2
- r1 == 2: putc(r2)
sysret (khusus kernel)
  0000'1110
halt
  0000'1111
load rX, [rY]
  0001'XXYY
store [rX], rY
  0010'YYXX
add rX, rY
  0011'XXYY
jmp rX
  01xx'xxrr
jz rX==0, rY
  1xxx'XXYY


Spesifikasi decoder instruksi kombinatorial:
Input:
- is_root_now
- in_0..in_7
- r0_0..r0_7, ..., r3_0..r3_7
Output:
- is_rdtsc, is_putc, ... is_jz
- security_exception
"""
fine_circ = False
gates = {}

def verify():
    global fine_circ

    if len(gates) > 200:
        print("Terlalu banyak gerbang, tidak muat di chip...")
        return

    outputs = [
        "is_rdtsc", "is_putc", "is_ldi", "is_syscall", "is_sysret",
        "is_hlt", "is_ld", "is_str", "is_add", "is_jmp", "is_jz",
        "security_exception"
    ]

    input_list = ["is_root_now"]
    for idx in range(8):
        input_list.append(f"in_{idx}")
        input_list.append(f"r0_{idx}")
        input_list.append(f"r1_{idx}")
        input_list.append(f"r2_{idx}")
        input_list.append(f"r3_{idx}")

    for out in outputs:
        if out not in gates:
            print(f"{out} belum diimplementasikan.")
            return

    for key in gates:
        left, right = gates[key]
        if left not in gates and left not in input_list:
            print(f"Kabel {left} belum terhubung.")
            return
        if right not in gates and right not in input_list:
            print(f"Kabel {right} belum terhubung.")
            return

    wire = {}
    for item in list(gates) + input_list:
        wire[item] = Bool(item)

    solver = Solver()
    for key in gates:
        left, right = gates[key]
        solver.add(wire[key] == Not(And(wire[left], wire[right])))

    result = solver.check()
    if result == unknown:
        print("Error tidak diketahui?")
        return
    if result == unsat:
        print("Sirkuit tidak stabil.")
        return

    rules = []
    rules.append(wire["is_jz"]      == wire["in_7"])
    rules.append(wire["is_jmp"]     == ~wire["in_7"] & wire["in_6"])
    rules.append(wire["is_add"]     == ~wire["in_7"] & ~wire["in_6"] & wire["in_5"] & wire["in_4"])
    rules.append(wire["is_str"]   == ~wire["in_7"] & ~wire["in_6"] & wire["in_5"] & ~wire["in_4"])
    rules.append(wire["is_ld"]    == ~wire["in_7"] & ~wire["in_6"] & ~wire["in_5"] & wire["in_4"])
    rules.append(wire["is_hlt"]    == ~wire["in_7"] & ~wire["in_6"] & ~wire["in_5"] & ~wire["in_4"] & wire["in_3"] & wire["in_2"] & wire["in_1"] & wire["in_0"])
    rules.append(wire["is_sysret"]  == ~wire["in_7"] & ~wire["in_6"] & ~wire["in_5"] & ~wire["in_4"] & wire["in_3"] & wire["in_2"] & wire["in_1"] & ~wire["in_0"])
    rules.append(wire["is_syscall"] == ~wire["in_7"] & ~wire["in_6"] & ~wire["in_5"] & ~wire["in_4"] & wire["in_3"] & wire["in_2"] & ~wire["in_1"])
    rules.append(wire["is_ldi"]     == ~wire["in_7"] & ~wire["in_6"] & ~wire["in_5"] & ~wire["in_4"] & wire["in_3"] & ~wire["in_2"])
    rules.append(wire["is_putc"]    == ~wire["in_7"] & ~wire["in_6"] & ~wire["in_5"] & ~wire["in_4"] & ~wire["in_3"] & wire["in_2"])
    rules.append(wire["is_rdtsc"]   == ~wire["in_7"] & ~wire["in_6"] & ~wire["in_5"] & ~wire["in_4"] & ~wire["in_3"] & ~wire["in_2"])

    kernel_addr = Or([
        ~wire["in_0"] & ~wire["in_1"] & wire["r0_7"],
        wire["in_0"] & ~wire["in_1"]  & wire["r1_7"],
        ~wire["in_0"] & wire["in_1"]  & wire["r2_7"],
        wire["in_0"] & wire["in_1"]   & wire["r3_7"],
    ])

    rules.append(wire["security_exception"] == ~wire["is_root_now"] & Or([
        wire["is_rdtsc"], wire["is_putc"], wire["is_sysret"],
        And(Or(wire["is_str"], wire["is_ld"]), kernel_addr)
    ]))

    solver.add(Not(And(rules)))
    result = solver.check()
    if result == unknown:
        print("Error tidak diketahui?")
        return
    if result == unsat:
        print("Verifikasi formal berhasil!")
    else:
        print("Verifikasi formal gagal!")
        return

    print("Sirkuit sudah benar!")
    fine_circ = True

def check(name):
    if name.startswith("_"): return False
    if any(ch not in string.ascii_letters + string.digits + "_" for ch in name): return False
    return True

def menu():
    global gates
    print("1. Cetak spesifikasi.")
    print("2. Hapus desain.")
    print("3. Tambah gerbang.")
    print("4. Cetak desain.")
    print("5. Verifikasi desain.")
    print("6. Keluar.")
    try:
        choice = int(input())
    except EOFError:
        sys.exit(0)
    except:
        return

    if choice == 1:
        print(spec)
    elif choice == 2:
        gates = {}
    elif choice == 3:
        print("Tulis 3 nama kabel (misal 'C A B') untuk menambah gerbang NAND C = A NAND B")
        z, x, y = input().strip().split()
        if not check(x) or not check(y) or not check(z):
            print("Nama tidak valid.")
            return
        if z in gates:
            print("Kabel sudah ada.")
            return
        gates[z] = (x, y)
        print("Berhasil ditambahkan.")
    elif choice == 4:
        for z in gates:
            x, y = gates[z]
            print(f"{z} = {x} NAND {y}")
    elif choice == 5:
        verify()
    elif choice == 6:
        sys.exit(0)
    else:
        print("???")

def run_nand(state, output_wire):
    if output_wire in state:
        return state[output_wire]
    left_wire, right_wire = gates[output_wire]
    left_val = run_nand(state, left_wire)
    right_val = run_nand(state, right_wire)
    state[output_wire] = not (left_val and right_val)
    return state[output_wire]

def run(program):
    memory = [0] * 256
    for idx, char in enumerate(flag):
        memory[idx+128] = ord(char)

    pc = 0
    regs = [0, 0, 0, 0]
    is_root_now = False
    steps = 0
    while True:
        time.sleep(0.01) # CPU lambat...

        steps += 1
        if steps > 10000:
            print("Batas langkah tercapai.")
            return

        instr = program[pc]
        pc += 1

        state = {}
        state["is_root_now"] = is_root_now
        for i in range(8):
            state[f"in_{i}"] = (instr >> i) & 1
            for r in range(4):
                state[f"r{r}_{i}"] = (regs[r] >> i) & 1

        outputs = [
            "is_rdtsc", "is_putc", "is_ldi", "is_syscall", "is_sysret",
            "is_hlt", "is_ld", "is_str", "is_add", "is_jmp", "is_jz"
        ]
        tipe_instruksi = []
        for out in outputs:
            if run_nand(state, out):
                tipe_instruksi.append(out)

        assert len(tipe_instruksi) == 1

        if run_nand(state, "security_exception"):
            print("SECURITY EXCEPTION. HALT.")
            return

        low = instr & 3
        high = (instr >> 2) & 3

        if state["is_jmp"] or state["is_jz"]:
            cond = True
            if state["is_jz"]:
                cond = regs[high] == 0
            if cond:
                pc = regs[low]
        elif state["is_add"]:
            regs[high] += regs[low]
            regs[high] &= 127
        elif state["is_str"]:
            memory[regs[low]] = regs[high]
        elif state["is_ld"]:
            regs[high] = memory[regs[low]]
        elif state["is_hlt"]:
            print("HALT.")
            return
        elif state["is_sysret"]:
            pc = regs[0]
            is_root_now = False
        elif state["is_syscall"]:
            regs[0] = pc
            pc = 130
            is_root_now = True
        elif state["is_ldi"]:
            regs[low] = program[pc]
            pc += 1
        elif state["is_putc"]:
            print(chr(regs[low]), end="")
            sys.stdout.flush()
        elif state["is_rdtsc"]:
            regs[low] = int(time.time()) % 10
        else:
            print("Seharusnya ngga terjadi...")
            return

def get_and_run():
    print("Ok. Desain CPU sudah dikirim ke pabrik, dan chip siap.")
    print("Mari jalankan kode!")
    print("Contoh: 09020a480c0a690c0a210c0a200c0a540c0a680c0a650c0a200c0a740c0a690c0a6d0c0a650c0a200c0a690c0a730c0a200c0a780c0a780c0a3a0c0a780c0a780c0a3a0c0a780c09010c0b303b09020c0a0a0c09000c")
    print("Input kode user (hex, maksimal 128 byte):")

    HALT = b"\x0f"
    code = bytes.fromhex(input().strip())[:128]
    code += HALT * (128 - len(code))

    KERNEL_CODE = bytes.fromhex("0f0f 0b91 870bff37 0b92 870bff37 0b96 87 0f 0209010e 0609020e")
    KERNEL_CODE += HALT * (128 - len(KERNEL_CODE))
    code += KERNEL_CODE

    run(code)

def main():
    print("Implementasikan sirkuit decoder CPU!")
    while not fine_circ:
        menu()
    get_and_run()

if __name__ == "__main__":
    main()