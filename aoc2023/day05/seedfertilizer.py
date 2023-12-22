import argparse


def parse_input(filename):
    seeds = []
    mappings = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if i == 0:
                seeds = [int(x) for x in line[6:].split()]
            elif "map" in line:
                mapping = []
            elif line.strip() == '':
                if i > 1:
                    mappings.append(mapping)
                    mapping = []
            else:
                dest, source, length = line.split()
                diff = int(dest) - int(source)
                mapping.append((range(int(source), int(source) + int(length)),
                           diff, (int(source), int(source) + int(length))))
    mappings.append(mapping)
    return (seeds, mappings )


def fertilize_seed(filename):
    seeds, mappings = parse_input(filename)
    min_seed = -1 
    for seed in seeds:
        for i, mapping in enumerate(mappings):
            for source_range, diff, _ in mapping:
                if seed in source_range:
                    seed = seed + diff 
                    break
        if min_seed < 0 or seed < min_seed:
            min_seed = seed 
    print(min_seed)
    min_seed = -1
    ugh = []
    for i in range(0, len(seeds), 2):
        ranges = [(seeds[i], seeds[i] + seeds[i + 1])]
        for l, mapping in enumerate(mappings):
            new_ranges = []
            for rng in ranges:
                sub_ranges = [rng]
                for r in sub_ranges:
                    max_r = r[1]
                    min_r = r[0]
                    for _, diff, min_max in mapping:
                        min_s = min_max[0]
                        max_s = min_max[1]
                        if max_r >= min_s and min_r <= max_s:
                            new_range = (max(min_r, min_s) + diff,
                                            min(max_r, max_s) + diff)
                            new_ranges.append(new_range)
                            if max_r <= max_s and min_r >= min_s:
                                r = None
                                break
                            elif max_r > max_s and min_r < min_s:
                                max_r = min_s
                                sub_ranges.append((max_s + 1, max_r))
                            elif max_r > min_s and not (min_r > min_s):
                                max_r = min_s
                            elif min_r < max_s and not (max_r < max_s):
                                min_r = max_s + 1
                    if r:
                        new_ranges.append(r)
            ranges = new_ranges
        ugh.extend(ranges)
    for r in ugh:
        if min_seed < 0 or min(r) < min_seed:
            min_seed = min(r)
    print(min_seed)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "SEED FERTILIZER",
                description = 'Fertilize the seeds using mappings'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    fertilize_seed(args.filename)
