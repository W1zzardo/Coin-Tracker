#include <cs50.h>
#include "helpers.h"
#include <stdio.h>
#include <stdlib.h>

bool search(int value, int values[], int n)
{
    int last = n - 1;
    int first = 0;

    while(first <= last)
    {
       int mid = first + ((last - first)/2);

       // if needle is gelijk aan mid
       if(value == values[mid])
       {
           return true;
       }
       // If needle is kleiner dan mid
       else if(value < values[mid])
       {
           first = mid + 1;
       }
       // if needle is groter dan mid
       else if(value > values[mid])
       {
           last = mid - 1;
       }
    }
    return false;
}


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
               // wisselen
               int wissel = values[i];
               values[i] = values[j];
               values[j] = wissel;
               controle = 1;
            }
        }
    }
return;
}
