import random
import copy

def snowverload(filename):
    vertices = {}
    count = {}
    with open(filename) as f:
        for line in f.readlines():
            main_c, rest = line.split(": ")
            if main_c not in vertices:
                vertices[main_c] = []
            for r in rest.split():
                vertices[main_c].append(r)
                if r not in vertices:
                    vertices[r] = []
                vertices[r].append(main_c)
                count[r] = 1
            count[main_c] = 1
    edges = run_karger(100, vertices)
    prod = 1
    for e in edges.values():
        prod *= (len(e) + 1)
    print(prod)
    
    
def choose_random_key(graph):
    v1 = random.choice(list(graph.keys()))
    v2 = random.choice(list(graph[v1]))
    return v1, v2

def karger(graph):
    length = []
    groups = {}
    while len(graph) > 2:
        v1, v2 = choose_random_key(graph)
        # Maintain new vertex groups
        if v1 in groups:
            if v2 in groups:
                groups[v1].extend(groups[v2])
                del groups[v2]
            groups[v1].append(v2)
        else:
            added = False
            for v, keys in groups.items():
                if v1 in keys:
                    if v2 in groups:
                        groups[v].extend(groups[v2])
                        del groups[v2]
                    groups[v].append(v2)
                    added = True 
                    break 
            if not added:
                groups[v1] = groups.get(v2, []) + [v2]
                if v2 in groups:
                    del groups[v2]
        # Move v2 edges to v1 and update other edges accordingly
        graph[v1].extend(graph[v2])
        for x in graph[v2]:
            graph[x].remove(v2)
            graph[x].append(v1)
        while v1 in graph[v1]:
            graph[v1].remove(v1)
        del graph[v2]
    for key in graph.keys():
        length.append(len(graph[key]))
    return (length[0], groups)

def run_karger(n, graph):
    count = len(graph)
    new_graph = None
    for _ in range(n):
        data = copy.deepcopy(graph)
        min_cut, min_graph = karger(data)
        if min_cut < count:
            count = min_cut
            new_graph = min_graph
    return new_graph

