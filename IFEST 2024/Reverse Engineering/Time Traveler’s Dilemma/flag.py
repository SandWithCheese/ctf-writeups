def linear_congruential_generator(m: int, a: int, c: int, seed: int):
    x = seed
    while True:
        yield x
        x = (a * x + c) % m


m: int = 2_147_483_648
a: int = 594_156_893
c: int = 0
seed: int = 123_456_789

gen = linear_congruential_generator(m, a, c, seed)

randint = [238002204140, 807779130162, 970822332959, 522227109232]

for i in range(4):
    rand = next(gen) + randint[i]
    print(f"{i}: {rand}")
