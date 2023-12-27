import argparse
import pprint
import copy
import numpy as np

# A line like 2,2,2~2,2,2 means that both ends of the brick are at 
# the same coordinate - in other words, that the brick is a single cube.

# Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks 
# that are two cubes in volume, both oriented horizontally. The first brick extends in the x direction, while the second brick extends in the y direction.

# A line like 0,0,1~0,0,10 represents a ten-cube brick which is
#  oriented vertically. One end of the brick is the cube located at 0,0,1, 
#  while the other end of the brick is located directly above it at 0,0,10.

# The ground is at z=0 and is perfectly flat; the lowest z value a
#  brick can have is therefore 1. So, 5,5,1~5,6,1 and 0,2,1~0,2,5 are 
#  both resting on the ground, but 3,3,2~3,3,3 was above the ground 
#  at the time of the snapshot.
def sortvalue(e):
    return e[0]

def falling_bricks(filename):
    bricks = []
    z_floors = {}
    with open(filename) as f:
        for b, line in enumerate(f.readlines()):
            start, end = line.strip().split("~")
            start = [int(s) for s in start.split(",")]
            end = [int(e) for e in end.split(",")]
            points = []
            for x in range(start[0], end[0] + 1):
                for y in range(start[1], end[1] + 1):
                    for z in range(start[2], end[2] + 1):
                        points.append((x, y, z))
            bricks.append((start[-1], points))
    bricks.sort(key=sortvalue)
    
    done_moving = {}
    for i, brick in enumerate(bricks):
        cubes = brick[1]
        while True:
            new_cubes = []
            stoppers = []
            for b in cubes:
                nb = (b[0], b[1], b[2] - 1)
                if nb in done_moving:
                    stoppers.append(done_moving[nb][0])
                new_cubes.append(nb)  
            if new_cubes[0][2] == 0 or stoppers:
                if stoppers:
                    new_cubes = cubes
                for nc in new_cubes:
                    done_moving[nc] = (i, stoppers)
                break 
            cubes = new_cubes
    cube_to_support = {}
    support_to_cube = {}
    for cube, support in done_moving.values():
        if cube not in cube_to_support:
            cube_to_support[cube] = set()
        if cube not in support_to_cube:
            support_to_cube[cube] = set()
        for s in support:
            if s not in support_to_cube:
                support_to_cube[s] = set()
            cube_to_support[cube].add(s)
            support_to_cube[s].add(cube)
    tot_to_remove = 0
    fallen = 0
    tried = set()
    for c,support in support_to_cube.items():
        remove = True
        for s in support:
            if len(cube_to_support[s]) == 1:
                remove = False 
        if remove:
            tot_to_remove += 1 
        else:
            tot_removed = cascade_fall({c}, support_to_cube, 
                                          cube_to_support)
            fallen += len(tot_removed) - 1
    
    print(tot_to_remove)
    print(fallen)


def cascade_fall(blocks, support_to_cube, cube_to_support):
    sc = copy.deepcopy(support_to_cube)
    cs = copy.deepcopy(cube_to_support)
    block = blocks
    while True:
        to_remove = set()
        for b in block:
            for s in sc[b]:
                if s not in blocks:
                    if b in cs[s]:
                        cs[s].remove(b)
                        if len(cs[s]) == 0:
                            to_remove.add(s)
                            
        blocks.update(to_remove)
        if not to_remove:
            d = [(v, c) for v, c in cs.items() if c]
            return blocks
        block = to_remove
    # pprint.pprint(done_moving)
        
        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
    