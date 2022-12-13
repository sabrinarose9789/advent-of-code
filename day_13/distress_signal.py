# receive a distress signal from the elves
# packets from distress signal got decoded out of order
# Input: list of received packets to decode message
#   list consists of pairs of packets
#   pairs are separated by a blank line
#   identify how many pairs of packets are in the right order
# List:
#   packet dat a consists of lists and inteters
#   eah list starts with [ and ends with ] and contains zero or more 
#   comma-separated values (either integers or other lists)
#   each lsit is it's own line
# when comparing two vals, the first val is left and second is right
    # If both values are integers, the lower integer should come first
    # If both values are lists, compare the first val of each list,
    # then the second and so on. If the left list runs out of items first,
    # left considered in right order
    # If exactly one value is an integer, convert the integer to a lit
import argparse
import ast

def compare_list(list1, list2):
    for j, val1 in enumerate(list1):
        if len(list2) <= j:
            return False
        val2 = list2[j]
        if type(val1) == int and type(val2) == int:
            if val1 < val2:
                return True
            if val2 < val1:
                return False
            else:
                continue
        if type(val1) == int:
            val1 = [val1]
        if type(val2) == int:
            val2 = [val2]
        if val1 == val2:
            continue
        else:
            return compare_list(val1, val2)
    return True
        

def correct_orders(filename):
    indices = 0
    list_sort = []
    with open(filename) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            list1 = ast.literal_eval(lines[i].strip())
            list2 = ast.literal_eval(lines[i + 1].strip())
            result = compare_list(list1, list2)
            if result:
                list_sort.extend([list1, list2])
                indices += i // 3 + 1 
            else:
                list_sort.extend([list2, list1])
    print(indices)
    return list_sort


def sort(lst):
    less = []
    equal = []
    greater = []
    if len(lst) > 1:
        pivot = lst[0]
        for x in lst:
            if x == pivot:
                equal.append(x)
                continue
            result = compare_list(x, pivot)
            if result:
                less.append(x)
            else:
                greater.append(x)
        return sort(less) + equal + sort(greater)
    else:
        return lst


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Distress Signal",
                description = 'Fix distress signal'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    list_sort = correct_orders(args.filename)
    list_sort.append([[2]])
    list_sort.append([[6]])
    sorted_list = sort(list_sort)
    ind1 = sorted_list.index([[2]]) + 1
    ind2 = sorted_list.index([[6]]) + 1 
    print(ind1 * ind2)