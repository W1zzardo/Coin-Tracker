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

       //if needle is gelijk aan mid
       if(value == values[mid])
       {
           return true;
       }
       //If needle is kleiner dan mid
       else if(value < values[mid])
       {
           first = mid + 1;
       }
       //if needle is groter dan mid
       else if(value > values[mid])
       {
           last = mid - 1;
       }
    }
    // TODO: implement a searching algorithm
    return false;
}