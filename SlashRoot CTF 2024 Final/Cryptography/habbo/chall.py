#!/usr/bin/env python3
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from os import urandom
import json

RANDOM = urandom(6).hex() 
KEY = urandom(16)

class Token:
    def __init__(
        self,
        name: str = "",
        timestamp: int = 0,
        rand: str = RANDOM,
        admin: bool = False
    ) -> None:
        if timestamp == 0:
            timestamp = int(datetime.now().timestamp())

        self.rand = rand
        self.name = name
        self.timestamp = timestamp
        self.admin = admin

    def authenticate(self):
        if self.admin and self.rand != RANDOM and self.timestamp == -1:
            return True
        else:
            return False

    def is_expired(self):
        now = int(datetime.now().timestamp())
        if self.timestamp == -1:
            return False
        elif self.timestamp + 60 < now:
            return True
        else:
            return False


class HabboHotel:
    def __init__(self) -> None:
        self.aes = AES.new(KEY, AES.MODE_ECB)

    def strip_keys(self, token: dict):
        new = {}
        for key in token:
            value = token[key]
            if type(key) == str:
                new[key.strip()] = value
            else:
                new[key] = value
        return new

    def generate_token(self, name: str):
        try:
            self.token = Token(name)
            token_str = json.dumps(self.token.__dict__)
            self.enc_token = self.aes.encrypt(pad(token_str.encode(), 16)).hex()
        except Exception as e:
            return f"Faulty token :( {repr(e)}"

    def read_token(self, enc_token: str):
        try:
            dec_token = self.aes.decrypt(unhexlify(enc_token))
            data = self.strip_keys(json.loads(unpad(dec_token, 16).decode()))
            self.token = Token(**data)
            self.enc_token = enc_token
        except Exception as e:
            return f"Faulty token :( {repr(e)}"

    def logout(self):
        del self.token
        del self.enc_token
        print("")

    def enter_secret_chamber(self):
        with open("./flag.txt") as f:
            print("FLAG:", f.read())

    def select_room(self, name):
        print(f"Hello {name}! Here is your token: {self.enc_token}")
        print("You can use this token for login. Token will expired 1 minute after creation")
        print()
        while True:
            print("Please select an action")
            print("\t[1] Book a room")
            print("\t[2] Enter secret chamber")
            print("\t[3] Logout")
            print()
            inp = input("Input: ")
            print()
            if inp == "1":
                print("Here's the key. Enjoy!")
                exit()
            elif inp == "2":
                result = self.token.authenticate()
                if result:
                    print("Oh! Right this way sir...")
                    self.enter_secret_chamber()
                    exit()
                else:
                    print("I'm sorry, you're not admin.")
            elif inp == "3":
                print("Okay, have a nice day!")
                break
            else:
                print("Unknown input")
            print()


if __name__ == "__main__":
    print("""
 __ __   ____  ____   ____    ___       __ __   ___   ______    ___  _     
|  |  | /    ||    \ |    \  /   \     |  |  | /   \ |      |  /  _]| |    
|  |  ||  o  ||  o  )|  o  )|     |    |  |  ||     ||      | /  [_ | |    
|  _  ||     ||     ||     ||  O  |    |  _  ||  O  ||_|  |_||    _]| |___ 
|  |  ||  _  ||  O  ||  O  ||     |    |  |  ||     |  |  |  |   [_ |     |
|  |  ||  |  ||     ||     ||     |    |  |  ||     |  |  |  |     ||     |
|__|__||__|__||_____||_____| \___/     |__|__| \___/   |__|  |_____||_____|
                                                                           
""")
    while True:
        hotel = HabboHotel()
        print("Welcome to our lobby!")
        print("Please select an action:")
        print("\t[1] Register")
        print("\t[2] Login")
        print("\t[3] Exit")
        print()
        inp = input("Input: ")
        print()

        if inp == "1":
            name = input("Your name: ")
            err = hotel.generate_token(name)
            if err:
                print(err)
                continue
            hotel.select_room(name)

        elif inp == "2":
            enc_token = input("Token: ")
            err = hotel.read_token(enc_token)
            if err:
                print(err)
                print()
                continue

            if hotel.token.is_expired():
                print("Your token is expired")
            else:
                hotel.select_room(hotel.token.name)

        elif inp == "3":
            print("Thank you for visiting! :)")
            break

        else:
            print("Unknown input")
        print()
