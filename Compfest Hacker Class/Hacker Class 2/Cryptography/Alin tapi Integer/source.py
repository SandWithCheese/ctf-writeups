import random
import numpy as np

m = np.array([int(open("secret1.txt", "r").read()), int(open("secret2.txt", "r").read())])
r = np.array([[random.getrandbits(100), random.getrandbits(100)], [random.getrandbits(100), random.getrandbits(100)]])
e = np.array([random.getrandbits(100), random.getrandbits(100)])

c = np.dot(e, r) + m

print("r = {}".format(r))
print("c = {}".format(c))