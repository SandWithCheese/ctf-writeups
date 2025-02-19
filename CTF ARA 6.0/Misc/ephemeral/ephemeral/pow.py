import hashlib, random

DIFFICULTY = 6
rand = random.randint(100000, 10000000000000000)
for i in range(rand, 10000000000000000):
	hashed = hashlib.sha256(str(i).encode()).hexdigest()
	hashed = hashlib.sha256(hashed.encode()).hexdigest()
	if hashed.startswith('0' * DIFFICULTY):
		print(i)
		break