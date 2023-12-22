import argparse
import queue
import math
import numpy as np

def find_least_heated_path(crucible, source, min_consec, max_consec):
    dist = {}
    prev = {}
    dist[source] = 0 
    prev[source] = None
    priority_queue = queue.PriorityQueue()
    seen = set()
    priority_queue.put((0, (source, "S")))
    priority_queue.put((0, (source, "R")))
    max_x = len(crucible)
    max_y = len(crucible[0])
    for i in range(max_x):
        for j in range(max_y):
            if (i,j) != source:
                dist[(i, j)] = math.inf
    while not priority_queue.empty():
        x = priority_queue.get()
        weight, v = x
        if v in seen:
            continue
        seen.add(v)
        point, dir = v
        if weight < dist[point]:
            dist[point] = weight
        x, y = point
        dist_1 = weight
        dist_2 = weight
        if dir in ("L", "R"):
            # Have to go north or south 
            for i in range(1, max_consec + 1):
                north_x = x - i 
                if north_x >= 0:
                    dist_1 += crucible[north_x][y]
                    if i >= min_consec:
                        priority_queue.put((dist_1, ((north_x, y), "N")))
                south_x = x + i 
                if south_x < max_x:
                    dist_2 += crucible[south_x][y]
                    if i >= min_consec:
                        priority_queue.put((dist_2, ((south_x, y), "S")))
        else:
            # Have to go left or right
            for i in range(1, max_consec + 1):
                left_y = y - i
                if left_y >= 0:
                    dist_1 += crucible[x][left_y]
                    if i >= min_consec:
                        priority_queue.put((dist_1, ((x, left_y), "L")))
                right_y = y + i 
                if right_y < max_y:
                    dist_2 += crucible[x][right_y]
                    if i >= min_consec:
                        priority_queue.put((dist_2, ((x, right_y), "R")))
    return dist, prev         


def create_graph(filename):
    crucible = []
    with open(filename) as f:
        for line in f.readlines():
            new_line = [int(l) for l in line.strip()]
            crucible.append(new_line)
    dist, prev = find_least_heated_path(crucible, (0,0), 1, 3)
    end = (len(crucible) - 1, len(crucible[0]) - 1)
    print(dist[end])
    dist, prev = find_least_heated_path(crucible, (0,0), 4, 10)
    print(dist[end])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Lens Library",
                description = 'Hashing to read a manual'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    create_graph(args.filename)
                        