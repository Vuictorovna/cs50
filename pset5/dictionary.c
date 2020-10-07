// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *table[N];

unsigned int dict_size = 0;

node *createNode(char *word);
void insertNode(unsigned int key, node *n);

// Returns true if word is in dictionary else false
bool check(const char *word)
{
   unsigned int key = hash(word);
   node *cursor = table[key];
   while (cursor != NULL)
   {
       if (strcasecmp(cursor->word, word) != 0)
       {
           cursor = cursor->next;
       }
       else
       {
           return true;
       }
   }
   return false;
}

// Hashes word to a number
// djb2 by Dan Bernstein
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c = 0;

    while (c == *word++)
    {
        hash = ((hash << 5) + hash) + c;
    }

    unsigned int newhash = hash % N;
    return newhash;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        return false;
    }

    char buffer[45];
    while( fscanf(file, "%s", buffer) != EOF )
    {
        node *result = createNode(buffer);
        if (result == NULL)
        {
            return false;
        }
        unsigned int key = hash(result->word);
        insertNode(key, result);

        dict_size++;
    }

    fclose(file);
    return true;
}

void insertNode(unsigned int key, node *n)
{
    if (table[key] != NULL)
    {
        n->next = table[key];
    }
    table[key] = n;
}

node *createNode(char *word)
{
    node *newnode = malloc(sizeof(node));
    if (newnode == NULL)
    {
        return NULL;
    }
    strcpy(newnode->word, word);
    newnode->next = NULL;
    return newnode;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    
    return true;
}
