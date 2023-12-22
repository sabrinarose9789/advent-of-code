import argparse
import re

NUM_LETTERS_TO_DIGITS = {
    'one': '1',
    'two': '2', 
    'three': '3', 
    'four': '4', 
    'five': '5', 
    'six': '6', 
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def find_numbers(line):
    number = [x for x in line if x.isnumeric()]
    if number:
        return int(number[0] + number[-1])
    return 0


def find_all_numbers(list_of_nums, line):
    first_occur = None
    first_num = ''
    last_occur = None
    second_num = ''
    for x in list_of_nums:
        lind = line.find(x)
        if lind >= 0 and (first_occur is None or lind < first_occur):
            first_occur = lind
            first_num = NUM_LETTERS_TO_DIGITS.get(x, x)
        rind = line.rfind(x)
        if rind >= 0 and (last_occur is None or rind > last_occur):
            last_occur = rind
            second_num = NUM_LETTERS_TO_DIGITS.get(x, x)
    return int(first_num + second_num)


def sum_calibaration_values(filename):
    total = 0
    total_2 = 0
    list_of_nums = list(NUM_LETTERS_TO_DIGITS.values()) + \
                   list(NUM_LETTERS_TO_DIGITS.keys())
    print(list_of_nums)
    with open(filename) as f:
        for line in f.readlines():
            total += find_numbers(line)
            total_2 += find_all_numbers(list_of_nums, line)
    print(total)
    print(total_2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Trebuchet?!",
                description = 'Sum the calibration values'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    sum_calibaration_values(args.filename)