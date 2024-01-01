#!/usr/local/bin/python3
import hashlib
import os

flag = "boka_chan_ga_oshiete_kureta_ironna_mita_meni_narera_puninan_ndatte_dore_dore" if os.getenv("FLAG") is None else os.getenv("FLAG")
secret = os.urandom(16)
test1 = os.urandom(16)
test2 = os.urandom(16)

print(">> proof me if you could find the collision <<")
try:
    message = bytes.fromhex(input("message (hex): "))
    proofit = bytes.fromhex(input("proofit (hex): "))

    if message == proofit:
        print(">> L for the chat")
        exit(1)

    if hashlib.md5(message + secret).hexdigest() == hashlib.md5(proofit + secret).hexdigest():
        print(">> spam W in the chat")
        print(">> yo chat why is this game so fun chat")
        print(">>", flag)
        exit(0)

except ValueError:
    print("yo is not hex")
    exit(1)