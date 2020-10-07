#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);

int main(int argc, string argv[])
{
    string text = get_string("Text: ");

    int count = count_letters(text);
    int words = 1;
    int sentence = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char ch = text[i];
        if (ch == ' ')
        {
            words ++;
        }
        if (ch == '?' || ch == '!' || ch == '.')
        {
            sentence ++;
        }
    }

    float L = (count * 100.0) / words;
    float S = (sentence * 100.0) / words;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

    return 0;
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char x = text[i];
        if (isalpha(x))
        {
            count ++;
        }
    }
    return count;
}


