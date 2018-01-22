#include <cs50.h>
#include "helpers.h"
#include <stdio.h>
#include <stdlib.h>


void sort(int values[], int n)
{
    int i;
    int j;

    for(i = 0; i < n-1; i++)
    {
        int controle = 0;
        for(j = i+1; j < n; j++)
        {
            if(values[i] < values[j])
            {
               int t = values[i];
               values[i] = values[j];
               values[j] = t;
               controle = 1;
            }
        }
    }
 // TODO: implement a sorting algorithm
return;
}