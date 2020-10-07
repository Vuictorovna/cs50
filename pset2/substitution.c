#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

bool is_input_valid(int argc, string argv[]);

char encode(char orig, string key, char base)
{
    int pos = orig - base;
    return key[pos];
}

int main(int argc, string argv[])
{
    if (!is_input_valid(argc, argv))
    {
        return 1;
    }
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    string key = argv[1];
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char ch = plaintext[i];
        if (isalpha(ch))
        {
            if (islower(ch))
            {
                ch =  tolower(encode(ch, key, 'a'));
            }
            else
            {
                ch = toupper(encode(ch, key, 'A'));
            }
        }
        printf("%c", ch);
    }
    printf("\n");

    return 0;
}

bool is_input_valid(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return false;
    }
    string key = argv[1];
    int n = strlen(key);
    for (int i = 0; i < n; i++)
    {
        if (isdigit(key[i]))
        {
            printf("Key must only contain alphabetic characters\n");
            return false;
        }
    }
    if (n != 26)
    {
        printf("Key must contain 26 characters\n");
        return false;
    }
    for (int i = 0; i < n; i++)
    {
        char x = tolower(key[i]);
        for (int j = 0; j < i; j++)
        {
            if (x == tolower(key[j]))
            {
                printf("Key must not contain repeated characters\n");
                return false;
            }
        }
    }
    return true;
}
