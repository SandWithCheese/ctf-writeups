#! /usr/bin/python3

import hashlib
import subprocess
from binascii import hexlify

wl_cmd = b'echo lol'
wl_hash = hashlib.sha1(wl_cmd).digest()[:3]

def main():
    while True:
        print('\nWelcome to my secret service, have fun!\n')
        input_cmd = input('> ').encode('latin1')
        
        if input_cmd == b'exit':
            print('Bye-Bye 👋👋👋')
            exit()
        
        if hashlib.sha1(input_cmd).digest()[:3] != wl_hash:
            print(f'Unknown command, try this command instead : {wl_cmd.decode("latin1")}')
            continue

        if b'flag.txt' in input_cmd:
            print(f'bruh use another method h3h3h3h3')

        try:
            res = subprocess.check_output(['/bin/bash', '-c', input_cmd])
            print(res.decode())            
        except subprocess.CalledProcessError as e:
            print(f'Command returned non-zero exit status {e.returncode}')

if __name__ == '__main__':
    main()