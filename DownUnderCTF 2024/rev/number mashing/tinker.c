#include <stdio.h>

int main() {
    int a, b, c;

    printf("Give me some numbers: ");
    scanf("%d %d", &a, &b);

    printf("a = %d, b = %d\n", a, b);

    printf("c = a / b = %d\n", a / b);


    return 0;
}

// a != 0
// b != 0 && b != 1
// c = a / b
// c = a