
import argparse

def parse_input(line):
    nums = line.strip().split(": ")[1].split(" | ")
    winning_nums = [int(x) for x in nums[0].split()]
    my_nums = [int(x) for x in nums[1].split()]

    return (winning_nums, my_nums)


def scratch(filename):
    points = 0
    copies_won = {}
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            card = i + 1
            winning_nums, my_nums = parse_input(line)
            copies_won[card] = copies_won.get(card, 0) + 1
            my_win_nums = len(set(winning_nums) & set(my_nums))
            if my_win_nums > 0:
                points += 2 ** (my_win_nums - 1)
                for k in range(1, my_win_nums + 1):
                    copies_won[card + k] = copies_won.get(card + k, 0) + \
                        copies_won[card]
    print(points)
    print(sum(copies_won.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Scratch card",
                description = 'Find winning scratchcards'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    scratch(args.filename)
            