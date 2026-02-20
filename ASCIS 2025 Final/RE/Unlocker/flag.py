import hashlib


# MT19937-64 implementation (matches std::mt19937_64 parameters)
class MT19937_64:
    def __init__(self, seed: int):
        # Parameters for MT19937-64
        self.w = 64
        self.n = 312
        self.m = 156
        self.r = 31
        self.a = 0xB5026F5AA96619E9
        self.u = 29
        self.d = 0x5555555555555555
        self.s = 17
        self.b = 0x71D67FFFEDA60000
        self.t = 37
        self.c = 0xFFF7EEE000000000
        self.l = 43
        self.f = 6364136223846793005  # 0x5851F42D4C957F2D

        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (~self.lower_mask) & ((1 << self.w) - 1)

        # State array
        self.mt = [0] * self.n
        self.index = self.n  # force initial twist

        # Initialization (same as std::seed_seq for a single seed)
        self.mt[0] = seed & ((1 << self.w) - 1)
        for i in range(1, self.n):
            prev = self.mt[i - 1]
            self.mt[i] = (self.f * (prev ^ (prev >> (self.w - 2))) + i) & (
                (1 << self.w) - 1
            )

    def twist(self):
        for i in range(self.n):
            x = (self.mt[i] & self.upper_mask) + (
                self.mt[(i + 1) % self.n] & self.lower_mask
            )
            xA = x >> 1
            if x & 1:  # lowest bit set?
                xA ^= self.a
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0

    def extract_number(self) -> int:
        if self.index >= self.n:
            self.twist()

        y = self.mt[self.index]
        self.index += 1

        # Tempering (std::mt19937_64)
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        return y & ((1 << self.w) - 1)


def generate_otp(length: int, seed: int = 20251025) -> str:
    charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    mt = MT19937_64(seed)
    out = []
    for _ in range(length):
        rnd = mt.extract_number()
        idx = rnd % len(
            charset
        )  # effectively what uniform_int_distribution will give here
        out.append(charset[idx])
    return "".join(out)


if __name__ == "__main__":
    otp = "pjEmGyPhO0U441E"
    print("OTP:", otp)
    print("Length:", len(otp))

    sha1_hex = hashlib.sha1(otp.encode("utf-8")).hexdigest()
    flag = f"CSCV2025{{{sha1_hex}}}"
    print("SHA1:", sha1_hex)
    print("Flag:", flag)
