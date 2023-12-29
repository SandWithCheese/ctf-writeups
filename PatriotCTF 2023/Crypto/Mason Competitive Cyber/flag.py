with open("MasonCompetitiveCyber.txt", "r") as f:
    lines = f.readlines()

flag_bin = ""
for line in lines:
    if "\\u200" in line:
        line = line.strip("\\u200")

    counter = (
        str(line.count("M"))
        + str(line.count("a"))
        + str(line.count("s"))
        + str(line.count("o"))
        + str(line.count("n"))
        + str(line.count("C"))
    )
    # for i in range(242, 256):
    #     if int(counter) % i == 80:
    #         print(i)
    #         quit()
    flag_bin += bin(int(counter))[2:]

for i in range(0, len(flag_bin), 8):
    block = flag_bin[i : i + 8]
    print(chr(int(block, 2)))
