from pwn import *
import base64
import hashlib

host, port = "165.232.133.53", "9081"

conn = remote(host, port)

# Wait for the initial prompt
conn.recvuntil(b"Please answer the following questions:\n\n")

# Answer all 6 questions automatically
answers = [
    "TrevorC2",  # Question 1: C2 server yang digunakan
    "aewfoijdc887xc6qwj21t",  # Question 2: Key yang digunakan oleh C2 server
    "whoami",  # Question 3: Perintah kedua yang dijalankan oleh C2 server
    "http://192.168.56.102:8888/m",  # Question 4: URL lengkap tempat threat actor mendownload malware
    "AES",  # Question 5: Jenis enkripsi yang digunakan oleh malware
    "7aeaef7351e88b7a",  # Question 6: Key yang digunakan untuk mengenkripsi file
    "b2195af3d80ec529",  # Question 7: IV yang digunakan untuk mengenkripsi file
    "remove flag hahaha",
    "Walawe1337!!@@"
]

for i, answer in enumerate(answers, 1):
    # Wait for the question prompt
    conn.recvuntil(f"No {i}:".encode())
    conn.recvuntil(b"Answer: ")

    # Send the answer
    try:
        conn.sendline(answer.encode())
    except:
        conn.sendline(answer)

    # Wait for response
    response = conn.recvline().decode().strip()
    print(f"Question {i}: {response}")

    # If incorrect, we might need to adjust the answer
    if "Incorrect" in response:
        print(f"Question {i} was incorrect. Answer: {answer}")

# After answering all questions, go interactive to see the final result
print("All questions answered. Going interactive...")
conn.interactive()
