#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    double calories_per_gram;
    double amount_in_grams;
    char name[50];
} Ingredient;

void init(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    alarm(180);
}

void show_flag(){
    printf("\nExcellent!\n");
    system("cat FLAG");
}

double calculate_total_calories(Ingredient ingredients[], int num_ingredients) {
    double total_calories = 0.0;
    for (int i = 0; i < num_ingredients; i++) {
        total_calories += ingredients[i].calories_per_gram * ingredients[i].amount_in_grams;
    }
    return total_calories;
}

int main() {
    init();

    Ingredient ingredients[3];
    printf("hint: show_flag = %p\n", (void *)show_flag);

    for (int i = 0; i <= 3; i++) {
        printf("\nEnter the name of ingredient %d: ", i + 1);
        scanf("%s", ingredients[i].name);

        printf("Enter the calories per gram for %s: ", ingredients[i].name);
        scanf("%lf", &ingredients[i].calories_per_gram);

        printf("Enter the amount in grams for %s: ", ingredients[i].name);
        scanf("%lf", &ingredients[i].amount_in_grams);
    }

    double total_calories = calculate_total_calories(ingredients, 3);

    printf("\nTotal calories for the meal: %.2f kcal\n", total_calories);

    return 0;
}
