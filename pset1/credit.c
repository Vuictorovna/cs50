#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    long card_number;
    do
    {
        card_number = get_long("Number: ");
    }
    while (card_number < 0);
    
    int iter = 0; 
    int sum_odd = 0;
    int sum_even = 0;
    int d1 = 0;
    int d2 = 0;

    while (card_number > 0)
    {
        long digit = card_number % 10;
        if (iter % 2 == 0)
        {
            sum_odd += digit; 
        }
        else 
        {
            int doubled_digit = digit * 2;
            if (doubled_digit >= 10)
            {
                int last_digit = doubled_digit % 10;
                int sum_digit = 1 + last_digit;
                sum_even += sum_digit;
            }
            else
            {
                sum_even += doubled_digit;
            }
        }
        card_number /= 10;
        d2 = d1;
        d1 = digit;
        iter ++ ;
        
    }
     
    int check_sum = sum_odd + sum_even;
    if (check_sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
   
   
    if (iter == 15 && d1 == 3 && (d2 == 4 || d2 == 7))
    {
        printf("AMEX\n");
    }
    else if (iter == 16 && d1 == 5 && d2 >= 1 && d2 <= 5)
    {
        printf("MASTERCARD\n");
    }
    else if ((iter == 13 || iter == 16) && d1 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
