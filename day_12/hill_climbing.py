# river too low to get disgnal
# INPUT: heightmap shows the local area from above broken into a grid;
#        the elevation of each square of the grid is given by the single lowercase
#         letter (a is lowest, z is highest)
# S is current position with elevation a, and the location with best signal has is E
# want to reach E in lowest amount of steps as possible
# during each step, you can move exactly one square up, down, left or right
# destination square can be at most one higher than current square (can be any lower)

import argparse
import math
import sys

sys.path.insert(0, '../helper_scripts/')
import selfqueue

def get_priority(chr):
    if chr == 'E':
        return 25
    if chr == 'S':
        return 0
    return ord(chr) - 97

def create_graph(filename):
    edges = {}
    start = (0,0)
    end = (0,0)
    starts = set()
    with open(filename) as f:
        x = [[*x.strip()] for x in f.readlines()]
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                edges[(i, j)] = []
                if val == 'S':
                    start = (i, j)
                if val == 'E':
                    end = (i, j)
                if val == 'a':
                    starts.add((i,j))
                val = get_priority(val)
                if i > 0:
                    left_val = get_priority(x[i - 1][j])
                    if left_val - val <= 1:
                        edges[(i, j)].append((i - 1, j))
                if i < len(x) - 1:
                    right_val = get_priority(x[i + 1][j])
                    if right_val - val <= 1:
                        edges[(i, j)].append((i + 1, j))
                if j > 0:
                    upper_val = get_priority(x[i][j - 1])
                    if upper_val - val <= 1:
                        edges[(i, j)].append((i, j - 1))
                if j < len(row) - 1:
                    below_val = get_priority(x[i][j + 1])
                    if below_val - val <= 1:
                        edges[(i, j)].append((i, j + 1))
    return (edges, start, end, starts)

def hillclimbing(edges, start):
    dist = {}
    dist[start] = 0
    path = {}
    path[start] = None
    for v in edges.keys():
        if v != start:
            dist[v] = math.inf
    queue = selfqueue.Queue()
    queue.enqueue(start)
    seen = set()
    while queue.notempty():
        next = queue.dequeue()
        for edge in edges[next]:
            if edge not in seen:
                dist[edge] = dist[next] + 1
                path[edge] = next
                queue.enqueue(edge)
                seen.add(edge)

    return dist, path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "HillClimbing",
                description = 'Find way up the hill'
    )
    parser.add_argument('filename')
    parser.add_argument('-m', action='store_true')
    args = parser.parse_args()
    edges, start, end, starts = create_graph(args.filename)
    steps, path = hillclimbing(edges, start)
    if args.m:
        paths = [steps[end],]
        for s in starts:
            a_steps, path = hillclimbing(edges,s)
            if a_steps[end] < math.inf:
                paths.append(a_steps[end])
        print(min(paths))
    else: 
        print(steps[end])
