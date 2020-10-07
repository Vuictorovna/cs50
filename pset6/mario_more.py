from cs50 import get_int


def get_positive_int():
    while True: 
        n = get_int("Height: ")
        if n >= 1 and n <= 8:
            return n


def main():
    n = get_positive_int()
    for i in range(n):
        for j in range(0, n-i-1):
            print(" ", end="")
        for j in range(0, i+1):
            print("#", end="")
        print("  ", end="")
        for j in range(0, i+1):
            print("#", end="")
        print('\n', end="")
        

main()