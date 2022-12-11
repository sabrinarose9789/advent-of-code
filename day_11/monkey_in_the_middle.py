# Monkeys playing with your things, need  to predict when they will
# throw them. Operate based on how worried you are about each item

# INPUT: Items each monkey has, how worried you are about it,
#        and how the moneky makes decisions based on your worry lefel
# Monkey attributes:
#   Starting items: lists worry level for each item moneky is holding in their order
#   Operations: how worry level changes based on the money inspecting it
#   Test: using worry level to decide where to throw next
# After each moneky inspects an item, but before testing worry level, relief
# the the moneky's inspection didn't damage the item causes your worry level to 
# be divided by three and rounded down
# Monkeys go in order (each monkey taking a single turn is a round)

# Focus on two most active monkeys to get items back
# Count on total number of times each monkey inspects item over 20 rounds
# Select two most active monkeys and multiply together
import argparse
import re
import monkey

def get_monkeys(filename):
    monkeys = {}
    mod_val = 1
    with open(filename) as f:
        monkey_paragraphs = f.read().split('\n\n')
        for m in monkey_paragraphs:
            m_lines = m.split('\n')
            m_num = int(re.search(r'\d+', m_lines[0]).group())
            items = list(map(int, re.findall(r'\d+', m_lines[1])))
            operations = m_lines[2].split()
            truth_test = int(re.search(r'\d+', m_lines[3]).group())
            t_monkey = int(re.search(r'\d+', m_lines[4]).group())
            f_monkey = int(re.search(r'\d+', m_lines[5]).group())
            monkeys[m_num] = monkey.Monkey(items, operations[-2], operations[-1], 
                                           truth_test, t_monkey, f_monkey)
            mod_val *= truth_test    
            print(monkeys[m_num], '\n')
    return monkeys, m_num, mod_val


def toss_around(monkeys, mod_val, num_monkeys, rounds):
    for _ in range(int(rounds)):
        for i in range(num_monkeys + 1):
            thrown = monkeys[i].throw_items(mod_val)
            for m, items in thrown.items():
                monkeys[m].items.extend(items)
    inspected = []
    for i in range(num_monkeys + 1):
        inspected.append(monkeys[i].inspected)
    
    largest = max(inspected)
    inspected.remove(largest)
    second = max(inspected)

    print(largest * second)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "MonkeyinTheMiddle",
                description = 'collect items from monkeys'
    )
    parser.add_argument('filename')
    parser.add_argument('rounds')
    args = parser.parse_args()
    monkeys, num_monkeys, mod_val = get_monkeys(args.filename)
    toss_around(monkeys, mod_val, num_monkeys, args.rounds)
