from secret import cal
import hashlib

enc = []
for char in cal:
    x = ord(char)
    x = hashlib.md5(str(x).encode()).hexdigest()
    enc.append(int(x, 16))
        
with open('my_diary_11_8_Wednesday.txt', 'w') as f:
    f.write(str(enc))
