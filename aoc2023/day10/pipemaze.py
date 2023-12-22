import argparse
import math
import sys

sys.path.insert(0, '../../helper_scripts/')
import selfqueue
import stack

def create_graph(filename):
    edges = {}
    start = (0,0)
    with open(filename) as f:
        x = [[*x.strip()] for x in f.readlines()]
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                if val != ".":
                    edges[(i, j)] = []
                    if val == 'S':
                        start = (i, j)
                    if val in "|LJ" or (i > 0 and x[i - 1][j] in '|7F' and val == "S"):
                        edges[(i, j)].append((i - 1, j))
                    if val in "|7F" or (i < len(x) - 1 and 
                                        x[i + 1][j] in '|LJ' and val == "S"):
                        edges[(i, j)].append((i + 1, j))
                    if val in '-J7' or (j > 0 and row[j - 1] in '-LF' and val == "S"):
                        edges[(i, j)].append((i, j - 1))
                    if val in '-LF' or (j < len(row) - 1 and 
                                        row[j + 1] in '-J7' and val == "S"):
                        edges[(i, j)].append((i, j + 1))
    return (edges, start,  x)


def create_dot_graph(filename):
    edges = {}
    pos_island = []
    with open(filename) as f:
        x = [[*x.strip()] for x in f.readlines()]
        for i, row in enumerate(x):
            for j, val in enumerate(row):
                if val == ".":
                    edges[(i, j)] = []
                    if i > 0 and x[i-1][j] == '.':
                        edges[(i, j)].append((i - 1, j))
                    if i < len(x) - 1 and x[i+1][j] == '.':
                        edges[(i, j)].append((i + 1, j))
                    if j > 0 and row[j-1] == '.':
                        edges[(i, j)].append((i, j - 1))
                    if j < len(row) - 1 and row[j+1] == '.':
                        edges[(i, j)].append((i, j + 1))
                    if i > 0 and i < len(x) - 1 and j > 0 and j < len(row) - 1:
                        pos_island.append((i,j))
    return (edges, len(x) - 1, len(row) - 1)


def solve_maze(edges, start):
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


def find_islands(edges, i, j):
    pos_edges = set(edges.keys())
    total_islands = []
    while True:
        bad_island = False
        start = pos_edges.pop()
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
                    if edge[0] in (0, i) or edge[1] in (0,j):
                        bad_island = True
                    dist[edge] = dist[next] + 1
                    path[edge] = next
                    queue.enqueue(edge)
                    seen.add(edge)
        pos_edges = pos_edges - seen 
        if not bad_island:
            total_islands.append(seen.union({start}))
        if not pos_edges:
            return total_islands 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Pipe Maze",
                description = 'Avoid the animal'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    graph, start, full_graph = create_graph(args.filename)
    dot_graph, max_i, max_j =  create_dot_graph(args.filename)
    dist, path = solve_maze(graph, start)
    total_islands = find_islands(dot_graph, max_i, max_j)
    print(max(x for x in dist.values() if x != math.inf))
    stack = stack.Stack()
    tot = 0
    visited = set()
    directions = {}
    stack.push(start)
    while True:
        if stack.len() == 0:
            break
        p = stack.pull()
        if p in visited:
            continue
        visited.add(p)
        if full_graph[p[0]][p[1]] in "|7F":
            directions[p] = "S"
        for a in graph[p]:
            if a not in visited:
                stack.push(a)
    for i, row in enumerate(full_graph):
        in_loop = False
        sub_tot = 0
        line = ''
        for j, col in enumerate(row):
            if (i, j) in directions:
                in_loop = not in_loop
                line += directions[(i, j)]
            elif (i,j) not in path and in_loop:
                line += '.'
                tot += 1
                sub_tot += 1
            elif (i, j) in path:
                line += col
            else:
                line += ' '
        print(line, sub_tot)
    print(tot)