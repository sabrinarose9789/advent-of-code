import argparse
import numpy as np

def math_area(dir, amount, cur):
    if dir in ("1", "D"):
        new = [cur[0] +  amount, cur[1]]
    elif dir in ("3", "U"):
        new = [cur[0] - amount, cur[1]]
    elif dir in ("2", "L"):
        new = [cur[0], cur[1] - amount]
    elif dir in ("0", "R"):
        new = [cur[0], cur[1] + amount]
    return (new, cur[1] * new[0] - cur[0] * new[1])


def dig_trench(filename):
    color_trench = 0 
    trench = 0
    cur = [0, 0]
    c = [0,0]

    with open(filename) as f:
        for line in f.readlines():
            dir, amount, color = line.split()
            color = color.strip("()")
            col_amount = int(color[1:-1], 16)
            amount = int(amount)
            col_dir = color[-1] 
            cur, t = math_area(dir, amount, cur)
            c, ct = math_area(col_dir, col_amount, c) 
            trench += t / 2 + amount / 2
            color_trench += ct / 2 + col_amount / 2
    print(trench + 1)
    print(color_trench + 1)


# NOT USED
def flood_fill(lagoon):
    tot = 0
    for i, row in enumerate(lagoon):
        in_loop = False
        next = ''
        sub_tot = 0
        for j, col in enumerate(row):
            if col in "^v" and (not next or next == col):
                in_loop = not in_loop 
                if col == "v":
                    next = "^"
                else:
                    next = "v"
            if col in "^v<>" or in_loop:
                sub_tot += 1
        tot += sub_tot
    print(tot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Lavaduct Lagoon",
                description = 'Dig out lavaduct'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    dig_trench(args.filename)
                        