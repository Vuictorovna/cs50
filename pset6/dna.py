from sys import argv, exit
import csv


def find_chain_len(sequence, pattern, start_pos):
    STR_count = 0
    current = start_pos
    STR = len(pattern)
    while sequence[current: current + STR] == pattern:
        STR_count += 1
        current = current + STR
    return STR_count


def find_max_patterns(sequence, pattern):
    STR = len(pattern)
    summa = []
    for y in range(0, len(sequence)):
        if sequence[y: y + STR] == pattern:
            count = find_chain_len(sequence, pattern, y)
            summa.append(count)
    if len(summa) > 0:
        max_patterns = max(summa)
    else:
        max_patterns = 0
    return max_patterns

    # из csv файла возвращает следующую строку
    
    
def taking_example(csvreader):
    example = next(csvreader, 'end')
    return example
    

def comparison(sample, example):
    for x in range(1, len(example)):
        if int(example[x]) != sample[x-1]:
            return False
    return True
    

def main():
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    with open(argv[2], "r") as file:
        sequence = file.read()

    with open(argv[1], "r") as file_csv:
        csvreader = csv.reader(file_csv)
        data = next(csvreader)

        sample = []
        for n in range(1, len(data)):
            result = find_max_patterns(sequence, data[n])
            sample.append(result)

        while True:
            example = taking_example(csvreader)
            if example == 'end':
                print("No match")
                return
            if comparison(sample, example) == True:
                print(example[0])
                return


main()
