import argparse
import numpy as np

def find_pattern(block):
    first_i = None
    second_i = None
    rows = len(block)
    for i in range(1, rows + 1):
        i_to_end = rows - i 
        t = min(i, i_to_end)
        start = block[i - t:i]
        end = np.flip(block[i:i + t], 0)
        equality = start == end
        if np.array_equal(start, end) and i != rows and not first_i:
            first_i = i
        elif equality.sum() >= start.size - 1:
            if not second_i and i != rows:
                second_i = i
    return (first_i, second_i)
        


def create_blocks(filename):
    lines = []
    total_lines = 0
    um = 0
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if line.strip():
                x = [l for l in line.strip()]
                lines.append(x)
            elif lines:
                block = np.array(lines)
                tot_a, tot_b = find_pattern(block.T)
                tot_A, tot_B = find_pattern(block)
                if not tot_a:
                    total_lines += tot_A * 100 
                elif not tot_A:
                    total_lines += tot_a 
                if not tot_b:
                    um += tot_B * 100 
                elif not tot_B:
                    um += tot_b
                lines = []
    print(total_lines)
    print(um)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Point of Incidence",
                description = 'Look for reflections'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    create_blocks(args.filename)