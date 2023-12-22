import glob
import heapq
import csv 
import os
import argparse

strength = {"A": "z",
            "K": "y",
            "Q": "x",
            "T": "v",
            "9": "u",
            "8": "t",
            "7": "s",
            "6": "r",
            "5": "q",
            "4": "p",
            "3": "o",
            "2": "n"}

def get_weight(cards, js_weight):
    weight = ''
    tot = {}
    strength["J"] = js_weight
    js = 0
    for i, card in enumerate(cards):
        card = strength[card]
        if card == "a":
            js += 1
        else:
            tot[card] = tot.get(card, 0) + 1 
        weight += card
    if js != 5:
        max_val = max(tot, key=(lambda key: tot[key]))
    if (js == 5) or (tot[max_val] + js == 5):
        return 'm' + weight
    elif (tot[max_val] + js == 4):
        return 'l' + weight
    elif (tot[max_val] + js == 2):
        pairs = 0
        for key in tot:
            if tot[key] == 2:
                pairs += 1
        if pairs == 2:
            return "i" + weight
        return "h" + weight
    elif (tot[max_val] + js == 3):
        if tot[max_val] == 3 and 2 in tot.values():
            return "k" + weight
        for w in tot:
            if w != max_val and tot[w] == 2 and js == 1:
                return "k" + weight
        return "j" + weight
    return "g" + weight


def sort_file(filename):
    fid = 1
    lines_jacks = []
    lines_jokers = []

    with open(filename, 'r') as f_in:
        for line_num, line in enumerate(f_in.readlines(), 1):
            line_vals = {}
            cards, bid = line.split()
            line_vals["cards"] = cards 
            line_vals["bid"] = int(bid)
            line_vals["weight"] = get_weight(cards, "w")
            lines_jacks.append(line_vals.copy())
            line_vals["weight"] = get_weight(cards, "a")
            lines_jokers.append(line_vals)
    lines_jacks = sorted(lines_jacks, key=lambda k:k["weight"])
    lines_jokers = sorted(lines_jokers, key=lambda k:k["weight"])
    return (lines_jacks, lines_jokers)


def camel_cards(filename):
    lines = sort_file(filename)
    for l in lines:
        score = 0
        for line_num, line in enumerate(l, 1):
            score += line_num * int(line["bid"])
        print(score)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Wait For It",
                description = 'Who wins the boat race'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    camel_cards(args.filename)

