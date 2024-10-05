#!/usr/bin/env python3

import secret
from Crypto.Util.number import bytes_to_long, isPrime

class RandomSequenceGenerator:
    a = secret.a
    b = secret.b
    c = secret.c

    def __init__(self, s):
        self._current_value = s

    def next(self):
        tmp = self._current_value * self.a
        adj = tmp + self.b
        self._current_value = divmod(adj, self.c)[1]
        return self._current_value

def genPrime():
    p = []
    prods = []
    
    hint = True

    it = 0
    shift = 10

    p_n = 1
    count = 0 

    while count < 10:
        cand = random.next()
        count += 1
        
        if 3 <= count <= 10:
            while True:
                if hint:
                    prods.append((cand << pow(2,shift)) + (cand >> (cand.bit_length() - shift)))
                    
                    it += 1
                    if it == 10:
                        hint = False
                if not isPrime(cand):
                    cand = random.next()
                else:
                    p_n *= cand
                    p.append(cand)
                    break
    
    return p, prods

if __name__ == '__main__':
    seed = secret.state
    random = RandomSequenceGenerator(seed)

    primes_arr, hint = genPrime()

    n = 1
    for j in primes_arr:
        n *= j

    _enc = hex(pow(bytes_to_long(secret.flag), 65537, n))

    banner = """
 _    _            _    _            _    _            _    _            _ 
| |  | |    /\    | |  | |    /\    | |  | |    /\    | |  | |    /\    | |
| |__| |   /  \   | |__| |   /  \   | |__| |   /  \   | |__| |   /  \   | |
|  __  |  / /\ \  |  __  |  / /\ \  |  __  |  / /\ \  |  __  |  / /\ \  | |
| |  | | / ____ \ | |  | | / ____ \ | |  | | / ____ \ | |  | | / ____ \ |_|
|_|  |_|/_/    \_\|_|  |_|/_/    \_\|_|  |_|/_/    \_\|_|  |_|/_/    \_\(_)
                                                                        

Welcome to my new encrypting algorithm
will you able to break me?
    """

    menu = """
[1] Get Flag
[2] Get Hint
[3] Check Flag
[4] Exit
    """

    param_n = f"""
n : {hex(n)}  
    """

    print(banner)
    print(param_n)
    print(menu)

    while True:

        user_input = int(input("> "))

        if user_input == 1:
            print(f"Your flag is : {_enc}\n")
        elif user_input == 2:
            print(f"Hint : {hint}\n")
        elif user_input == 3:
            user_flag = input("Your Flag : ")
            if user_flag == secret.flag.decode():
                print("Correct!")
            else:
                print("Incorect!")
        elif user_input == 4:
            print("Bye-Bye! Nooobz\n")
            exit()
        else:
            print("Input Invalid")