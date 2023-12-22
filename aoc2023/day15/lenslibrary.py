import argparse 

def determine_hash(string):
    cur_value = 0
    for letter in string:
        cur_value += ord(letter)
        cur_value = (cur_value * 17) % 256
    return cur_value


def start_production(filename):
    sum_value = 0 
    hashmap = {}
    f = open(filename, "r")
    string = f.read().strip().split(",")
    for s in string:
        x = s.split("=")
        if len(x) == 2:
            box = determine_hash(x[0])
            if box not in hashmap:
                hashmap[box] = []
            added = False
            for i, val in enumerate(hashmap[box]):
                if val[0] == x[0]:
                    hashmap[box][i] = (x[0], int(x[1]))
                    added = True
                    break
            if not added:
                hashmap[box].append((x[0], int(x[1])))
        else:
            x = s.split("-")[0]
            box = determine_hash(x)
            remove = False
            if box in hashmap:
                for val in hashmap[box]:
                    if val[0] == x:
                        remove = True 
                        break
            if remove:
                hashmap[box].remove(val)              
        sum_value += determine_hash(s)
    print(sum_value)
    focus_power = 0
    for box_num, labels in hashmap.items():
        box_multiple = box_num + 1
        for i, val in enumerate(labels, 1):
            focal_length = val[1]
            focus_power += box_multiple * i * focal_length 
    print(focus_power)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Lens Library",
                description = 'Hashing to read a manual'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    start_production(args.filename)
                        


