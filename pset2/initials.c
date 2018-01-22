#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    //input
    string naam = get_string();
    printf("%c", toupper(naam[0]));
    //loop om te kijken wanneer het een spatie tegenkomt en de eerst volgende letter print
    for(int i = 0; i < strlen(naam); i++)
    {
       if(naam[i] == ' ')
       {
            printf("%c", toupper(naam[i+1]));
            i++;
       }
    }
    printf("\n");
}