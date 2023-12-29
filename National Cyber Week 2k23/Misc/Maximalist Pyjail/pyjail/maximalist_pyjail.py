import string
import os
sessions = {}
account = []
uniq = os.urandom(16).hex()
os.mkdir(os.path.join(os.path.dirname(__file__), "feedback", uniq))
def register(username, password, role):
    try:
        sessid = os.urandom(16).hex()
        sessions[sessid] = username
        account.append((username, password, role))
        return sessid
    except:
        print("Something went wrong!")
        return 0
    
def login():
    try:
        print("1. Login with username and password")
        print("2. Login with session key")
        choice = input("Your choice: ")
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            for ind in range(len(account)):
                if account[ind][0] == username and account[ind][1] == password:
                    return [account[ind][0], account[ind][2]]
            print("Invalid username or password!")
            return [0, 0]
        elif choice == "2":
            sessid = input("Session key: ")
            username = sessions.get(sessid, 0).strip()
            if username == 0:
                print("Invalid session key!")
                return [0, 0]
            
            for ind in range(len(account)):
                if account[ind][0] == username:
                    return [account[ind][0], account[ind][2]]
        else:
            print("Invalid choice!")
            return [0, 0]
    except:
        print("Something went wrong!")
        return [0, 0]



register("admin_handsome_zzz", os.urandom(16).hex(), "admin")
name = role = 0    
while True:
    if name == 0 and role == 0:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Your choice: ")
        if choice == "1":
            username = input("Username: ")
            if username == "admin_handsome_zzz":
                print("You can't register as admin!")
                continue
            if username.strip() == "":
                print("Username can't be empty")
                continue
            password = input("Password: ")
            sessid = register(username, password, "user")
            if sessid == 0:
                continue
            print("Your session key: " + sessid)
            
        elif choice == "2":
            name, role = login()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

    elif role == "user":
        print("1. Try Calculator")
        print("2. Give a feedback")
        print("3. Logout")
        choice = input("Your choice: ")
        if choice == "1":
            print("-------CALCULATOR-------")
            exp = input("Input(X [+-*/] Y): ")
            if len(exp) > 30 or any([c not in string.ascii_letters+string.digits+" +-*/()" for c in exp]):
                print("Unfortunately this is still in development, so the calculator only supports simple expressions!")
                continue
            if len(exp.split(" + ")) == 2 or len(exp.split(" - ")) == 2 or len(exp.split(" * ")) == 2 or len(exp.split(" / ")) == 2:
                try:
                    print(eval(exp, {'__builtins__': None}, {'__builtins__': None}))
                except:
                    print("Something went wrong!")
            else:
                print("Invalid expression!")
        elif choice == "2":
            try:
                feedback_file = os.path.join(os.path.dirname(__file__), "feedback", uniq, name)
                try:
                    f = open(feedback_file, "r")
                    print("You've already given a feedback!")
                except:
                    f = open(feedback_file, "w")
                    f.write(input("Feedback: "))
                    print("Write feedback successfully!")
                    f.close()
            except:
                print("Something went wrong!")
        elif choice == "3":
            name = role = 0
        else:
            print("Invalid choice!")

    elif role == "admin":
        print("1. Try Calculator Newest Update")
        print("2. Logout")
        choice = input("Your choice: ")
        if choice == "1":
            print("-------CALCULATOR-------")
            exp = input("Input(X [+-*/] Y): ")
            if any([c not in string.printable for c in exp]) or any([c in exp for c in ["__", "'", "\""]]) or len(exp) > 120:
                print("admin I'm sorry, I'm afraid I can't let you do that!")
                continue
            try:
                print(eval(exp, {'__builtins__': None}, {'__builtins__': None}))
            except:
                print("Something went wrong!")
        elif choice == "2":
            name = role = 0
        else:
            print("Invalid choice!")