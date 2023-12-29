# ...

def main():
    banned = ['eval', 'exec', 'import', 'open', 'system', 'globals', 'os', 'password', 'admin']

    print("--- Prisoner Limited Access System ---")

    user = input("Enter your username: ")

    if user == "john":
        inp = input(f"{user} > ")

        while inp != "exit":
            for keyword in banned:
                if keyword in inp.lower():
                    print(f"Cannot execute unauthorized input {inp}")
                    print("I told you our system is hack-proof.")
                    exit()
            try:
                eval(inp)
            except:
                print(f"Cannot execute {inp}")
            
            inp = input(f"{user} > ")

    elif user == "admin":
        print("LOGGING IN TO ADMIN FROM PRISONER SHELL IS NOT ALLOWED")
        print("SHUTTING DOWN...")
        exit()
    
    else:
        print("User not found.")

# ...