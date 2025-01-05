from secrets import randbits, randbelow
from libnum import n2s, s2n
import random
import signal

FLAG = open('flag.txt').read().strip().lstrip('TCF{').rstrip("}")
print(len(FLAG))
assert(len(FLAG) == 29)
p = randbits(128)
q = randbits(128)
N = p * q
print(p)
print(q)
print(N)
e = 0x1001

random.seed(b'azuketto was here')

# Integer complex number field cause python sucks
# I'm pretty sure this is correct, e.g. a + bj == ComplexField(a, b)
class ComplexField:
    real: int
    imag: int
    modulo: int
    
    def __init__(self, real: int = 0, imag: int = 0, modulo: int = N):
        self.real = real
        self.imag = imag
        self.modulo = modulo
    
    def __mul__(self, other):
        assert(isinstance(other, ComplexField))
        real = (self.real * other.real - self.imag * other.imag) % self.modulo
        imag = (self.real * other.imag + self.imag * other.real) % self.modulo
        return ComplexField(real, imag)
    
    def __add__(self, other):
        assert(isinstance(other, ComplexField))
        real = (self.real + other.real) % self.modulo
        imag = (self.imag + other.imag) % self.modulo
        return ComplexField(real, imag)
    
    def __pow__(self, power):
        assert(isinstance(power, int))
        res = ComplexField(1, 0)
        z = ComplexField(self.real, self.imag)
        while power:
            print(f"real: {z.real}, imag: {z.imag}")
            if power & 1: res *= z
            power >>= 1
            z *= z
        return res
    
    def __repr__(self) -> str:
        return n2s(self.real).hex() + ":" + n2s(self.imag).hex()


def split_data(data: int, rand = randbelow) -> ComplexField:
    real = rand(N)
    im = real ^ data
    return ComplexField(real, im)

def main():
    for _ in range(25):
        print("="*50)
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Get flag")
        print("="*50)
        
        choice = int(input(">>> "))
        
        if choice == 1:
            data = bytes.fromhex(input("Data: ").strip())
            data = s2n(data)
            pt = split_data(data, lambda x: random.getrandbits(250))
            ct = pt ** e
            print(ct)
        elif choice == 2:
            d = pow(e, -1, (p-1)*(q-1))
            real = bytes.fromhex(input("Real: ").strip())
            real = s2n(real)
            im = bytes.fromhex(input("Imag: ").strip())
            im = s2n(im)
            ct = ComplexField(real, im)
            pt = ct ** d
            print(sum([ord(c) for c in str(pt)]))
        elif choice == 3:
            data = s2n(FLAG)
            pt = split_data(data)
            print(pt)
            ct = pt ** e
            print(ct)
        else:
            exit(1)
        
        
if __name__ == '__main__':
    signal.alarm(120)
    try:
        main()
    except Exception as e:
        exit(1)


# a^2 mod n = b
    # a^2 = b mod n
    # given a and b, can we find n?