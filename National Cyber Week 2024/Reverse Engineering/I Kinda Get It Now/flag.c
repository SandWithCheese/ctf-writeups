#include <stdio.h>
#include <string.h>
#include <stdint.h>

void reverse_transform5(unsigned char* data, size_t len, int shift) {
    unsigned char temp[len];
    shift = shift % len;
    if (shift < 0) shift += len;
    for (size_t i = 0; i < len; i++) {
        temp[(i + len - shift) % len] = data[i];
    }
    memcpy(data, temp, len);
}

void reverse_transform4(unsigned char* data, size_t len, unsigned char* inverse_substitution_table) {
    for (size_t i = 0; i < len; i++) {
        data[i] = inverse_substitution_table[data[i]];
    }
}

unsigned char mod_inverse(unsigned char mult, uint16_t mod) {
    int a = mult, m = mod;
    int m0 = m, t, q;
    int x0 = 0, x1 = 1;

    if (m == 1) return 0;

    while (a > 1) {
        q = a / m;
        t = m;
        m = a % m, a = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }

    if (x1 < 0) x1 += m0;

    return (unsigned char)x1;
}

void reverse_transform3(unsigned char* data, size_t len, unsigned char mult, unsigned char add) {
    unsigned char inv_mult = mod_inverse(mult, 256);
    for (size_t i = 0; i < len; i++) {
        data[i] = (inv_mult * (data[i] - add)) % 256;
    }
}

void reverse_transform2(unsigned char* data, size_t len, unsigned char shift) {
    for (size_t i = 0; i < len; i++) {
        data[i] = (data[i] >> (shift & 0x1f)) | (data[i] << (8 - (shift & 0x1f)));
    }
}

void reverse_transform1(unsigned char* data, size_t len, unsigned char mod_val) {
    for (size_t i = 0; i < len; i++) {
        data[i] = (data[i] - i + mod_val) % mod_val;
    }
}

void generate_inverse_substitution_table(unsigned char* table, unsigned char* inverse_table) {
    for (int i = 0; i < 256; i++) {
        inverse_table[table[i]] = i;
    }
}

void decrypt(void* input, size_t len, unsigned char* substitution_table, void* output) {
    memcpy(output, input, len);

    unsigned char inverse_substitution_table[256];
    generate_inverse_substitution_table(substitution_table, inverse_substitution_table);

    for (int i = 9; i >= 0; i--) {
        reverse_transform5(output, len, 2);
        reverse_transform4(output, len, inverse_substitution_table);
        reverse_transform3(output, len, 5, 8);
        reverse_transform2(output, len, 3);
        reverse_transform1(output, len, 0xFF);
    }
}

void generate_substitution_table(unsigned char* table) {
    uint32_t seed = 0x3039;
    for (int i = 0; i < 256; i++) {
        table[i] = (unsigned char)i;
    }
    for (int i = 255; i > 0; i--) {
        seed = (seed * 0x41c64e6d + 0x3039) % 0x7fffffff;
        uint32_t j = seed % (i + 1);
        unsigned char temp = table[i];
        table[i] = table[j];
        table[j] = temp;
    }
}

int main() {
    unsigned char ciphertext[] = { 107, 207, 161, 72, 67, 246, 216, 243, 182, 94, 113, 117, 163, 2, 159 };
    size_t len = sizeof(ciphertext);
    unsigned char substitution_table[256];

    generate_substitution_table(substitution_table);

    unsigned char decrypted[len];
    decrypt(ciphertext, len, substitution_table, decrypted);

    printf("Decrypted plaintext: ");
    for (size_t i = 0; i < len; i++) {
        printf("%c", decrypted[i]);
    }
    printf("\nDecryption Done!\n");

    return 0;
}
