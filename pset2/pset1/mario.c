#include <cs50.h>
#include <stdio.h>



int main(void)
{

int h;                              //h staat voor hoogte
int s;                              //s staat voor spaties
int t;                              //t staat voor hashTag
int i;                              //i staat voor rijen

do {
    printf("Height:");
    h = get_int();
    }
    while (h < 0 || h > 23);                //Opnieuw als het ingevulde getal kleiner dan 0 is of groter dan 23, anders retry


        for (i= 1; i <= h; i++)
        {


            for (s= (h-i); s > 0; s--)                       //loop voor de spaties, als deze er niet is zal de piramide andersom zijn, zo krijg je opdracht 2
            {                                               // s definiëren
                printf(" ");
            }


               for (t = 1; t <= (i+1); t++)                   //loop voor de #
               {
                    printf("#");

               }
                    printf("\n");                           //regel overslaan zodat de # onder elkaar komen

         }

    return 0;


}


