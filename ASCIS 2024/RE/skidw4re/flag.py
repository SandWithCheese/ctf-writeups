from Crypto.Cipher import AES

KEY, IV = (
    b"thisis32bitlongpassphraseimusing"[:16],
    b"thisis32bitlongpassphraseimusing"[16:],
)


def aes_gcm_decrypt(ciphertext, tag):
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=IV)
    # plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


print(aes_gcm_decrypt(bytes.fromhex("3d840a47b5ce38be626fa13500c53b5b")))
