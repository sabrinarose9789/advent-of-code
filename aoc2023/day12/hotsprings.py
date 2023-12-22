import argparse
from pprint import pprint

def pattern_works(blocks, pattern, seen_patterns):
    p = tuple(pattern)
    if p not in seen_patterns:
        seen_patterns[p] = {}
    if len(pattern) == 0 and "#" not in ''.join(blocks):
        seen_patterns[p][tuple(blocks)] = 1
        return 1, seen_patterns
    elif (len(blocks) == 0 and pattern) or \
        (len(pattern) == 0 and "#" in ''.join(blocks)):
        seen_patterns[p][tuple(blocks)] = 0
        return 0, seen_patterns
    
    tot_patterns = 0
    seen_blocks = seen_patterns[p]
    for b in seen_blocks:
        if b == tuple(blocks):
            tot_patterns += seen_blocks[b]
            return tot_patterns, seen_patterns
    block = blocks[0]
    if pattern[0] == len(block):
        tot, seen_patterns = pattern_works(blocks[1:], 
                                           pattern[1:], 
                                           seen_patterns)
        tot_patterns += tot
    elif pattern[0] < len(block):
        if block[pattern[0]] != "#":
            new_block = block[pattern[0] + 1:]
            new_blocks = [new_block] + blocks[1:]
            tot, seen_patterns = pattern_works(new_blocks, 
                                               pattern[1:], 
                                               seen_patterns)
            tot_patterns += tot
    if len(block) >= 1 and block[0] != '#':
        new_block = block[1:]
        new_blocks = [new_block] + blocks[1:]
        tot, seen_patterns = pattern_works(new_blocks, 
                                           pattern, 
                                           seen_patterns)
        tot_patterns += tot
    elif "#" not in block:
        tot, seen_patterns = pattern_works(blocks[1:], 
                                           pattern, 
                                           seen_patterns)
        tot_patterns += tot
    seen_patterns[p][tuple(blocks)] = tot_patterns
    return tot_patterns, seen_patterns


def find_springs_and_damage(filename):
    xs = 0
    ys = 0
    with open(filename) as f:
        for line in f.readlines():
            springs, damage = line.split()
            f = '\.()'
            pos_groups = [x for x in springs.split(".") if x]
            pattern = [int(x) for x in damage.split(',')]
            x, w = pattern_works(pos_groups, pattern, {})
            xs += x
            springs = '?'.join([springs] * 5)
            pos_groups = [x for x in springs.split(".") if x]
            pattern = pattern * 5 
            y, w = pattern_works(pos_groups, pattern, w)
            ys += y
    print(xs)
    print(ys)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Hot Springs",
                description = 'Fix damaged springs'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    find_springs_and_damage(args.filename)