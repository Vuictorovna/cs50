import cs50
import csv
from sys import argv, exit
from cs50 import SQL


db = SQL("sqlite:///students.db")


def main():
    if len(argv) != 2:
        print("Usage: python roster.py HouseName")
        exit(1)

    housemates = db.execute("SELECT first, middle, last, birth FROM students WHERE house = (?) ORDER BY last, first", argv[1])

    for row in housemates:
        if row["middle"] == None:
            print(row["first"] + " " + row["last"] + ", born " + str(row["birth"]))
        else:
            print(row["first"] + " " + row["middle"] + " " + row["last"] + ", born " + str(row["birth"]))


main()
