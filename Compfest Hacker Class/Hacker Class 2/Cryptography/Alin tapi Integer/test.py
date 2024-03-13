import numpy as np
import random

a = np.array([[1, 2], [3, 4]])
b = np.array([1, 2])
c = [
    1382837223529433249865880805057517251915619710567990062916431,
    1316535860531446525236099898143306829501741219648966991591354,
]

r = [
    [1148260253752960666411026955982, 1152853384449195147441103181809],
    [531286261948311003070916961777, 315004570177689845888128427159],
]

c = np.array(c)
r = np.array(r, dtype="float64")

test = np.linalg.inv(r)
# r = r * (1 / det)
# print(r)
# print(r)
temp = np.dot(c, test)
print(temp)



# print(np.dot(a, b))
# print(np.dot(b, a))

# print(random.getrandbits(100))
