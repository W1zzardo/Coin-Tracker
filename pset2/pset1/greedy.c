#include <cs50.h>
#include <stdio.h>
#include <math.h>


int main(void)
{


int cents= 0;
int quarters= 25;
int dimes= 10;                                  //Variabelen alvast een waarde geven
int nickels=5;
int pennies= 1;
float amount;                             //Hoeveel geld is er verschuldigd
int rest;

do{
   printf("How much change is owed?\n");
   amount = get_float();
  }
  while(amount < 0);

    rest = round(100*amount);                  //Het bedrag omrekenen naar centen
    double round (double rest);

while (rest >= quarters)
    {
        cents++;
        rest = (rest - quarters);
    }


while (rest >= dimes)
    {
        cents++;
        rest = (rest - dimes);                     //Het tellen van de munten
    }

while (rest >= nickels)
    {
        cents++;
        rest = (rest - nickels);
    }


while (rest >= pennies)
    {
        cents++;
        rest = rest - pennies;
    }


printf("%d\n", cents);                        //Zet het aantal munten die nodig zijn op het scherm (output)

return 0;

}