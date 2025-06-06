#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool check(const char* str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        if (str[i] != str[len - 1 - i]) {
            return false;
        }
    }
    return true;
}

int main() {
    char input[100];
    int len;
    bool valid = true;

    scanf("%s", input);
    len = strlen(input);

    // Check if string is palindrome
    valid = valid && check(input);

    // Check if length is 21 (0x15)
    valid = valid && (len == 21);

    // Check for 'a' characters at specific positions
    valid = valid && (len > 20 &&
        input[0] == 'a' &&
        input[2] == 'a' &&
        input[4] == 'a' &&
        input[7] == 'a' &&
        input[9] == 'a');

    // Check relationship between characters
    valid = valid && (len > 3 &&
        input[1] == (input[3] - 1));

    // Check for 'm' at specific position
    valid = valid && (len > 19 &&
        input[19] == 'm');

    // Check for 'p' at specific position
    valid = valid && (len > 15 &&
        input[15] == 'p');

    // Check relationship between characters
    valid = valid && (len > 6 &&
        input[6] == (input[5] - 4));

    // Check if characters at specific positions are equal
    valid = valid && (len > 17 &&
        input[8] == input[17]);

    // Check for 'c' at specific position
    valid = valid && (len > 10 &&
        input[10] == 'c');

    if (valid) {
        printf("%s\n", input);
    }
    else {
        puts("Wrong!");
    }

    return 0;
}
