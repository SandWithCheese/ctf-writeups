#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char pin[8];

void setup()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    FILE *f = fopen("/dev/urandom", "r");
    size_t i = 0;
    while (i < 6)
    {
        char c = getc(f);
        if (c >= '0' && c <= '9')
        {
            pin[i++] = c;
        }
    }
    fclose(f);
    f = fopen("/tmp/pin", "w"); // pretend that admin can access /tmp/pin anytime :)
    fprintf(f, "%s\n", pin);
    fclose(f);
}

int auth()
{
    char buf[8];
    for (int i = 0; i < 3; i++)
    {
        printf("PIN: ");
        fread(buf, sizeof(*buf), 6, stdin);
        if (strncmp(pin, buf, 6) == 0)
        {
            return 1;
        }
    }
    return 0;
}

void scream(char *s)
{
    int i = 0;
    while (s[i] != '\0')
    {
        s[i] = toupper(s[i]);
        i++;
    }
}

void print_flag()
{
    char flag[100];
    FILE *f = fopen("./flag.txt", "r");
    if (f == NULL)
    {
        printf("flag.txt not found, please contact @msfir on Discord\n");
        exit(0);
    }
    flag[fread(flag, sizeof(*flag), sizeof(flag), f)] = '\0';
    fclose(f);
    printf("%s\n", flag);
}
int main()
{
    char buf[100];
    char username[100];
    int choice;

    setup();

    printf("Username: ");
    scanf("%s%*c", username);

    if (strcmp(username, "admin") == 0 && !auth())
    {
        printf("Authentication failed.\n");
        return 1;
    }

    while (1)
    {
        printf("Hello, %s!\n", username);
        printf("1. Scream\n");
        printf("2. Get secret\n");
        printf("3. Exit\n");
        printf(">> ");
        scanf("%d", &choice);
        if (choice == 1)
        {
            printf("Message: ");
            scanf("%s%*c", buf);
            scream(buf);
            printf("%s\n", buf);
        }
        else if (choice == 2)
        {
            if (strcmp(username, "admin") != 0)
            {
                printf("You're not admin!\n");
            }
            else
            {
                print_flag();
            }
        }
        else if (choice == 3)
        {
            printf("Goodbye!\n");
            return 0;
        }
        else
        {
            printf("Invalid choice!\n");
        }
    }
}
