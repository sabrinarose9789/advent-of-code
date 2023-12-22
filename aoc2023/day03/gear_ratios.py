import argparse 

def translate_schematic(filename):
    schematic = [] 
    with open(filename) as f:
        for line in f.readlines():
            schematic.append(line.strip())
    nums = []
    end = len(schematic)
    gears = {}
    for i, line in enumerate(schematic):
        num = ''
        keep = False
        add_gear = False
        for l, letter in enumerate(line):
            if letter.isnumeric():
                num += letter
                if not keep: 
                    adjacent_n = range(max(0, i - 1), min(end, i + 2))
                    adjacent_m = range(max(0, l - 1), min(len(line), l + 2))
                    for k in adjacent_n:
                        for w in adjacent_m:
                            val = schematic[k][w]
                            if not val.isnumeric() and not val == ".":
                                keep = True
                                if val == "*":
                                    add_gear = (k, w)
                                break
            else:
                if num and keep:
                    nums.append(int(num))
                    keep = False
                    if add_gear:
                        if add_gear not in gears:
                            gears[add_gear] = []
                        gears[add_gear].append(int(num))
                        add_gear = False
                num = ''
        if num and keep:
            nums.append(int(num))
            if add_gear:
                if add_gear not in gears:
                    gears[add_gear] = []
                gears[add_gear].append(int(num))
    print(sum(nums))
    print(sum(k[0] * k[1] for k in gears.values() if len(k) == 2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Gear Ratios",
                description = 'Examine engine schematics'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    translate_schematic(args.filename)

