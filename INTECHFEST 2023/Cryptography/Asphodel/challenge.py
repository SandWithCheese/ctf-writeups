import numpy as np
import galois
import os
import random
from hashlib import sha256

GF = galois.GF(2)

N = 128
R = 15

MSG = 'The main things about ghosts, most of them have lost their voices'
FLAG = open('flag.txt', 'r').read()


def bytes_to_vector(b):
    vec = GF([0] * N)
    assert len(b) == N // 8
    for i in range(len(b)):
        tmp = b[i]
        for j in range(8):
            vec[8 * i + 7 - j] = tmp & 1
            tmp >>= 1
    return vec


def vector_to_bytes(vec):
    assert len(vec) == N
    b = bytearray(N // 8)
    for i in range(len(b)):
        for j in range(8):
            b[i] = (b[i] << 1) | int(vec[8 * i + j])
    return b


class Signature:

    def __init__(self, key):
        random.seed('Embrace the darkness, mortal, and discover your true desires!')
        self.key = bytes_to_vector(key)
        self.matrices = [self._gen_matrix() for _ in range(R)]
        self.constants = [self._gen_vector() for _ in range(R)]

    def _gen_matrix(self):
        while True:
            mat = GF(np.zeros((N, N), dtype=int))
            for i in range(N):
                for j in range(N):
                    mat[i, j] = random.randint(0, 1)
            if np.linalg.det(mat) != 0:
                return mat

    def _gen_vector(self):
        vec = GF([0] * N)
        for i in range(N):
            vec[i] = random.randint(0, 1)
        return vec

    def sbox(self, a, b, c):
        return a + b + c

    def linear(self, state, r):
        return self.matrices[r] @ state

    def linear_inv(self, state, r):
        return np.linalg.inv(self.matrices[r]) @ state

    def add_constant(self, state, r):
        return state + self.constants[r]

    def mix_key(self, state):
        return state + self.key

    def sign(self, message):
        state = bytes_to_vector(sha256(message).digest()[:16])
        for r in range(R):
            state[0] = self.sbox(state[0], state[1], state[2])
            state = self.linear(state, r)
            state = self.add_constant(state, r)
            state = self.mix_key(state)

        return vector_to_bytes(state)

    def verify(self, message, signature):
        state = bytes_to_vector(signature)
        for r in range(R - 1, -1, -1):
            state = self.mix_key(state)
            state = self.add_constant(state, r)
            state = self.linear_inv(state, r)
            state[0] = self.sbox(state[0], state[1], state[2])

        return sha256(message).digest()[:16] == vector_to_bytes(state)


if __name__ == '__main__':

    try:
        print("Preparing souls...")
        signer = Signature(os.urandom(16))
        m = bytes.fromhex(input('Your msg: '))
        if m == MSG or sha256(m).digest() == sha256(MSG.encode()).digest():
            print('No cheating!')
            exit()

        sig = signer.sign(m).hex()
        print("Your signature: ", sig)

        check = input('Secret signature: ')
        user_sig = bytes.fromhex(check)

        if signer.verify(MSG.encode(), user_sig):
            print(FLAG)
        else:
            print("No good!")
    except Exception as e:
        print('No cheating!')
