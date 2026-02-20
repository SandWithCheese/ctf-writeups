# Scan codes from WORD_ARRAY_140002220 (indices 0..38)
scan_codes = [
    0x2E, 0x1F, 0x2E, 0x2F,
    0x03, 0x0B, 0x03, 0x06,
    0x1A, 0x11, 0x23, 0x05,
    0x14, 0x0C, 0x02, 0x2C,
    0x0C, 0x31, 0x05, 0x14,
    0x17, 0x2F, 0x04, 0x0C,
    0x05, 0x19, 0x19, 0x26,
    0x02, 0x2E, 0x05, 0x14,
    0x02, 0x0B, 0x31, 0x02,
    0x02, 0x02, 0x1B,
]

# Shift flags from WORD_140002370 (indices 0..38)
# 0 = no shift, 1 = shift held
shift_flags = [
    1, 1, 1, 1,
    0, 0, 0, 0,
    1, 0, 0, 0,
    0, 1, 0, 0,
    1, 0, 0, 0,
    0, 0, 0, 1,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0,
    1, 1, 1, 1,
]

# Minimal scan-code → (unshifted, shifted) mapping for the codes used
keymap = {
    0x02: ('1', '!'),
    0x03: ('2', '@'),
    0x04: ('3', '#'),
    0x05: ('4', '$'),
    0x06: ('5', '%'),
    0x0B: ('0', ')'),
    0x0C: ('-', '_'),
    0x11: ('w', 'W'),
    0x14: ('t', 'T'),
    0x17: ('i', 'I'),
    0x19: ('p', 'P'),
    0x1A: ('[', '{'),
    0x1B: (']', '}'),
    0x1F: ('s', 'S'),
    0x23: ('h', 'H'),
    0x26: ('l', 'L'),
    0x2C: ('z', 'Z'),
    0x2E: ('c', 'C'),
    0x2F: ('v', 'V'),
    0x31: ('n', 'N'),
}

flag_chars = []
for sc, sh in zip(scan_codes, shift_flags):
    normal, shifted = keymap.get(sc, ('?', '?'))
    flag_chars.append(shifted if sh else normal)

flag = ''.join(flag_chars)
print(flag)
