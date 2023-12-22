# reindeer need energy, snack on star fruit
# elves go to get stuff on foot
# Input: number of calories each elf is carrying
# Elf writes how calorie of each item they carry  by line
# When new elf starts writing, skips one line
# want to know which elf is carrying the most snacks
import argparse


def most_eaten(filename):
    elfs_cal = []
    elf = 0
    with open(filename) as r:
        for line in r.readlines():
            if line != "\n":
                elf += int(line)
            else:
                elfs_cal.append(elf)
                elf = 0
    elfs_cal.append(elf)
    elfs_cal.sort(reverse=True)
    print(elfs_cal[0], sum(elfs_cal[:3]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "calorieCounter",
                description = 'finds the elf carrying the most calories'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    most_eaten(args.filename)