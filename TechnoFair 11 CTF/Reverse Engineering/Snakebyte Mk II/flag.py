3000, "3.000")
3010, "3.000+1")  # removed UNARY_CONVERT
3020, "3.000+2")  # added BUILD_SET
3030, "3.000+3")  # added keyword-only parameters
3040, "3.000+4")  # added signature annotations
3050, "3.000+5")  # print becomes a function
3060, "3.000+6")  # PEP 3115 metaclass syntax
3061, "3.000+7")  # string literals become unicode
3071, "3.000+8")  # PEP 3109 raise changes
3081, "3.000+9")  # PEP 3137 make __file__ and __name__ unicode
3091, "3.000+10")  # kill str8 interning
3101, "3.000+11")  # merge from 2.6a0, see 62151
3103, "3.000+12")  # __file__ points to source file
3111, "3.0a4")  # WITH_CLEANUP optimization
3131, "3.0a5")  # lexical exception stacking, including POP_EXCEPT
3141, "3.1a0")  # optimize list, set and dict comprehensions
3151, "3.1a0+")  # optimize conditional branches
3160, "3.2a0")  # add SETUP_WITH
3170, "3.2a1")  # add DUP_TOP_TWO, remove DUP_TOPX and ROT_FOUR
3180, "3.2a2")  # 3.2a2 (add DELETE_DEREF)

# Python 3.2.5 - PyPy 2.3.4 PyPy adds 7 to the corresponding CPython
# number
3180 + 7, "3.2pypy")

3190, "3.3a0")  # __class__ super closure changed
3200, "3.3a0+")  # __qualname__ added
3220, "3.3a1")  # changed PEP 380 implementation

# Added size modulo 2**32 to the pyc header
# NOTE: 3.3a2 is our name, other places call it 3.3
# but most 3.3 versions are 3.3a4 which comes next.
# FIXME: figure out what the history is and
# what the right thing to do if this isn't it.
3210, "3.3a2")
3230, "3.3a4")  # revert changes to implicit __class__ closure

# Evaluate positional default arg keyword-only defaults
3250, "3.4a1")

# Add LOAD_CLASSDEREF; add_magic_from_int locals, f class to override free vars
3260, "3.4a1+1")

3270, "3.4a1+2")  # various tweaks to the __class__ closure
3280, "3.4a1+3")  # remove implicit class argument
3290, "3.4a4")  # changes to __qualname__ computation
3300, "3.4a4+")  # more changes to __qualname__ computation
3310, "3.4rc2")  # alter __qualname__ computation
3320, "3.5a0")  # matrix multiplication operator
3330, "3.5b1")  # pep 448: additional unpacking generalizations
3340, "3.5b2")  # fix dictionary display evaluation order #11205
3350, "3.5")  # add GET_YIELD_FROM_ITER opcode #24400 (also 3.5b2)

    3351, "3.5.2"
)  # fix BUILD_MAP_UNPACK_WITH_CALL opcode #27286; 3.5.3, 3.5.4, 3.5.5
3360, "3.6a0")  # add FORMAT_VALUE opcode #25483
3361, "3.6a0+1")  # lineno delta of code.co_lnotab becomes signed
3370, "3.6a1")  # 16 bit wordcode
3371, "3.6a1+1")  # add BUILD_CONST_KEY_MAP opcode #27140

    3372, "3.6a1+2"
)  # MAKE_FUNCTION simplification, remove MAKE_CLOSURE #27095
3373, "3.6b1")  # add BUILD_STRING opcode #27078

    3375, "3.6b1+1"
)  # add SETUP_ANNOTATIONS and STORE_ANNOTATION opcodes #27985

    3376, "3.6b1+2"
)  # simplify CALL_FUNCTION* & BUILD_MAP_UNPACK_WITH_CALL
3377, "3.6b1+3")  # set __class__ cell from type.__new__ #23722
3378, "3.6b2")  # add BUILD_TUPLE_UNPACK_WITH_CALL #28257

# more thorough __class__ validation #23722
3379, "3.6rc1")

# add LOAD_METHOD and CALL_METHOD opcodes #26110
3390, "3.7.0alpha0")

# update GET_AITER #31709
3391, "3.7.0alpha3")

# Initial PEP 552 - Deterministic pycs #31650
# Additional word in header and possibly no timestamp
3392, "3.7.0beta2")

# Final PEP 552: timestamp + size field or no timestamp + SipHash
# remove STORE_ANNOTATION opcode #3255
3393, "3.7.0beta3")

# restored docstring as the first stmt in the body; this might
# affect the first line number #32911
3394, "3.7.0")

# move frame block handling to compiler #17611
3400, "3.8.0a1")

# add END_ASYNC_FOR #33041
3401, "3.8.0a3+")

# PEP570 Python Positional-Only Parameters #36540
3410, "3.8.0a1+")

# Reverse evaluation order of key: value in dict comprehensions
# #35224
3411, "3.8.0b2+")

# Swap the position of positional args and positional only args in
# ast.arguments #37593
3412, "3.8.0beta2")

# Fix "break" and "continue" in "finally" #37830
3413, "3.8.0rc1+")

# add LOAD_ASSERTION_ERROR #34880
3420, "3.9.0a0")

# simplified bytecode for with blocks #32949
3421, "3.9.0a0")

# Remove BEGIN_FINALLY, END_FINALLY, CALL_FINALLY, POP_FINALLY bytecodes #33387
3422, "3.9.0alpha1")

# add IS_OP, CONTAINS_OP and JUMP_IF_NOT_EXC_MATCH bytecodes #39156
3423, "3.9.0a0")

# simplify bytecodes for *value unpacking
3424, "3.9.0a2")

# simplify bytecodes for **value unpacking
3425, "3.9.0beta5")

# Make 'annotations' future by default
3430, "3.10a1")

# New line number table format -- PEP 626
3431, "3.10a1")

# Function annotation for MAKE_FUNCTION is changed from dict to tuple bpo-42202
3432, "3.10a2")

# RERAISE restores f_lasti if oparg != 0
3433, "3.10a2")
3434, "3.10a6")
3435, "3.10a7")
3438, "3.10b1")
3439, "3.10.0rc2")

3450, "3.11a1a")
3451, "3.11a1b")
3452, "3.11a1c")
3453, "3.11a1d")
3454, "3.11a1e")
3455, "3.11a1f")
3457, "3.11a1g")
3458, "3.11a1h")
3459, "3.11a1i")
3460, "3.11a1j")
3461, "3.11a1k")
3462, "3.11a2")
3463, "3.11a3a")
3464, "3.11a3b")
3465, "3.11a4a")
3466, "3.11a4b")
3466, "3.11a4c")
3467, "3.11a4d")
3468, "3.11a4e")
3469, "3.11a4f")
3470, "3.11a4g")
3471, "3.11a4h")
3472, "3.11a4i")
3473, "3.11a4j")
3474, "3.11a4k")
3475, "3.11a5a")
3476, "3.11a5b")
3477, "3.11a5c")
3478, "3.11a5d")
3479, "3.11a5e")
3480, "3.11a5e")
3481, "3.11a5f")
3482, "3.11a5g")
3483, "3.11a5h")
3484, "3.11a5i")
3485, "3.11a5j")
3486, "3.11a6a")
3487, "3.11a6b")
3488, "3.11a6c")
3489, "3.11a6d")
3490, "3.11a6d")
3491, "3.11a7a")
3492, "3.11a7b")
3493, "3.11a7c")
3494, "3.11a7d")
3495, "3.11a7e")
3531, "3.12.0rc2")