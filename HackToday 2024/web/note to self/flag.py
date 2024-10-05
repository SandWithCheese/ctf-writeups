import requests

url = "http://0.0.0.0:8000/"


def register(name):
    data = {"name": name}
    response = requests.post(url + "register", json=data)
    return response


def upload(token, content):
    data = {"content": content}
    headers = {"Token": token}
    response = requests.post(url + "notes/upload", json=data, headers=headers)
    return response


def download(token, note_id):
    headers = {"Token": token}
    response = requests.get(url + f"notes/download/{note_id}", headers=headers)
    return response


token = register("testt\n").json()["Token"]
print(token)

# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0In0.SFRKiGgpznhtuKnjInNBUv4NKXur4yH4Z2CcBDui5QY"

res = upload(token, "test")
print(res)

res = download(token, res.json()["note_id"])
print(res.text)
