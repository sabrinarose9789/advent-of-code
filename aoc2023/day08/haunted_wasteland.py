import argparse
import numpy as np

def navigate_network(filename):
    network = {}
    starting_nodes = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if i == 0:
                order = line
            elif line:
                key, vals = line.split(" = ")
                left, right = vals.strip("()").split(", ")
                network[key] = {"L": left, "R": right}
                if key[-1] == "A":
                    starting_nodes.append(key)
    print("ANSWER 1: ")
    print(find_steps("AAA", order, network, "ZZZ"))
    print("ANSWER 2: ")
    other_steps = [] 
    for s in starting_nodes:
        steps = find_steps(s, order, network, "Z")
        other_steps.append(steps)
    print(np.lcm.reduce(other_steps))


def find_steps(place, order, network, end):
    steps = 0
    path = order
    while True:
        steps += 1
        turn = path[0]
        path = path[1:]
        if len(path) == 0:
            path = order
        place = network[place][turn]
        if (place == end) or (len(end) == 1 and place[-1] == end):
            return steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Haunted Wasteland",
                description = 'Navigate scary place'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    navigate_network(args.filename)

