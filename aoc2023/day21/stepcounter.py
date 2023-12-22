
import argparse
import queue

def step_counter(filename):
    with open(filename) as f:
        gardenplot = [l.strip() for l in f.readlines()]
    moveable_spaces = {}
    infinite_graph = {}
    most_steps = {}
    start = (0, 0)
    for i, row in enumerate(gardenplot):
        for j, value in enumerate(row):
            if value == "#":
                continue
            moveable_spaces[(i,j)] = []
            infinite_graph[(i,j)] = []
            most_steps[(i,j)] = 0
            above = (i - 1, j)
            left = (i, j - 1)
            down = ( i + 1, j)
            right = (i, j + 1)
            for next_term in (above, left,down, right):
                x, y = next_term
                cur_graph = (0,0)
                if x >= 0 and x < len(gardenplot) and y >= 0 and y < len(row):
                    if gardenplot[x][y] != '#':
                        moveable_spaces[(i,j)].append(next_term)
                if x == len(gardenplot):
                    x = 0 
                    cur_graph = (1, 0)
                if y == len(row):
                    y = 0
                    cur_graph = (0, 1)
                if x < 0:
                    x = len(gardenplot) - 1 
                    cur_graph = (-1, 0)
                if y < 0:
                    y = len(gardenplot) - 1
                    cur_graph = (0, -1)
                if gardenplot[x][y] != "#":
                    infinite_graph[(i,j)].append(((x,y), cur_graph))
            if value == "S":
                start = (i, j)
    v, _  = bfs_steps_infinite(start, infinite_graph, 65)
    print(sum(len(k) for k in v.values()))
    _, v1 = bfs_steps_infinite(start, infinite_graph, 328)
    a = 0 
    bs = 0
    ts = 0
    for i in range(-2, 3):
        for j in range(-2, 3):
            ks = 0
            for k in v1.values():
                ks += sum(w ==(i,j) for w in k)
            if (i, j) == (0,0):
                os = ks
            elif (i, j ) == (0,1):
                es = ks 
            elif i == 0 and j in (-2, 2) or j == 0 and i in (-2, 2):
                ts += ks 
            elif i in (-1, 1) and j in (-2, 2):
                bs += ks 
            elif i in (-1, 1) and j in (-1, 1):
                a += ks
    n = 26501365 // len(gardenplot)
    sol = find_nth_65_step(n, os, es, a, bs, ts)
    print(sol)


    
def find_nth_65_step(x, os, es, a, bs,ts):
    return os * ((x-1) ** 2) + es * (x ** 2) + a * (x- 1) + bs * x + ts


def bfs_steps(start, graph, max_steps):
    next_steps = queue.Queue()
    next_steps.put((start, 0))
    counter = 0
    visited = {}
    visited_2 = {}
    while True:
        if next_steps.empty():
            break 
        n, steps = next_steps.get() 
        if steps > counter:
            counter = steps
        if n in visited or n in visited_2:
            continue
        if steps < max_steps:
            n_steps = steps + 1
            for next in graph[n]:
                    if next not in visited and next not in visited_2:
                        next_steps.put((next, n_steps))
        if max_steps % 2 == 0 and steps % 2 == 0 and n not in visited:
            visited.append(n)
        elif steps % 2 == 1 and n not in visited_2:
            visited_2.append(n)    
    return len(visited)


def bfs_steps_infinite(start, graph, max_steps):
    next_steps = queue.Queue()
    next_steps.put((start, 0, (0,0)))
    visited = {}
    visited_2 = {}
    while True:
        if next_steps.empty():
            break 
        n, steps, g = next_steps.get()
        if (n in visited and g in visited[n]) or \
            (n in visited_2 and g in visited_2[n]):
            continue
        n_steps = steps + 1
        for t, cg in graph[n]:
                ng = (g[0] + cg[0], g[1] + cg[1])
                if (t not in visited or ng not in visited[t]) and \
                    (t not in visited_2 or ng not in visited_2[t]):
                    next_steps.put((t, n_steps, ng))
        if  steps % 2 == 0:
            if n not in visited:
                visited[n] = [g]
            elif g not in visited[n]:
                visited[n].append(g)
        elif steps % 2 == 1:
            if n not in visited_2:
                visited_2[n] = [g]
            elif g not in visited_2[n]:
                visited_2[n].append(g)
        if steps == max_steps:
            print(steps, sum(len(k) for k in visited_2.values()) )
            break
    return (visited, visited_2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Step Counter",
                description = 'Reach exactly x steps'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    step_counter(args.filename)
                        
