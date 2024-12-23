#include <stdio.h>

int main() {
    char buf[100];
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 1, 0LL);
    printf("Welcome to Hackaday 2024! This is a very simple challenge :)");
    gets(buf);
    return 0;
}
