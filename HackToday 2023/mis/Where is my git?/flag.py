import git

repo = git.Repo("./where-is-my-git")

with open("head.txt", "r") as f:
    heads = f.readlines()


flag = ""
idx = 1
for i in range(1, len(heads), 2):
    head = heads[i][:7]

    repo.git.reset("--hard", head)
    with open(f"./where-is-my-git/part-{idx}.txt", "r") as f:
        flag += f.read()

    idx += 1
print(flag)
