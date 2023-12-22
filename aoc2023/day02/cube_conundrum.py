
import argparse
import re

def possible_game(sets, r=12, g=13, b=14):
    colors = {"red": (r, 0), 
              "green": (g, 0), 
              "blue": (b, 0)}
    poss_game = True
    rounds = sets.split("; ")
    for round in rounds:
        for color in colors.keys():
            num = re.findall("(\d+) " + color, round)
            if num:
                num = int(num[0]) 
                if num > colors[color][0]:
                    poss_game = False 
                if num > colors[color][1]:
                    colors[color] = (r, num)
    power = 1 
    for k in colors.values():
        power *= k[1]
    return (poss_game, power)


def check_games(filename):
    total = 0
    power_sum = 0
    with open(filename) as f:
        for line in f.readlines():
            game_num = re.findall("Game (\d+):", line)[0]
            poss_game, power = possible_game(line)
            if line.strip() and poss_game:
                total += int(game_num)
            power_sum += power
    print(total)
    print(power_sum)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Cube Conundrum",
                description = 'Check which games are possible with number of cubes'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    check_games(args.filename)