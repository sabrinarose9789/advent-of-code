# Trees planted carefully in a grid, that the elves planted
# Wondering if good spot for tree house, but wonder if enough
# to keep the tree house hidden
# Need to do: Count the number of trees visible from outside the
# grid when looking directly along a row or column

# INPUT: map/grid of the height of each tree
# Each tree represented by single digit that represents it's height 
#   0 shortest, 9 tallest
# visible only if all other trees between it and edge are shorter than it
import argparse
import numpy as np

def get_sight_range(ar):
    if not ar.any():
        return len(ar)
    return np.argmax(ar) + 1

def tree_visibility(filename):
    grid = []
    with open(filename) as f:
        for line in f.readlines():
            trees = [int(l) for l in line.strip()]
            grid.append(trees)
    grid = np.array(grid)
    x, y = grid.shape
    seen = 0
    best_scene = 0
    for i in range(x):
        for j in range(y):
            val = grid[i, j]

            if (i == grid[:i+1,j].argmax() and val not in grid[:i, j]) or \
            (0 == grid[i:, j].argmax()  and val not in grid[i+1:,j])or \
            (j == grid[i, :j + 1].argmax() and val not in grid[i, :j]) or \
            (0 == grid[i,j:].argmax() and val not in grid[i,j+1:]):
                seen += 1
            
            up_block = np.flip(grid[:i,j] >= val)
            down_block = grid[i + 1:, j] >= val
            left_block = np.flip(grid[i, :j] >= val)
            right_block = grid[i,j + 1:] >= val
    
            up = get_sight_range(up_block)
            down = get_sight_range(down_block)
            left = get_sight_range(left_block)
            right = get_sight_range(right_block)

            score = up * down * left * right
            if score > best_scene:
                best_scene = score
    print(seen)
    print(best_scene)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "TreetopTreeHouse",
                description = 'determine if this tree grid good for a treehouse'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    tree_visibility(args.filename)