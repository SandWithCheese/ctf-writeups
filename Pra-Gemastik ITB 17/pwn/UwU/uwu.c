#include <stdio.h>

int main()
{
    char flag[64];
    FILE *f;

    f = fopen("flag.txt", "r");
    fscanf(f, "%s", flag);
    fclose(f);
    size_t ptr = (size_t)flag;

    size_t num = 0;
    f = fopen("/dev/urandom", "r");
    fread(&num, 1, sizeof(num), f);

    printf("Gimme flag address ♡〜٩( ˃▿˂ )۶〜♡: ");
    scanf("%ld", &ptr);

    size_t pass;
    printf("Are ya hooman (o_O)? Type %ld: ", num);
    scanf("%ld", &pass);

    if (pass == num)
    {
        printf("Ya hooman! Imma give ya the flag, or maybe not ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧\n");
        printf("%s\n", (char *)ptr);
    }
    else
    {
        printf("Ya no hooman ( ｡ •̀ ᴖ •́ ｡)\n");
    }

    return 0;
}
