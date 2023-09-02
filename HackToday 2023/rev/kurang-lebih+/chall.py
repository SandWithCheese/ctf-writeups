def check(flag: bytes) -> bool:
    return
    # return )and(()and(())))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))


if __name__ == "__main__":
    FLAG = input("SECRET : ")
    print("CORRECT!" if check(FLAG.encode().ljust(40, b"a")) else "WRONG!")
