# elves yell to meet back up with them upriver
# get to communication device, but screen broke.
# cathode-ray tub screen and simple CPU driven by clock circuite
#   clock circuit clicks at constant rate (tick called cycle)
# find out signal being sent by CPU
#   Has single register X which starts with the value 1
#   Two instructions:
#       addx V takes two cycles to complete. After two cycles the X register
#           is increased by the value V (V can be negative)
#       noop takes one cycle to complete. Has no other effect
# INPUT: series of instructions
# Signal strength: cycle number multipled by value of the X register
# OUTPUT: signal strength at 20th cycle plus every 40th cycle after that
import argparse
import numpy as np

def read_instructions(filename):
    CRT = []
    cycle_check = 20
    signal_strength = 0
    X = 1
    prev_add = None
    with open(filename) as f:
        CRT_row = ''
        for i in range(1, 242):
            col = (i - 1) - (i- 1) // 40 * 40
            if col == 0 and CRT_row:
                CRT.append(CRT_row)
                CRT_row = ''
            if col <= X + 1 and col >= X- 1:
                CRT_row += '#'
            else:
                CRT_row += '.'
            if i == cycle_check:
                signal_strength += X * cycle_check
                cycle_check += 40
            if prev_add:
                X += prev_add
                prev_add = None
            else:
                line = f.readline()
                if line and 'noop' != line.strip():
                    _, add_str = line.split()
                    prev_add = int(add_str)
    print('signal strength: ',signal_strength, '\nmessage:')
    for line in CRT:
        print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Cathode-RayTube",
                description = 'Design replacement for device video system'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    read_instructions(args.filename)