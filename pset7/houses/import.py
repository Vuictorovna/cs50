import cs50
import csv
from sys import argv, exit
from cs50 import SQL


db = SQL("sqlite:///students.db")


def main():
    if len(argv) != 2:
        print("Usage: python import.py characters.csv")
        exit(1)

    with open(argv[1], 'r') as file_csv:
        csvreader = csv.DictReader(file_csv)

        for row in csvreader:
            name = row["name"]
            name_list = name.split()

            if len(name_list) == 2:
                first_name = name_list[0]
                last_name = name_list[1]
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", 
                           first_name, None, last_name, row["house"], row["birth"])
            elif len(name_list) == 3:
                first_name = name_list[0]
                middle_name = name_list[1]
                last_name = name_list[2]
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", 
                           first_name, middle_name, last_name, row["house"], row["birth"])


main()
