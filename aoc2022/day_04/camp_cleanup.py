# Clear up space to unload ships
# Each elf assigned job to clean up section of camp,
# identified by ID number
# Elf has multiple IDs to clean
# Overlap has happened, need to reduce duplicated effort

# INPUT: list of section assignments for pairs of elves

# find the assignment pairs where one range fully contains the other
import argparse 
import re

def find_pairs(filename):
    fully_contained = 0
    overlap = 0
    with open(filename) as f:
        for line in f.readlines():
            a_1, a_2, b_1, b_2 = re.split(',|-', line.strip())
            a_sections = set(range(int(a_1), int(a_2)+ 1))
            b_sections = set(range(int(b_1), int(b_2) + 1))
            if b_sections.issubset(a_sections) or a_sections.issubset(b_sections):
                fully_contained += 1
            if b_sections.intersection(a_sections):
                overlap += 1
    print(f"{fully_contained} of the pairs have complete overlap\n{overlap} have partial overlap")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "CampCleanup",
                description = 'finds completely overlapped clean up pairs'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    find_pairs(args.filename)