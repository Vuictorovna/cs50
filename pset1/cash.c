#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float change_dollars;
    do
    {
        change_dollars = get_float("Change owed: ");
    }
    while (change_dollars < 0);

    int left = round(change_dollars * 100);
    int change_coins_count = 0;
    if (left >= 25)
    {
        change_coins_count += left / 25;
        left %= 25;
    }
    if (left >= 10)
    {
        change_coins_count += left / 10;
        left %= 10;
    }
    if (left >= 5)
    {
        change_coins_count += left / 5;
        left %= 5;
    }
    change_coins_count += left;

    printf("%i\n", change_coins_count);
}