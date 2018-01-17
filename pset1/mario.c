#include <cs50.h>
#include <stdio.h>

void space(int n);
void hashtag(int n);
void say(string s, int n);

int main(void)
{
    int h;
    do
    {
        printf("Height: ");
        h = get_int();
    }
    while ( h < 0 || h > 23 );

    for(int i = 1; i <= h; i++)
        {
            space(h - i);
            hashtag(i + 1);
        printf("\n");
        }
}

void space(int n)
{
    say(" ", n);
}

void hashtag(int n)
{
    say("#", n);
}

void say(string s, int n)
{
    for(int i = 0; i < n; i++)
    {
        printf("%s", s);
    }
}