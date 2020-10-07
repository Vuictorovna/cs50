from cs50 import get_int
from sys import exit


def get_positive_int():
    while True: 
        card_number = get_int("Number: ")
        if card_number > 0:
            return card_number


def main():
    iter = 0
    sum_odd = 0
    sum_even = 0
    d1 = 0
    d2 = 0
    doubled_digit = 0
    last_digit = 0
    sum_digit = 0
    check_sum = 0
    card_number = get_positive_int()
   
    while card_number > 0:
        digit = card_number % 10
        
        if iter % 2 == 0:
            sum_odd += digit
        else: 
            doubled_digit = digit * 2
            if doubled_digit >= 10:
                last_digit = doubled_digit % 10
                sum_digit = 1 + last_digit
                sum_even += sum_digit
            else:
                sum_even += doubled_digit
        
        card_number //= 10
        d2 = d1
        d1 = digit
        iter += 1 
        
    check_sum = sum_odd + sum_even
    if check_sum % 10 != 0:
        print("INVALID")
        exit(0)
   
    if iter == 15 and d1 == 3 and (d2 == 4 or d2 == 7):
        print("AMEX")
    elif iter == 16 and d1 == 5 and d2 >= 1 and d2 <= 5:
        print("MASTERCARD")
    elif (iter == 13 or iter == 16) and d1 == 4:
        print("VISA")
    else:
        print("INVALID")


main()