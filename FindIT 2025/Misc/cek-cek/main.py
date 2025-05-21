import hashlib
import os

from secret import FLAG


def check(s):
    if "." in s or "flag" in s:
        return False
    return True


hash_obj = hashlib.blake2b()
hash_obj.update(FLAG.encode())
flag = hash_obj.hexdigest()


def open_file(file_name):
    if not check(file_name):
        return "eits tidak boleh begitu", 500

    try:
        file = os.open(file_name, os.O_RDONLY)
        data = os.read(file, 1024)
    except Exception:
        return "error bang"

    return data.decode("utf-8")


if __name__ == "__main__":
    with open("/flag.txt", "w") as f:
        f.write(FLAG)

    flag_file = os.open("/flag.txt", os.O_RDONLY)
    flag_data = os.read(flag_file, 1024)

    if FLAG.encode() != flag_data:
        print("flag file is corrupted")
        exit(1)

    while True:
        print("Do you want check my file?")
        print("1. yes")
        print("2. no")

        choice = input(">>> ")
        if choice == "1":
            file_name = input("file name: ")
            print(open_file(file_name))
        elif choice == "2":
            print("ok, here the flag:")
            print(flag)
        else:
            print("invalid choice")
