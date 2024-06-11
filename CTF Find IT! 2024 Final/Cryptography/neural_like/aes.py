import base64
from Crypto.Cipher import AES

def aes_encrypt(message, aes_key, iv):
    output = "error encryption"
    for i in range(100):
        try:
            cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            padded_message = message + (16 - len(message) % 16) * ' '
            encrypted_message = cipher.encrypt(padded_message.encode())
            output = base64.b64encode(encrypted_message).decode('utf-8')
            break
        except:
            print("Encryption error! Retrying...")
            pass
    return output
    