from pwn import *
import base64
import hashlib

host, port = "165.232.133.53", "9081"

# All possible keys for question 6
question6_keys = [
    "0000000000000000",
    "0000000000000010",
    "0010000000000000",
    "0100000000000000",
    "0111111111111111",
    "0123456789abcdef",
    "0999999999999999",
    "1111111111111111",
    "1234567890123456",
    "162ad6776fa00aa7",
    "1652638804087794",
    "2856903984951653",
    "3333333333333333",
    "3456789012345678",
    "3d95607ce6f7d521",
    "4254076641128259",
    "4b18355671751add",
    "553ec4088cec8ed6",
    "5678901234567890",
    "7320508075688772",
    "773b1ef8788b576e",
    "7890123456789012",
    "792add41cea7895a",
    "7a5564aefc2ffbca",
    "7aeaef7351e88b7a",
    "803536a47f1d4de1",
    "839d7893943782ee",
    "8519278097689642",
    "9012345678901234",
    "90dae675c059a097",
    "92b0dcacf4dff82a",
    "95eb58ba6c98b013",
    "a3424de66a44bf3a",
    "a4337bc45a8fc544",
    "b2195af3d80ec529",
    "b274fb77fecf1db6",
    "ba071f82c28477e1",
    "c03f52dc550cd6e1",
    "cf0d0240c010bd65",
    "d5de9dd3bb756afa",
    "d7e8a010a7c856ce",
    "e37569c26f8522d2",
    "e87021bc896588bd",
    "e911b2e478f8dedf",
    "f51579ae8d93c865",
]


def try_question6():
    print(f"Testing {len(question6_keys)} keys for question 6...")

    for i, key in enumerate(question6_keys):
        print(f"Trying key {i+1}/{len(question6_keys)}: {key}")

        # Create a new connection for each attempt
        conn = remote(host, port)

        try:
            # Wait for the initial prompt
            conn.recvuntil(b"Please answer the following questions:\n\n")

            # Answer first 5 questions
            answers = [
                "TrevorC2",  # Question 1: C2 server yang digunakan
                "aewfoijdc887xc6qwj21t",  # Question 2: Key yang digunakan oleh C2 server
                "whoami",  # Question 3: Perintah kedua yang dijalankan oleh C2 server
                "http://192.168.56.102:8888/m",  # Question 4: URL lengkap tempat threat actor mendownload malware
                "AES",  # Question 5: Jenis enkripsi yang digunakan oleh malware
            ]

            for j, answer in enumerate(answers, 1):
                # Wait for the question prompt
                conn.recvuntil(f"No {j}:".encode())
                conn.recvuntil(b"Answer: ")

                # Send the answer
                conn.sendline(answer.encode())

                # Wait for response
                response = conn.recvline().decode().strip()
                print(f"  Question {j}: {response}")

                if "Incorrect" in response:
                    print(f"  Question {j} failed, stopping this attempt")
                    break

            # Now try question 6 with the current key
            conn.recvuntil(f"No 6:".encode())
            conn.recvuntil(b"Answer: ")

            # Send the key
            conn.sendline(key.encode())

            # Wait for response
            response = conn.recvline().decode().strip()
            print(f"  Question 6: {response}")

            if "Correct" in response:
                print(f"\n🎉 SUCCESS! The correct key for question 6 is: {key}")
                return key
            elif "Incorrect" in response:
                print(f"  Key {key} is incorrect")
            else:
                print(f"  Unexpected response: {response}")

        except Exception as e:
            print(f"  Error with key {key}: {e}")
        finally:
            conn.close()

        print(f"  ---")

    print("\n❌ No correct key found among the provided keys")
    return None


if __name__ == "__main__":
    correct_key = try_question6()
    if correct_key:
        print(f"\n✅ Final answer: {correct_key}")
    else:
        print("\n❌ Need to investigate further or try different keys")
