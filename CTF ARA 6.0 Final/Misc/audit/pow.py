import hashlib, random, uuid

DIFFICULTY = 6
myid = uuid.uuid4().hex
i = 0
while True:
	code = myid + '-' + str(i)
	hashed = hashlib.sha256(code.encode()).hexdigest()
	hashed = hashlib.sha256(hashed.encode()).hexdigest()
	if hashed.startswith('0' * DIFFICULTY):
		print(code)
		break
	i += 1
