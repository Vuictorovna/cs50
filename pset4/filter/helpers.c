#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][width - j - 1];
            image[i][width - j - 1] = image[i][j];
            image[i][j] = tmp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            int count = 0;

            for (int a = i - 1; a <= i + 1; a++)
            {
                for (int b = j - 1; b <= j + 1; b++)
                {
                    if (a < 0 || b < 0 || a >= height || b >= width)
                    {
                        continue;
                    }
                    sumRed += image[a][b].rgbtRed;
                    sumGreen += image[a][b].rgbtGreen;
                    sumBlue += image[a][b].rgbtBlue;
                    count++;
                }
            }

            int avrRed = round(sumRed / (float) count);
            int avrGreen = round(sumGreen / (float) count);
            int avrBlue = round(sumBlue / (float) count);

            tmp[i][j].rgbtRed = avrRed;
            tmp[i][j].rgbtGreen = avrGreen;
            tmp[i][j].rgbtBlue = avrBlue;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tmp[i][j];
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int GxRed = 0;
            int GxGreen = 0;
            int GxBlue = 0;
            int GyRed = 0;
            int GyGreen = 0;
            int GyBlue = 0;
            
            for (int a = i - 1; a <= i + 1; a++)
            {
                for (int b = j - 1; b <= j + 1; b++)
                {
                    if (a < 0 || b < 0 || a >= height || b >= width)
                    {
                        continue;
                    }

                    int ga = a - (i - 1);
                    int gb = b - (j - 1);
                    
                    int gx = Gx[ga][gb];
                    GxRed += image[a][b].rgbtRed * gx;
                    GxGreen += image[a][b].rgbtGreen * gx;
                    GxBlue += image[a][b].rgbtBlue * gx;

                    int gy = Gy[ga][gb];
                    GyRed += image[a][b].rgbtRed * gy;
                    GyGreen += image[a][b].rgbtGreen * gy;
                    GyBlue += image[a][b].rgbtBlue * gy;
                }
            }

            int finalRed = round(sqrt(GxRed * GxRed + GyRed * GyRed));
            int finalGreen = round(sqrt(GxGreen * GxGreen + GyGreen * GyGreen));
            int finalBlue = round(sqrt(GxBlue * GxBlue + GyBlue * GyBlue));

            if (finalRed > 255)
            {
                finalRed = 255;
            }
            if (finalGreen > 255)
            {
                finalGreen = 255;
            }
            if (finalBlue > 255)
            {
                finalBlue = 255;
            }

            tmp[i][j].rgbtRed = finalRed;
            tmp[i][j].rgbtGreen = finalGreen;
            tmp[i][j].rgbtBlue = finalBlue;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tmp[i][j];
        }
    }
}
