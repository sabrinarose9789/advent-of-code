import argparse
import math
import numpy as np

def cosmic_expansion(filename, exp):
    lines = []
    ex_rows = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            x = ['' if l == '.' else l for l in line.strip() ]
            lines.append(x)
            if all(space == '' for space in x):
                ex_rows.append(i)
    space = np.array(lines)

    i = 0
    ex_cols = []
    while i < space.shape[1]:
        if np.all(space[:, i] == ''):
            ex_cols.append(i)
        i += 1
    galaxies = np.where(space == "#")
    distance = 0
    for i, x in enumerate(galaxies[0]):
        y = galaxies[1][i]
        for j, x2 in enumerate(galaxies[0][i + 1:], i + 1):
            closer_x = min(x, x2)
            further_x = max(x, x2)
            new_x = further_x
            y2 = galaxies[1][j]
            closer_y = min(y, y2)
            further_y = max(y, y2)
            new_y = further_y
            for r in ex_rows:
                if r > closer_x and r < further_x:
                    new_x += exp - 1
            for c in ex_cols:
                if c > closer_y and c < further_y:
                    new_y += exp - 1
            dist = abs(new_y - closer_y) + abs(new_x - closer_x)
            distance += dist

    print(distance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Cosmic Expansion",
                description = 'Shortest distance to the cosmos'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    cosmic_expansion(args.filename, 2)
    cosmic_expansion(args.filename, 1000000)