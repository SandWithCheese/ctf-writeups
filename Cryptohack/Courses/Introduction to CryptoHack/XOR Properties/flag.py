from Crypto.Util.number import bytes_to_long, long_to_bytes

KEY1 = bytes_to_long(
    bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
)
KEY2 = KEY1 ^ bytes_to_long(
    bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")
)
KEY3 = KEY2 ^ bytes_to_long(
    bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
)
FLAG = (
    KEY1
    ^ KEY2
    ^ KEY3
    ^ bytes_to_long(
        bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")
    )
)

print(long_to_bytes(FLAG))
