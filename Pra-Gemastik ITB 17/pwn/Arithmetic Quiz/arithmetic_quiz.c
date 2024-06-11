#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void timeout(int n)
{
    printf("Time out!\n");
    exit(0);
}

void setup()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(30);
}

int randint()
{
    int result;
    FILE *f = fopen("/dev/urandom", "r");
    fread(&result, sizeof(result), 1, f);
    fclose(f);
    return result;
}

double add(double a, double b)
{
    return a + b;
}

double subtract(double a, double b)
{
    return a - b;
}

double multiply(double a, double b)
{
    return a * b;
}

double divide(double a, double b)
{
    return a / b;
}

typedef double (*operation)(double, double);
const char operators[] = {'+', '-', '*', '/'};
const operation operations[] = {
    ['+'] = add,
    ['-'] = subtract,
    ['*'] = multiply,
    ['/'] = divide,
};

void feedback()
{
    char buf[256];
    printf("What do you think about this quiz?\n");
    printf(">> ");
    gets(buf);
    printf("Thank you!\n");
}

int main()
{
    setup();

    double a = randint() % 100;
    double b = randint() % 100;
    char op = operators[randint() % sizeof(operators)];
    double result = operations[(size_t)op](a, b);
    double answer;

    printf("Here is your question\n");
    printf("%g %c %g = ", a, op, b);

    for (int i = 0; i < 2; i++)
    {
        scanf("%lf%*c", &answer);
        printf("Your answer, ");
        printf((char *)&answer);
        printf(", is ");
        if (answer == result)
        {
            printf("correct :)\n");
            break;
        }
        else
        {
            if (i == 0)
            {
                printf("wrong :(\n");
                printf("But I'll give you a second chance.\n");
                printf("What's the answer?\n");
                printf(">> ");
            }
            else
            {
                printf("wrong again :(\n");
            }
        }
    }
    feedback();
    return 0;
}
