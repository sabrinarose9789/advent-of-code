import argparse
import numpy as np

def tilt_north(rocks):
    changed_rocks = True
    while changed_rocks:
        changed_rocks = False 
        for i, row in enumerate(rocks[1:], 1):
            for j, val in enumerate(row):
                if val == "O":
                    above_val = rocks[i-1][j]
                    if above_val == ".":
                        rocks[i] = rocks[i][:j] + "." + rocks[i][j+1:]
                        rocks[i - 1] = rocks[i - 1][:j] + "O" + rocks[i - 1][j+1:]
                        changed_rocks = True
    return rocks

def tilt_south(rocks):
    changed_rocks = True
    r_m = len(rocks)
    while changed_rocks:
        changed_rocks = False 
        for i in range(r_m - 2, -1, -1):
            row = rocks[i]
            for j, val in enumerate(row):
                if val == "O":
                    above_val = rocks[i+1][j]
                    if above_val == ".":
                        rocks[i] = rocks[i][:j] + "." + rocks[i][j+1:]
                        rocks[i + 1] = rocks[i+ 1][:j] + "O" + rocks[i + 1][j+1:]
                        changed_rocks = True
    return rocks

def tilt_west(rocks):
    for i, row in enumerate(rocks):
        while ".O" in row:
            row =  row.replace(".O", "O.")
        rocks[i]= row
    return rocks

def tilt_east(rocks):
    for i, row in enumerate(rocks):
        while "O." in row:
            row =  row.replace("O.", ".O")
        rocks[i]= row
    return rocks

def reflector_dish(filename):
    rocks = []
    sum_of_rocks = 0
    with open(filename) as f:
        for line in f.readlines():
            rocks.append(line.strip())
    seen_rocks = []
    break_loop = False
    for i in range(1000000000):
        rocks = tilt_north(rocks)
        if i == 0:
            for m, line in enumerate(rocks):
                multiple = len(rocks) - m
                sum_of_rocks += sum(1 for k in line if k == "O") * multiple
            print(sum_of_rocks)
        rocks = tilt_west(rocks)
        rocks = tilt_south(rocks)
        rocks = tilt_east(rocks)
        for j, s_rock in enumerate(seen_rocks):
            if rocks == s_rock:
                seen_rocks = seen_rocks[j:]
                break_loop = True
                break
        if break_loop:
            break
        r = rocks.copy()
        seen_rocks.append(r)
    k = (1000000000 - j) % (len(seen_rocks))
    rock = seen_rocks[k - 1]
    sum_of_rocks = 0
    for i, line in enumerate(rock):
        multiple = len(rock) - i 
        sum_of_rocks += sum(1 for k in line if k == "O") * multiple  
    print(sum_of_rocks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Parabolic Reflector Dish",
                description = 'Move rocks'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    reflector_dish(args.filename)
                        
