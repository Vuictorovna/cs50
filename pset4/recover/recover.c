#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>


typedef uint8_t BYTE;


bool is_jpeg(BYTE buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
}


int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        fprintf(stderr, "Invalid.\n");
        return 1;
    }

    const int BLOCK_SIZE = 512;

    BYTE buffer[BLOCK_SIZE];
    int fileNo = 0;
    char filename[8];
    FILE *img = NULL;

    while (true)
    {
        int rc = fread(buffer, BLOCK_SIZE, 1, file);
        if (rc != 1)
        {
            break;
        }
        if (is_jpeg(buffer))
        {
            if (fileNo != 0)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", fileNo);
            img = fopen(filename, "w");
            fileNo++;
        }
        if (img != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }
    fclose(img);
    fclose(file);
    return 0;
}


