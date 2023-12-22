import math
import argparse

def count_wins(t, d):
    zero_1 = ((t * -1) - (t ** 2 - 4 * d) ** .5) / (2 * -1)
    zero_2 = ((t * -1) + (t ** 2 - 4 * d) ** .5) / (2 * -1)
    return (math.ceil(min(zero_1, zero_2)), math.floor(max(zero_1, zero_2)))


def wait_for_it(filename):
    wins = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            nums = line.split(":")[1].strip()
            if i == 0:
                time = int(''.join(x for x in nums.split()))
                times = [int(x) for x in nums.split()]
            if i == 1:
                distance = int(''.join(x for x in nums.split()))
                dist = [int(x) for x in nums.split()]
        for i, t in enumerate(times):
            min_win, max_win = count_wins(t, dist[i] + 1)
            wins.append(max_win - min_win + 1)
    print(math.prod(wins))
    min_win, max_win = count_wins(time, distance + 1)
    print(max_win - min_win + 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Wait For It",
                description = 'Who wins the boat race'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    wait_for_it(args.filename)
