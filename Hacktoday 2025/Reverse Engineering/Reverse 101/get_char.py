# Script untuk brute force beberapa rules
for a1 in range(256):
    # Rule yang akan dicek
    if (a1 & 0xF0) | 7 == 103:
        print(a1)
