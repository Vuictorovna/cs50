from cs50 import get_string


def count_letters(text):
    count = 0
    for ch in text:
        if ch.isalpha() == True:
            count += 1
    return count


def main():
    text = get_string("Text: ")
    count = count_letters(text)
    words = 1
    sentence = 0
    for ch in text:
        if ch == ' ':
            words += 1
        if ch == '?' or ch == '!' or ch == '.':
            sentence += 1

    L = (count * 100.0) / words
    S = (sentence * 100.0) / words
    index = round(0.0588 * L - 0.296 * S - 15.8)
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


main()
