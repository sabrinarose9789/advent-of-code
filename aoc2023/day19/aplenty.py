import math
import sys
import re
import argparse
import textwrap
import pandas
import numpy as np


class Edge:
    """
    Class to define the branch between a root node and a child node
    """
    def __init__ (self, parent, child, splitval=None):
        """
        Constructor

        Creates a branch by matching the parent value with the subtree value,
        connected by what the value of the split attribute was to get the
        subtree

        Parameters:
         parent, child: DecisionTree objects
         splitval: string of what value the child tree was split on from the
                   parent (None if root node and therefore no split)
        """
        self.parent = parent.value
        self.child = child.value
        self.splitval = splitval


    def __str__(self):
        """
        String representation of Edge
        """
        string = ("edge from " + str(self.parent) + " to " +
               str(self.child) + " on " + str(self.splitval))
        return string


class DecisionTree:
    """
    A class representing a (non-null) tree with a root
    node and some number of child subtrees (which will,
    themselves, be instances of Tree)

    Based on Tree Class given in CS121 for PA6 with very minor changes
    """

    def __init__(self, k=None, v=None, edge=None):
        """
        Constructor.

        Creates either a tree with a root node and no
        child subtrees. The root node will have a key and
        value associated with it.

        Parameters
        - k, v: Key and value for the root node.
        - edge: Edge object
        """
        self.value = v
        self.key = k
        self.edge = edge
        self.children = []


    def add_child(self, other_tree):
        """
        Adds an existing tree as a child of the tree.

        Parameter:
        - other_tree: Tree to add as a child subtree.
        """
        if not isinstance(other_tree, DecisionTree):
            raise ValueError("Parameter to add_child must be a Tree object")

        self.children.append(other_tree)


    def num_children(self):
        """Returns the number of children"""
        return len(self.children)


    def __print_r(self, prefix, last, kformat, vformat, maxdepth):
        """
        Recursive method to print out the tree. Should not be
        called directly. See print() method for more details.

        Note: Design taken from provide tree in CS121 PA 6
        """

        if maxdepth is not None:
            if maxdepth == 0:
                return
            maxdepth -= 1

        if len(prefix) > 0:
            if last:
                lprefix1 = prefix[:-3] + u"  └─{}───".format(self.edge.splitval)
            else:
                lprefix1 = prefix[:-3] + u"  ├─{}───".format(self.edge.splitval)
        else:
            lprefix1 = u""

        if len(prefix) > 0:
            lprefix2 = prefix[:-3] + u"  │"
        else:
            lprefix2 = u""

        if last:
            lprefix3 = lprefix2[:-1] + "   "
        else:
            lprefix3 = lprefix2 + "  "

        ltext = (kformat + ": " + vformat).format(self.key, self.value)

        ltextlines = textwrap.wrap(ltext, 80, initial_indent=lprefix1,
            subsequent_indent=lprefix3)

        print(lprefix2)
        print(u"\n".join(ltextlines))

        for i, subtree in enumerate(self.children):
            if i == self.num_children() - 1:
                newprefix = prefix + u"   "
                newlast = True
            else:
                newprefix = prefix + u"  │"
                newlast = False

            subtree.__print_r(newprefix, newlast, kformat, vformat, maxdepth)


    def print(self, kformat="{}", vformat="{}", maxdepth=None):
        """
        Prints out the tree.

        Parameters:
        - kformat, vformat: Format strings for the key and value.
        - maxdepth: Maximum depth to print.
        """

        self.__print_r(u"", False, kformat, vformat, maxdepth)


def create_tree(filename):
    to_add = {}
    tree_done = False
    values = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if not line.strip():
                tree_done = True
                continue 
            if tree_done:
                val = {}
                numbers = line.strip("\n}{")
                pairs = numbers.split(",")
                for p in pairs:
                    letter, rating = p.split("=")
                    val[letter] = int(rating)
                values.append(val)
            else:
                workflow = line.strip("\n }").split("{")
                name = workflow[0]
                steps = workflow[1].split(',')
                tree = create_tree_r(steps, name)
                to_add[name] = tree
                if i == 0:
                    tree.print()
    main_tree = to_add["in"]
    main_tree = complete_tree_r(main_tree, to_add)
    main_tree.print()
    tot = 0
    for val in values:
        if traverse_tree(main_tree, val):
            tot += sum(v for v in val.values())
    print(tot)
    why = sum_tree_pos(main_tree)
    s = 0
    for x in why:
        s += math.prod(len(val) for val in x.values())
    print(s)


def traverse_tree(tree, val):
    if tree.key == "R":
        return False 
    if tree.key == "A":
        return True 
    for subtree in tree.children:
        k = tree.key.split(",")[-1]
        v = tree.value
        e = subtree.edge.splitval
        if "<=" in e and val[k] <= v:
            return traverse_tree(subtree, val)
        if "<" in e and val[k] < v:
            return traverse_tree(subtree, val)
        if ">=" in e and val[k] >= v:
            return traverse_tree(subtree, val)
        if ">" in e and val[k] > v:
            return traverse_tree(subtree, val)


def complete_tree_r(tree, to_add):
    for i, subtree in enumerate(tree.children):
        if subtree.key in to_add:
            v = subtree.edge
            subtree = complete_tree_r(to_add[subtree.key], to_add)
            subtree.edge = Edge(tree, subtree, v.splitval)
            tree.children[i] = subtree
        else:
            v = subtree.edge
            subtree = complete_tree_r(subtree, to_add)
            subtree.edge = Edge(tree, subtree, v.splitval)
            tree.children[i] = subtree
    return tree


def create_tree_r(steps, name):
    next_case = re.split(":", steps[0])
    if len(next_case) == 1:
        leaf = DecisionTree(next_case[0])
        leaf.edge = Edge(leaf, leaf, next_case[0])
        return leaf
    edge, next = next_case
    letter, change, amount = re.split("(<|>)", edge)
    tree = DecisionTree(name +"," +  letter, int(amount))
    alt_change = ">="
    if change == ">":
        alt_change = "<="
    child_1 = DecisionTree(next)
    child_1.edge = Edge(tree, child_1, change)
    child_2 = create_tree_r(steps[1:], name)
    child_2.edge = Edge(tree, child_2, alt_change)
    tree.add_child(child_1)
    tree.add_child(child_2)
    return tree


def sum_tree_pos(tree):
    results = []
    if tree.key == "R":
        return None
    if tree.key == "A":
        A_results = {}
        for i in "xmas":
            A_results[i] = set(range(1, 4001))
        return [A_results]
    for subtree in tree.children:
        k = tree.key.split(",")[-1]
        v = tree.value
        e = subtree.edge.splitval
        result = sum_tree_pos(subtree)
        if e in ("<=", ">"):
            v += 1
        if result:
            for r in result:
                if ">" in e:
                    r[k] = r[k].intersection(set(range(v, 4001)))
                else:
                    r[k] = r[k].intersection(set(range(1, v)))
                if r[k]:
                    results.append(r)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "Aplenty",
                description = 'This seems like a decision tree'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    create_tree(args.filename)
                        
