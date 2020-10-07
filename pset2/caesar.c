#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

bool is_input_valid(int argc, string argv[]); 

char calc_cipher(char c, int key, char base)
{
    char idx = c - base;
    return (idx + key) % 26 + base;
}


int main(int argc, string argv[])
{
    if (!is_input_valid(argc, argv))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    int key = atoi(argv[1]);
   
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char ch  = plaintext[i];
        if (isalpha(ch)) 
        {
            char base = 'A';
            if (islower(ch))
            {
                base = 'a';
            }
            ch = calc_cipher(ch, key, base); 
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
        return false;
    }

    string key = argv[1];
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        char x = key[i];
        if (isalpha(x))
        {
            return false;
        }
    } 
    return true;
}
