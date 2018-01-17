#include <cs50.h>
#include <stdio.h>

int main(void)
{
    float dollars;
    do
    {
        printf("O hai! How much change is owed?\n");
        dollars = get_float();
    }
    while (dollars < 0);

    float temp = (dollars * 100);
    int cents = (temp + 0.5);
    int coins = 0;

        while (cents >= 25)
            {
            cents = cents - 25;
            coins = coins + 1;
            }

        while (cents >= 10 && cents < 25)
            {
            cents = cents - 10;
            coins = coins + 1;
            }

        while (cents >= 5 && cents < 10)
            {
            cents = cents - 5;
            coins = coins + 1;
            }

        while (cents >= 1 && cents < 5)
            {
            cents = cents - 1;
            coins = coins + 1;
            }
            printf("%i\n", coins);
}