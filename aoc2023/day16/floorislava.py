import argparse
import sys
import numpy as np

sys.path.insert(0, '../../helper_scripts/')
import selfqueue


SLASH_DIR = {"\\":
             {"S": "E",
             "E": "S",
             "W": "N",
             "N": "W"},
             "/": 
             {"E": "N",
              "S": "W",
              "W": "S",
              "N": "E"}
}



class Beam:
    def __init__(self, start, dir, map, seen=None):
        if not seen:
            self.seen_spaces = set()
        else:
            self.seen_spaces = seen
        self.map = map
        self.to_travel = selfqueue.Queue()
        self.to_travel.enqueue((start,dir))

    def travel_beam(self):
        while self.to_travel:
            next = self.to_travel.dequeue()
            if not next:
                break
            if next in self.seen_spaces:
                continue
            pos, dir = next
            self.seen_spaces.add((pos, dir))
            pos_x, pos_y = pos
            if dir == "N":
                pos_x-= 1 
            if dir == "W":
                pos_y -= 1 
            if dir == "E":
                pos_y += 1 
            if dir == "S":
                pos_x += 1 
            new_pos = (pos_x, pos_y)
            if -1 in new_pos or self.map.shape[0] == pos_x or \
                self.map.shape[1] == pos_y:
                continue
            next_space = self.map[pos_x][pos_y]
            if dir in ("W", "E") and next_space == "|":     
                if (new_pos, "N") not in self.seen_spaces:
                    self.to_travel.enqueue((new_pos, "N"))
                if (new_pos, "S") not in self.seen_spaces:
                    self.to_travel.enqueue((new_pos, "S"))
            elif dir in ("S", "N") and next_space == "-":
                if (new_pos, "W") not in self.seen_spaces:
                    self.to_travel.enqueue((new_pos, "W"))
                if (new_pos, "E") not in self.seen_spaces:
                    self.to_travel.enqueue((new_pos, "E"))
            elif next_space in SLASH_DIR:
                new_dir = SLASH_DIR[next_space][dir]
                if (new_pos, new_dir) not in self.seen_spaces:
                    self.to_travel.enqueue((new_pos, new_dir))
            else:
                if (new_pos, dir) not in self.seen_spaces:
                    self.to_travel.enqueue((new_pos, dir))
        return self.seen_spaces
    

def energize_tiles(filename):
    contraption = []
    with open(filename) as f:
        for line in f.readlines():
            new_line = [l for l in line.strip()]
            contraption.append(new_line)
    contraption = np.array(contraption)
    beam = Beam((-0, -1), "E", contraption)
    seen_paths = beam.travel_beam()
    seen = set()
    for pos, dir in seen_paths:
        if -1 not in pos:
            seen.add(pos)
    print(len(seen))
    max_seen = 0 
    for i in range(contraption.shape[0]):
        for dir in ("E", "W"):
            point = (i, -1)
            if dir == "W":
                point = (i, contraption.shape[1])
            beam = Beam(point, dir, contraption)
            seen_paths = beam.travel_beam()
            seen = set()
            for pos, dir in seen_paths:
                if -1 not in pos:
                    seen.add(pos)
            if len(seen) > max_seen:
                max_seen = len(seen)
    for i in range(contraption.shape[1]):
        for dir in ("N", "S"):
            point = (-1, i)
            if dir == "N":
                point = (contraption.shape[0] - 1, i)
            beam = Beam(point, dir, contraption)
            seen_paths = beam.travel_beam()
            seen = set()
            for pos, dir in seen_paths:
                if -1 not in pos:
                    seen.add(pos)
            if len(seen) > max_seen:
                max_seen = len(seen)
    print(max_seen)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "The Floor Will be Lava",
                description = 'Feel like this is a warning'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    energize_tiles(args.filename)
                        
