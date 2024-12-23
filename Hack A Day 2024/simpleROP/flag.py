from pwn import *

host, port = "hackaday2024-66-pwn-challenge-65dfd03de7d01279.elb.us-west-2.amazonaws.com", "9998"

r = remote(host, port)

r.interactive()