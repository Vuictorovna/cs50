from cs50 import get_float


def get_positive_float():
    while True: 
        change_dollars = get_float("Change owed: ")
        if change_dollars > 0:
            return change_dollars


def main():
    change_dollars = get_positive_float()
    left = round(change_dollars * 100)
    change_coins_count = 0
    
    if left >= 25:
        change_coins_count += left // 25
        left %= 25
    
    if left >= 10:
        change_coins_count += left // 10
        left %= 10
    
    if left >= 5:
        change_coins_count += left // 5
        left %= 5
    
    change_coins_count += left

    print(change_coins_count)
    

main()