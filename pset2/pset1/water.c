#include <cs50.h>
#include <stdio.h>



int main(void)
{

    printf("Minutes:");
    int minutes = get_int();                            //maak input aan

    if (minutes >= 0)
    {
    printf("Bottles: %i \n", minutes * 12);
    }
        else if (minutes < 0)                           //Als het aantal minuten negatief is, zal dit neit worden goedgekeurd
        {
        printf("Invalid number \n");

        }
            return 0;

}

