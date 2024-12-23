// package main

// import (
// 	"crypto/aes"
// 	"encoding/hex"
// 	"fmt"
// )

// func main() {
// 	// Example AES key
// 	key := []byte("thisis32bitlongpassphraseimusing")

// 	// Create a new AES cipher
// 	block, err := aes.NewCipher(key)
// 	if err != nil {
// 		panic(err)
// 	}

// 	// ciphertextHex := "3d840a47b5ce38be626fa13500c53b5b"
// 	ciphertextHex := "ef15394cddf8a4308a4a6d49f3dd1ab30680631e"
// 	saad, err := hex.DecodeString(ciphertextHex)
// 	fmt.Printf("Ciphertext: %x\n", saad)

// 	decrypted := make([]byte, aes.BlockSize)
// 	block.Decrypt(decrypted, saad)

// 	fmt.Printf("Decrypted: %s\n", string(decrypted))
// }

package main

import (
	"crypto/aes"
	"encoding/hex"
	"fmt"
)

// EncryptAES performs AES encryption with the given key and plaintext
func EncryptAES(key []byte, plaintext string) (string, error) {
	// Create a new AES cipher block with the key
	block, err := aes.NewCipher(key)
	if err != nil {
		return "", fmt.Errorf("failed to create cipher: %v", err)
	}

	// Convert plaintext string to a byte slice
	plaintextBytes := []byte(plaintext)

	// Make sure the plaintext is a multiple of the block size by padding if necessary
	blockSize := block.BlockSize()
	if len(plaintextBytes)%blockSize != 0 {
		padding := blockSize - (len(plaintextBytes) % blockSize)
		plaintextBytes = append(plaintextBytes, make([]byte, padding)...)
	}

	// Encrypt the plaintext (in-place encryption)
	ciphertext := make([]byte, len(plaintextBytes))
	for i := 0; i < len(plaintextBytes); i += blockSize {
		block.Encrypt(ciphertext[i:i+blockSize], plaintextBytes[i:i+blockSize])
	}

	// Return the encrypted result as a hex-encoded string
	return hex.EncodeToString(ciphertext), nil
}

// EncryptFinal prepares key and plaintext, and performs the encryption
func EncryptFinal() {
	// Example key and plaintext
	key := []byte("thisis32bitlongpassphraseimusing") // 32 bytes key
	plaintext := "The eye of eagle"           // example plaintext

	// Encrypt the plaintext using AES
	encryptedText, err := EncryptAES(key, plaintext)
	if err != nil {
		fmt.Println("Error during encryption:", err)
		return
	}

	// Print the encrypted text
	fmt.Println("Encrypted text:", encryptedText)
}

func main() {
	EncryptFinal()
}
