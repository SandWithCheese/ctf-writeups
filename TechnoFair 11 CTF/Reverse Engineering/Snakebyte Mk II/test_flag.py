def int_to_reversed_hex_byte(i):
    return f"{i.to_bytes(2, 'little').hex()}"


versions = [
    3000,
    3010,
    3020,
    3030,
    3040,
    3050,
    3060,
    3061,
    3071,
    3081,
    3091,
    3101,
    3103,
    3111,
    3131,
    3141,
    3151,
    3160,
    3170,
    3180,
    # Python 3.2.5 - PyPy 2.3.4 PyPy adds 7 to the corresponding CPython
    # number
    3180 + 7,
    3190,
    3200,
    3220,
    # Added size modulo 2**32 to the pyc header
    # NOTE: 3.3a2 is our name
    # but most 3.3 versions are 3.3a4 which comes next.
    # FIXME: figure out what the history is and
    # what the right thing to do if this isn't it.
    3210,
    3230,
    # Evaluate positional default arg keyword-only defaults
    3250,
    # Add LOAD_CLASSDEREF; add_magic_from_int locals
    3260,
    3270,
    3280,
    3290,
    3300,
    3310,
    3320,
    3330,
    3340,
    3350,
    3351,
    3360,
    3361,
    3370,
    3371,
    3372,
    3373,
    3375,
    3376,
    3377,
    3378,
    # more thorough __class__ validation #23722
    3379,
    # add LOAD_METHOD and CALL_METHOD opcodes #26110
    3390,
    # update GET_AITER #31709
    3391,
    # Initial PEP 552 - Deterministic pycs #31650
    # Additional word in header and possibly no timestamp
    3392,
    # Final PEP 552: timestamp + size field or no timestamp + SipHash
    # remove STORE_ANNOTATION opcode #3255
    3393,
    # restored docstring as the first stmt in the body; this might
    # affect the first line number #32911
    3394,
    # move frame block handling to compiler #17611
    3400,
    # add END_ASYNC_FOR #33041
    3401,
    # PEP570 Python Positional-Only Parameters #36540
    3410,
    # Reverse evaluation order of key: value in dict comprehensions
    # #35224
    3411,
    # Swap the position of positional args and positional only args in
    # ast.arguments #37593
    3412,
    # Fix "break" and "continue" in "finally" #37830
    3413,
    # add LOAD_ASSERTION_ERROR #34880
    3420,
    # simplified bytecode for with blocks #32949
    3421,
    # Remove BEGIN_FINALLY
    3422,
    # add IS_OP
    3423,
    # simplify bytecodes for *value unpacking
    3424,
    # simplify bytecodes for **value unpacking
    3425,
    # Make 'annotations' future by default
    3430,
    # New line number table format -- PEP 626
    3431,
    # Function annotation for MAKE_FUNCTION is changed from dict to tuple bpo-42202
    3432,
    3433,
    3434,
    3435,
    3436,
    3437,
    3438,
    3439,
    3450,
    3451,
    3452,
    3453,
    3454,
    3455,
    3456,
    3457,
    3458,
    3459,
    3460,
    3461,
    3462,
    3463,
    3464,
    3465,
    3466,
    3467,
    3468,
    3469,
    3470,
    3471,
    3472,
    3473,
    3474,
    3475,
    3476,
    3477,
    3478,
    3479,
    3480,
    3481,
    3482,
    3483,
    3484,
    3485,
    3486,
    3487,
    3488,
    3489,
    3490,
    3491,
    3492,
    3493,
    3494,
    3495,
    3500,
    3501,
    3502,
    3503,
    3504,
    3505,
    3506,
    3507,
    3508,
    3509,
    3510,
    3511,
    3512,
    3513,
    3514,
    3515,
    3516,
    3517,
    3518,
    3519,
    3520,
    3521,
    3522,
    3523,
    3524,
    3525,
    3526,
    3527,
    3528,
    3529,
    3530,
    3531,
]

for version in versions:
    # Replace the version number (first 2 byte) with the reversed hex byte
    with open("chall.pyc", "rb") as f:
        data = f.read()

    hex_byte = bytes.fromhex(int_to_reversed_hex_byte(version))
    print(f"Version: {version}, Hex byte: {hex_byte}")
    data = hex_byte + data[2:]

    with open(f"chall_{version}.pyc", "wb") as f:
        f.write(data)

    # Update existing command.sh to add the new version
    with open("command.sh", "r") as f:
        lines = f.readlines()

    with open("command.sh", "w") as f:
        for line in lines:
            f.write(line)

        f.write(f"pycdc chall_{version}.pyc\n")
