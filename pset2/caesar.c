#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //check of de input gelijk aan 2 is
    if(argc != 2)
    {
        printf("Error, integer required\n");
        return 1;
    }
    int key = atoi(argv[1]);
    //input string
    printf("plaintext: ");
    string formule = get_string();
    //ciphertext
    printf("ciphertext: ");
    for (int i = 0, n = strlen(formule); i < n; i++)
    {
            //Controleren of het een letter is
        if(isalpha(formule[i]))
        {
            //Als de input een kleine letter is....
            if(islower(formule[i]))
            {
            printf("%c", (((formule[i] + key) - 97) %26) + 97);
            }
            //Als de input een hoofdletter is.....
            if(isupper (formule[i]))
            {
                printf("%c", (((formule[i] + key) - 65) %26) + 65);
            }
        }
            //Als het geen letter is, dan schijf je de input op het scherm
        else
        {
            printf("%c", formule[i]);
        }
    }
    printf("\n");
}