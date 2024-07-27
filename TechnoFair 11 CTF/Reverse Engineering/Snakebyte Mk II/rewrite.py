with open("flag.py", "r") as f:
    lines = f.readlines()

# Write to flag.py the first element of split(",")
with open("test_flag.py", "w") as f:
    for line in lines:
        f.write(line.split(",")[0] + "\n")
