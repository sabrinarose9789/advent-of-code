# Signal seems like it coming behind the waterfall
# Cave system inside
# Need to analyze falling material. 

# INPUT: scan a two-D vertical slice of the cave above you
#   mainly air with stucture made of rock
#   traces the path of each solid rock structure and reports the x, y
#   coordinate that form the shape of the path (x dist to right, y down)
# Sand pouring in from point 500
# sand produced one unit at a time , next unit of sand is not produced unitl prev
# comes to rest
# Sand always falls down 1 step if possible
#   if blocked, move diagonally one step down and to the left. If that
#   tile is blocked, move one dow to right.
#   If all three blocked, sand comes to rest
#
# How many units of sand come to rest before sand starts flowing into the abyss
import argparse
import os
import sys
import numpy as np


def sand_drop(cave):
    point = [0, 500]

    while True:
        if point[0] >= 199:
            return cave, True
        if cave[point[0] + 1, point[1]] not in (1, 5,8):
            point[0] += 1
        elif cave[point[0] + 1, point[1] - 1] not in (1, 5,8):
            point[0] += 1
            point[1] -= 1
        elif cave[point[0] + 1, point[1] + 1] not in (1, 5,8):
            point[0] += 1
            point[1] += 1
        elif point == [0, 500]:
            return cave, True
        else:
            cave[point[0], point[1]] = 5
            break
    return cave, False


def fall_sand(filename):
    cave = np.zeros((200, 1000))
    sands = 0
    floor = 0
    with open(filename) as f:
        for line in f.readlines():
            pairs = line.split(' -> ')
            for i, pair in enumerate(pairs[:-1]):
                x1, y1 = pair.split(',')
                x2, y2 = pairs[i+1].split(',')
                if x1.strip() == x2.strip():
                    miny = min(int(y1), int(y2))
                    maxy =  max(int(y1), int(y2))
                    cave[ miny:maxy + 1,int(x1)] = 1
                if y1.strip() == y2.strip():
                    minx = min(int(x1), int(x2))
                    maxx =  max(int(x1), int(x2))
                    cave[ int(y1), minx:maxx + 1] = 1
                if int(y1) > floor:
                    floor = int(y1)
                if int(y2) > floor:
                    floor = int(y2)
    cave[floor + 2,:] = 8
    while True:
        os.system('clear')
        cave, done = sand_drop(cave)
        print(cave[:10,490:510])
        if done:
            print(sands)
            break
        sands += 1
                               
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "RegolithResovoir",
                description = 'Find way through cave'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    fall_sand(args.filename)