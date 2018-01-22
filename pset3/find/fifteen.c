/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */

#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();

        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(500000);
        }

        // sleep thread for animation's sake
        usleep(500000);
    }

    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(2000000);
}


void init(void)
{
    int tile = d * d - 1;
    //row
    for(int row = 0; row < d; row++)
    {
        //colum
        for(int colum = 0; colum < d; colum++)
        {
            board[row][colum] = tile;
            tile--;
        }
    }

    // wisselt 1 en 2 om de game bij 4x4 te kunnen winnen
    if((d * d) % 2 == 0)
    {
        board[d - 1][d - 3] = 1;
        board[d - 1][d - 2] = 2;
    }
}

// Deze functie tekent het bord
void draw(void)
{
    for (int row = 0; row < d; row++)
    {
        for (int colom = 0; colom < d; colom++)
        {
            // Vervangt de 0 voor een '_'
            if(board[row][colom] == 0)
            {
                printf(" _ ");
            }
            else
            {
            printf("%2d ", board[row][colom]);
            }
        }
    printf("\n");
    }
}

// Deze functie verplaatst de tile en wisselt met de '_'
bool move(int tile)
{
    int tile_row;
    int tile_colom;
    int white_row;
    int white_colom;

     if (tile > d * d - 1 || tile < 1)
    {
        return false;
    }

    //zoek plaats van blokjes + wit blokje
    for (int row = 0; row < d; row++)
    {
        for (int colom = 0; colom < d; colom++)
        {
            if(board[row][colom] == tile)
            {
                tile_row = row;
                tile_colom = colom;
            }
            if(board[row][colom] == 0)
            {
                white_row = row;
                white_colom = colom;
            }
        }
    }

    // Hier worden de tile verplaatst
    if (tile == board[white_row - 1][white_colom])
    {
        board[white_row][white_colom] = tile;
        board[white_row - 1][white_colom] = 0;
        return true;
    }

    else if (tile == board[white_row + 1][white_colom])
    {
        board[white_row][white_colom] = tile;
        board[white_row + 1][white_colom] = 0;
        return true;
    }
    else if (tile == board[white_row][white_colom - 1])
    {
        board[white_row][white_colom] = tile;
        board[white_row][white_colom - 1] = 0;
        return true;
    }
    else if (tile == board[white_row][white_colom + 1])
    {
        board[white_row][white_colom] = tile;
        board[white_row][white_colom + 1] = 0;
        return true;
    }
    return false;
}


bool won(void)

{
    int counter = 1;

    for (int row = 0; row < d; row++)
    {
        for (int colom = 0; colom < d; colom++)
        {
            if (board[row][colom] == counter)
                counter++;
        }
    }

    if (counter == d * d && board[d - 1][d - 1] == 0)
        return true;
    else
    {
        return false;
    }
}