from fastapi import FastAPI, Request, Header
from typing import Annotated
from fastapi.responses import Response, RedirectResponse, FileResponse
from schemas import *
from uuid import uuid4
import json
import jwt

app = FastAPI(title="Note to Self")

with open("token.txt") as f:
    SECRET_TOKEN = f.read().strip()
    f.close()


def Error(msg, code):
    return Response(json.dumps({"Error": msg}), code)


def encode_token(user: str):
    payload = {"sub": user}
    return jwt.encode(payload, SECRET_TOKEN, "HS256")


def decode_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_TOKEN, ["HS256"])
        return decoded["sub"]
    except:
        return None


def users():
    with open("users.txt") as f:
        data = f.readlines()
        f.close()
    data = [x.strip() for x in data]
    return data


def active_users():
    with open("active_users.txt") as f:
        data = f.readlines()
        f.close()
    data = [x.strip() for x in data]
    return data


def not_admin():
    with open("not-admin.txt") as f:
        data = f.readlines()
        f.close()
    data = [x.strip() for x in data]
    return data


def add_user(user: str):
    with open("users.txt", "a") as f:
        f.write(user + "\n")
        f.close()


def add_not_admin(user: str):
    with open("not-admin.txt", "a") as f:
        f.write(user + "\n")
        f.close()


def add_active_user(user: str):
    with open("active_users.txt", "a") as f:
        f.write(user + "\n")
        f.close()


def write_note(user, content: str):
    note_id = str(uuid4())
    header = f"A note uploaded by {user}\n"
    with open(f"notes/{note_id}", "w") as f:
        f.write(header)
        f.write(content + "\n")
        f.close()
    if user not in not_admin():
        add_not_admin(user)
    return note_id


@app.get("/")
def root():
    return RedirectResponse("/docs", 301)


@app.post("/register")
def register(user: User):
    user = user.name.replace("\n", "")
    if user in users():
        return Error("Username is already registered.", 403)
    add_user(user)
    token = encode_token(user)
    return {"Token": token}


@app.get("/home")
def home(Token: Annotated[str, Header()]):
    user = decode_token(Token)
    if not user:
        return Error("Token is invalid.", 401)
    return {"OK": f"Hello {user}"}


@app.post("/notes/upload")
def upload(note: Note, Token: Annotated[str, Header()]):
    user = decode_token(Token)
    if not user:
        return Error("Token is invalid.", 401)
    if len(note.content) > 10000:
        return Error("Too long, we can not handle that.", 500)
    if user not in active_users():
        add_active_user(user)
    note_id = write_note(user, note.content)
    return {"note_id": note_id}


@app.get("/notes/download/{note_id}")
def download(note_id: str, Token: Annotated[str, Header()]):
    user = decode_token(Token)
    if not user:
        return Error("Token is invalid.", 401)
    # print(active_users())
    if user not in active_users():
        return Error("Only active user can download notes.", 403)
    filename = f"notes/{note_id}"
    try:
        open(filename).close()
    except:
        return Error("Something went wrong? No such file?", 404)
    # print(user.encode())
    # print(not_admin())
    # print(note_id)
    if note_id == "flag.txt" and user in not_admin():
        return Error("You are not allowed to download this file.", 403)

    return FileResponse(filename)
