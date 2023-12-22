# Unload supplies from ships
# stored in stacks of marked crates - needed supplies buried under other crates
# ship has giant cargo crane to move crates between stacks
# need to find out which crates  will end up where

# INPUT: drawing of starting stacks of crates and rearrangement procedure
# Return the top crate of each stack in order.

import argparse
import sys
import re 

sys.path.insert(0, '../helper_scripts/')
import stack

def stack_supplies(filename, model):
    strings = []
    stacks = {}
    instructions = []
    with open(filename) as f:
        for line in f.readlines():
            if "[" in line:
                group = ''
                for letter in line.strip('\n'):
                    group += letter
                    if len(group) == 4 or letter == ']':
                        strings.append(group.strip('[] '))
                        group = ''
                if group:
                    strings.append(group.strip('[] '))
            elif "move" in line:
                moves = re.split('move | from | to ', line.strip())
                moves = [int(val) for val in moves if val]
                instructions.append(moves)
            elif line.strip() != '':
                stack_len = max(line.strip().split())
                for i in range(int(stack_len)):
                    stacks[i + 1] = stack.Stack()
    input_crates(stacks, strings, int(stack_len))
    if model == "9000":
        move_crates_9000(stacks, instructions)
    else:
        move_crates_9001(stacks, instructions)
    val = get_top_crates(stacks, int(stack_len))
    print(val)
    

def input_crates(stacks, strings, stack_len):
    i = stack_len
    strings.reverse()
    for string in strings:
        if string:
            stacks[i].push(string)
        i -= 1
        if i == 0:
            i = stack_len
    

def move_crates_9000(stacks, instructions):
    for num, stack1, stack2 in instructions:
        for _ in range(num):
            val = stacks[stack1].pull()
            stacks[stack2].push(val)


def move_crates_9001(stacks, instructions):
    for num, stack1, stack2 in instructions:
        vals = []
        for _ in range(num):
            vals.append(stacks[stack1].pull())
        vals.reverse()
        for val in vals:
            stacks[stack2].push(val)


def get_top_crates(stacks, stack_len):
    val = ''
    for i in range(stack_len):
        v = stacks[i + 1].pull()
        val += v
    return val


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "SupplyStack",
                description = 'rearranges stacks'
    )
    parser.add_argument('filename')
    parser.add_argument('model')
    args = parser.parse_args()
    stack_supplies(args.filename, args.model)