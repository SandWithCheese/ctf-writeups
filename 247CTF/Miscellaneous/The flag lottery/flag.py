import pwn, random, time

conn = pwn.remote("758e1f57871f83b9.247ctf.com", 50260)
secret = random.Random()
secret.seed(int(time.time()))
winning_choice = str(secret.random())
print(winning_choice)

conn.interactive()
