from z3 import *

s = Solver()
(
    f0,
    f1,
    f2,
    f3,
    f4,
    f5,
    f6,
    f7,
    f8,
    f9,
    f10,
    f11,
    f12,
    f13,
    f14,
    f15,
    f16,
    f17,
    f18,
    f19,
    f20,
    f21,
    f22,
    f23,
    f24,
    f25,
    f26,
    f27,
    f28,
    f29,
    f30,
    f31,
    f32,
    f33,
    f34,
    f35,
    f36,
    f37,
    f38,
    f39,
) = Ints(
    "f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 f13 f14 f15 f16 f17 f18 f19 f20 f21 f22 f23 f24 f25 f26 f27 f28 f29 f30 f31 f32 f33 f34 f35 f36 f37 f38 f39"
)

s.add((f22 - f28 + f4 + f35 - f29) == -25)
s.add((f26 - f0 + f23 + f11 - f16) == -19)
s.add((f9 - f21 + f37 + f34 - f14) == 195)
s.add((f19 - f18 + f6 + f13 - f12) == 112)
s.add((f36 - f38 + f33 + f32 - f3) == 168)
s.add((f2 - f20 + f7 + f10 - f30) == 49)
s.add((f5 - f25 + f27 + f39 - f17) == 87)
s.add((f24 - f8 + f15 + f31 - f1) == 102)
s.add((f22 + f28 - f4 - f35 + f29) == 105)
s.add((f26 + f0 - f23 - f11 + f16) == 83)
s.add((f9 + f21 - f37 - f34 + f14) == 49)
s.add((f19 + f18 - f6 - f13 + f12) == 122)
s.add((f36 + f38 - f33 - f32 + f3) == -96)
s.add((f2 + f20 - f7 - f10 + f30) == 147)
s.add((f5 + f25 - f27 - f39 + f17) == 123)
s.add((f24 + f8 - f15 - f31 + f1) == 120)
s.add((f22 - f28 - f4 + f35 + f29) == -47)
s.add((f26 - f0 - f23 + f11 + f16) == -37)
s.add((f9 - f21 - f37 + f34 + f14) == 223)
s.add((f19 - f18 - f6 + f13 + f12) == 136)
s.add((f36 - f38 - f33 + f32 + f3) == 28)
s.add((f2 - f20 - f7 + f10 + f30) == 41)
s.add((f5 - f25 - f27 + f39 + f17) == -27)
s.add((f24 - f8 - f15 + f31 + f1) == 90)
s.add((f22 + f28 + f4 - f35 - f29) == 127)
s.add((f26 + f0 + f23 - f11 - f16) == 101)
s.add((f9 + f21 + f37 - f34 - f14) == 21)
s.add((f19 + f18 + f6 - f13 - f12) == 98)
s.add((f36 + f38 + f33 - f32 - f3) == 44)
s.add((f2 + f20 + f7 - f10 - f30) == 155)
s.add((f5 + f25 + f27 - f39 - f17) == 237)
s.add((f24 + f8 + f15 - f31 - f1) == 132)
s.add((f22 - f28 + f4 - f35 + f29) == 105)
s.add((f26 - f0 + f23 - f11 + f16) == 93)
s.add((f9 - f21 + f37 - f34 + f14) == 173)
s.add((f19 - f18 + f6 - f13 + f12) == 134)
s.add((f36 - f38 + f33 - f32 + f3) == 64)
s.add((f2 - f20 + f7 - f10 + f30) == 153)
s.add((f5 - f25 + f27 - f39 + f17) == 95)
s.add((f24 - f8 + f15 - f31 + f1) == 262)
s.add((f22 + f28 - f4 + f35 - f29) == -25)
s.add((f26 + f0 - f23 + f11 - f16) == -29)
s.add((f9 + f21 - f37 + f34 - f14) == 71)
s.add((f19 + f18 - f6 + f13 - f12) == 100)
s.add((f36 + f38 - f33 + f32 - f3) == 8)
s.add((f2 + f20 - f7 + f10 - f30) == 43)
s.add((f5 + f25 - f27 + f39 - f17) == 115)
s.add((f24 + f8 - f15 + f31 - f1) == -40)
s.add((f22 - f28 - f4 - f35 - f29) == -305)
s.add((f26 - f0 - f23 - f11 - f16) == -329)
s.add((f9 - f21 - f37 - f34 - f14) == -231)
s.add((f19 - f18 - f6 - f13 - f12) == -330)
s.add((f36 - f38 - f33 - f32 - f3) == -260)
s.add((f2 - f20 - f7 - f10 - f30) == -267)
s.add((f5 - f25 - f27 - f39 - f17) == -199)
s.add((f24 - f8 - f15 - f31 - f1) == -198)
s.add((f22 + f28 + f4 + f35 + f29) == 385)
s.add((f26 + f0 + f23 + f11 + f16) == 393)
s.add((f9 + f21 + f37 + f34 + f14) == 475)
s.add((f19 + f18 + f6 + f13 + f12) == 564)
s.add((f36 + f38 + f33 + f32 + f3) == 332)
s.add((f2 + f20 + f7 + f10 + f30) == 463)
s.add((f5 + f25 + f27 + f39 + f17) == 409)
s.add((f24 + f8 + f15 + f31 + f1) == 420)


# s.check()
# models = s.model()


# flag = "105 112 98 46 108 105 110 107 47 122 51 45 122 111 108 118 101 45 104 117 104 32 40 110 111 116 32 102 108 97 103 32 98 116 119 32 36 94 36 41".split()
# for i in flag:
#     print(chr(int(i)), end="")
# while s.check() == sat:
#     # print(s.model())
#     # s.add(Or(f1 !+ ))
#     solution = "False"
#     m = s.model()
#     print(m)
#     for i in m:
#         solution = f"Or(({i} != {m[i]}), {solution})"
#     print(solution)
#     loop = eval(solution)
#     s.add(loop)
# Return the first "M" models of formula list of formulas F
def get_models(M):
    result = []
    while len(result) < M and s.check() == sat:
        m = s.model()
        result.append(m)
        # Create a new constraint the blocks the current model
        block = []
        for d in m:
            # d is a declaration
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            # create a constant from declaration
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))
    return result


print(get_models(10))
