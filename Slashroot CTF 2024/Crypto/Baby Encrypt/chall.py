#!/usr/bin/env python3

from Crypto.Cipher import AES as _A
import os as _o
from secret import FLAG as _F

_K = _o.urandom(16)
_I = _o.urandom(16)

_d = lambda _c, _k, _i: bytes(_x ^ _y for _x, _y in zip(_c, b''.join(list((_A.new(_k, _A.MODE_ECB).encrypt(_i if _j == 0 else _e) for _j, _e in enumerate([_A.new(_k, _A.MODE_ECB).encrypt(_i)] * (len(_c) // _A.block_size + 1))))[:len(_c)])))

def _m():
    while True:
        try:
            _ct = bytes.fromhex(input('ciphertext anda: '))
            print(eval(_d(_ct, _K, _I)))
        except Exception:
            print('ciphertext tidak valid!')

if __name__ == '__main__':
    _m()
