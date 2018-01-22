#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
     //check of input 2 is
    if(argc != 2)
    {
        printf("Error, integer required\n");
        return 1;
    }
    string key = argv[1];
    int lengte = strlen(key);
    //check of de input letters zijn
    for (int i = 0; i < strlen(key); i++)
    {
        if(!isalpha(key[i]))
        {
            printf("Only letters!!\n");
            return 1;
        }
    }
    //input van string
    printf("plaintext: ");
    string formule = get_string();
    printf("ciphertext: ");

    //loop omzetten input
    for (int i = 0, x = 0, y = strlen(formule); i < y; i++)
    {
        // Geef key voor deze letter
        int letter = tolower(key[x % lengte]) - 97;
        if (isupper(formule[i]))
        {
            //voor de letters in key, neem A en a als 0, B en b als 1, etc...
            printf("%c", 'A' + (formule[i] - 'A' + letter) % 26);
            x++;
        }
        else if(islower(formule[i]))
        {
            //voor de letters in key, neem A en a als 0, B en b als 1, etc...
            printf("%c", 'a' + (formule[i] - 'a' + letter) % 26);
            x++;
        }
        else
        {
            // return
            printf("%c", formule[i]);
        }
    }
    printf("\n");
    return 0;
}