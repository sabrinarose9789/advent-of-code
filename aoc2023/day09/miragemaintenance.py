import argparse 

def find_next_sequence(seq):
    a = 1
    x = seq.pop()
    rows =[[x]]
    seq.reverse()
    for s in seq:
        rows[0].append(s)
        if len(rows) > 1:
            for i, row in enumerate(rows[1:], 1):
                row.append(rows[i - 1][-2] - rows[i - 1][-1])
        rows.append([rows[-1][0] - rows[-1][1]])
    prev = 0 
    rows.reverse()
    for r in rows:
        prev += r[0]
    return prev


def maintain_mirage(filename):
    histories = []
    prev_histories = []
    with open(filename) as f:
        for line in f.readlines():
            seq = [int(x) for x in line.split()]
            hist = find_next_sequence(seq)
            seq =  [int(x) for x in line.split()]
            seq.reverse()
            prev_hist = find_next_sequence(seq)
            histories.append(hist)
            prev_histories.append(prev_hist)
    print(sum(histories))
    print(sum(prev_histories))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Haunted Wasteland",
                description = 'Navigate scary place'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    maintain_mirage(args.filename)