# given device with communication system
# it is malfunctioning
# device needs to lock onto their signal. random series of chars,
# received one at a time
# need to add a subroutine to the device that detects start-of-packet marker
    # determined by sequence of four characters that are all different
# INPUT: string (datastream buffer)
# determine # of characters processed before first marker found

import argparse


def find_marker(filename, dist):
    with open(filename) as f:
        line = f.readline()
        prev = line[:dist - 1]
        cur = dist -1
        for char in line[dist - 1:]:
            cur += 1
            prev = prev + char
            if len(set(prev)) == len(prev):
                print(cur)
                break
            prev = prev[1:]
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "tuningTrouble",
                description = 'fix malfunctioning communication device'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    print("First marker found at:")
    find_marker(args.filename, 4)
    print("\nMessage marker found at:")
    find_marker(args.filename, 14)