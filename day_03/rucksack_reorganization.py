# mr.elf failed at packing
# rucksack design
#   2 large compartments
#   all items of a given type go into exactly one of the two compartments
#   each item type is identified by a single lower or upper case letter (a and A are dif types)
# Input: list of all items currently in each rucksack
#   each row is characters of all items in 1 rucksack. 
#   first half is items in first compartment, second half is items in second
# Item priority: a-z have priority 1-26, A-Z priority 27-52
# Find items in both halves, sum of their priorities

import argparse

def get_priority(chr):
    if chr.islower():
        return ord(chr) - 96
    else:
        return ord(chr) - 38


def reorganize(filename):
    priority_sum = 0
    group_items = []
    badge_sum = 0
    with open(filename) as f:
        for line in f.readlines():
            hp = len(line.strip()) // 2
            first_half = set(line[:hp])
            second_half = set(line[hp:])
            repeat = first_half.intersection(second_half)
            for val in repeat:
                priority_sum += get_priority(val)
            group_items.append(set(line.strip()))
            if len(group_items) == 3:
                int_1 = group_items[0].intersection(group_items[1])
                final = group_items[2].intersection(int_1)
                for badge in final:
                    # should only be one
                    badge_sum += get_priority(badge)
                group_items = []
    print(f"REORGANIZE SUM: {priority_sum}\nBADGE SUM: {badge_sum}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "RucksackReorganization",
                description = 'fReorganize the rucksack'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    reorganize(args.filename)