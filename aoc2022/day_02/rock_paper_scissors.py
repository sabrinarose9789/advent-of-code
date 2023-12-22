# rock paper scissors to decide whose tent is closest to snack storage
# Input: encrypted strategy guide where:
#       first column: Opponent's play (A == "rock", B == "paper", C == "scissors")
#       second column: ? You think what you should play in  response (X == "rock", Y == "paper", Z == "scissors")
# Winner is player with the highest score
# total score = sum for score each round
# score = shape selected (1 for R, 2 for P, 3 for S) + outcome (0 for lost, 3 for draw, 6 for win)
import argparse


SHAPE_DICT = {"A": "R", "B": "P", "C": "S",
              "X": {"R":"S", "P":"R", "S":"P"}, 
              "Y": {"R":"R", "P":"P", "S":"S"},
              "Z": {"R":"P", "P":"S", "S":"R"}
}


SHAPE_SCORE = {"R": 1, "P": 2, "S":3}

OUTCOME_SCORE = {"R": {"R":3, "P": 0, "S":6},
                 "P": {"R":6, "P":3, "S":0},
                 "S": {"R":0, "P": 6, "S":3}}

def find_score(filename):
    op_score = 0
    my_score = 0
    with open(filename) as f:
        for line in f.readlines():
            op, me = line.split()
            op_shape = SHAPE_DICT[op]
            my_shape = SHAPE_DICT[me][op_shape]
            op_score += SHAPE_SCORE[op_shape] + OUTCOME_SCORE[op_shape][my_shape]
            my_score += SHAPE_SCORE[my_shape] + OUTCOME_SCORE[my_shape][op_shape]
    print(f"OPPONENT'S SCORE: {op_score}\nMY SCORE: {my_score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "RockPaperScissors",
                description = 'find your score'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    find_score(args.filename)