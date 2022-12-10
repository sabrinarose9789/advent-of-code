# Rope bridge creaks as you walk along
# Can it support your weight
# Model rope physics - where not to step
# rope with a knot at each end - mark head and tail of the rope
#   if head moves far enough from tail, tail pulled towards head
# model positions of knots on a 2-D grid
# INPUT: series of motions the head makes (DIR, AMOUNT)
# RULES:
#   Head and Tail must always be touching (diagonally adjacent and overlapping count)
#   If HEAD ever two steps directly up, down, left, or right from Tail, Tail must
#   also move one step in that direction
#   IF Head and Tail aren't touching and aren't in same row/column, Tail moves one
#   step diagonally to keep up
# GOAL:
#   Figure out where the tail goes as the head follows a series of motions
#   Count up all of the positions the tail visited at least once.


# Rope now consists of ten knots H 1, 2, .., 9
import argparse

def dist_from_head(head, tail):
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return False
    return True

def move_head(value, dir):
    x, y= value
    if dir == 'R':
        x += 1
    elif dir == "L":
        x -= 1
    elif dir == 'U':
        y -= 1
    elif dir == 'D':
        y += 1
    return (x, y)

def move_tail(tail, head):
    h_x, h_y = head
    t_x, t_y = tail
    if h_x - t_x > 1:
        t_x += 1
        if h_y - t_y >= 1:
            t_y += 1
        elif t_y - h_y >= 1:
            t_y -= 1
    elif t_x - h_x > 1:
        t_x -= 1
        if h_y - t_y >= 1:
            t_y += 1
        elif t_y - h_y >= 1:
            t_y -= 1
    elif t_y - h_y > 1:
        t_y -= 1
        if h_x - t_x >= 1:
            t_x += 1
        elif t_x - h_x >= 1:
            t_x -= 1
    elif h_y - t_y > 1:
        t_y += 1
        if h_x - t_x >= 1: 
            t_x += 1
        elif t_x - h_x >= 1:
            t_x -= 1
    return (t_x, t_y)
    

def tail_follow_head(filename, knots):
    rope_knots = [(0,0)] * knots
    seen = set()
    seen.add(rope_knots[-1])
    with open(filename) as f:
        for line in f.readlines():
            dir, amt = line.strip().split()
            amt = int(amt)
            for _ in range(amt):
                rope_knots[0] = move_head(rope_knots[0], dir)
                for i in range(0, knots-1):
                    if not (abs(rope_knots[i][0] - rope_knots[i+1][0]) <= 1 \
                        and abs(rope_knots[i][1] - rope_knots[i+1][1]) <= 1):
                        rope_knots[i+1] = move_tail(rope_knots[i+ 1],
                                                    rope_knots[i])
                seen.add(rope_knots[-1])
    print(len(seen))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "RopeBridge",
                description = 'Is this rope bridge stable'
    )
    parser.add_argument('filename')
    parser.add_argument('knots')
    args = parser.parse_args()
    tail_follow_head(args.filename, int(args.knots))