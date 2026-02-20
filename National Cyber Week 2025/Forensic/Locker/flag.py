from pwn import *

HOST = "31.97.187.222"
PORT = 27312

# Put ALL answers here in order:
answers = [
    "11961",  # Q1
    "192.168.198.128",  # Q2
    "192.168.198.129:8000",  # Q3
    "DESKTOP-P15ADMF",  # Q4
    "belajar_calculus.pdf",  # Q5
    "chuongdoung.exe",  # Q6
    "/Work/secret/chuongdoung.exe",  # Q7
    "20/11/2025:03:21:31",  # Q8
    "a153d59a98200b035fcc4fbee153e4b3f75358221fb006358f704e574af02993",  # Q9
    "4", # Q10
    "T1055", # Q11
    "Application Layer Protocol", # Q12
    "14A929E9", # Q13
    "3871445A1BCFC5417780344C650551084BDEEE5C459FAF63014A07C25080097A", # Q14
    "72", # Q15
]


def main():
    r = remote(HOST, PORT)

    answer_index = 0

    while True:
        try:
            data = r.recvuntil(b"Answer:", timeout=5)
        except EOFError:
            print("\n[!] Remote host closed the connection.")
            break

        if not data:
            print("\n[!] No more data. Exiting.")
            break

        print(data.decode(errors="ignore"), end="")

        if answer_index >= len(answers):
            print("\n[!] No more answers in the list. Add more!")
            break

        send_answer = answers[answer_index] + "\n"
        print(f"> Sending answer: {answers[answer_index]}")
        r.send(send_answer.encode())

        answer_index += 1

        # Print any follow-up text before next question
        try:
            follow = r.recv(timeout=1)
            if follow:
                print(follow.decode(errors="ignore"), end="")
        except:
            pass

    r.interactive()


if __name__ == "__main__":
    main()
