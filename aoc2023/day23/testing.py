# -*- coding: utf-8 -*-
"""
You're currently on the single path tile in the top row; 
your goal is to reach the single path tile in the bottom row. 
Because of all the mist from the waterfall, the slopes are 
probably quite icy; if you step onto a slope tile, your next 
step must be downhill (in the direction the arrow is pointing). 
To make sure you have the most scenic hike possible, never step
onto the same tile twice. What is the longest hike you can take?
"""
import pprint
import queue
import textwrap
from collections import deque

def create_graph(filename):
    with open(filename) as f:
        slopes = [l.strip() for l in f.readlines()]
    graph = {}
    graph_2 = {}
    start = (0, 0)
    for i, row in enumerate(slopes):
        for j, value in enumerate(row):
            if value == "#":
                continue
            graph[(i,j)] = []
            graph_2[(i,j)] = set()
            pos_moves = []
            all_moves = []
            above = (max(i - 1, 0), j)
            all_moves.append(above)
            if value in ".^":
                pos_moves.append(above)
            left = (i, max(j - 1, 0))
            all_moves.append(left)
            if value in ".<":
                pos_moves.append(left)
            below = (min(i + 1, len(slopes) - 1), j)
            all_moves.append(below)
            if value in ".v":
                pos_moves.append(below)
            left = (i, min(j + 1, len(row) -1))
            all_moves.append(left)
            if value in ".>":
                pos_moves.append(left)
            for next_term in all_moves:
                x, y = next_term
                if next_term != (i, j) and slopes[x][y] != "#":
                    if next_term in pos_moves:
                        graph[(i,j)].append((x,y))
                    graph_2[(i,j)].add((x,y))
            if i == 0 and value == ".":
                start = (i, j)
            if i == len(slopes) -1 and value == ".":
                end = (i,j)
    k = findLongestPath(graph, start)
    print(k)
    bad_try = create_tree_r(graph_2, (1,1), set(), end)
    bad_try.calculate_distance()
    max_dist = bad_try.max_distance(end) 
    print(max_dist + 1)

    
def dfs(node, adj, dp, vis): 
    # Mark as visited 
    vis[node] = True
    # Traverse for all its children 
    for child in adj[node]:  
        # If not visited 
        if not vis[child]:
            dfs(child, adj, dp, vis) 
        # Store the max of the paths 
        dp[node] = max(dp[node], 1 + dp[child]) 


class Tree:
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
        self.parents = []
        self.children = []
        self.distance = 0


    def add_child(self, other_tree):
        """
        Adds an existing tree as a child of the tree.

        Parameter:
        - other_tree: Tree to add as a child subtree.
        """
        if not isinstance(other_tree, Tree):
            raise ValueError("Parameter to add_child must be a Tree object")
        self.children.append(other_tree)

    
    def calculate_distance(self):
        for child in self.children:
            child.distance += self.distance+ 1
            child.calculate_distance()


    def num_children(self):
        """Returns the number of children"""
        return len(self.children)

    def max_distance(self, point):
        max_dist = 0
        if self.key == point:
            max_dist = self.distance
        for child in self.children:
            child_max = child.max_distance(point) 
            if child_max > max_dist:
                max_dist = child_max 
        return max_dist

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
                lprefix1 = prefix[:-3] + u"  └─{}───".format(self.distance)
            else:
                lprefix1 = prefix[:-3] + u"  ├─{}───".format(self.distance)
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


def create_tree_r(graph, point, visited, end):
    tree = Tree(point)
    next_visited = graph[point].difference(visited)
    if len(next_visited) == 0 or point == end:
        return tree
    visited.add(point)

    for n in next_visited:
        p = point
        distance = 0
        c = visited.copy()
        while True:
            if len(graph[n]) != 2:
                break 
            c.add(n)
            pos_points = graph[n].difference(c)
            if not pos_points:
                break
            p = n 
            n = pos_points.pop()
            distance += 1
        child = create_tree_r(graph, n, c, end)
        child.distance = distance
        tree.add_child(child)
    return tree

def findLongestPath(adj, n): 
    dp = {}
    vis = {}
    for node in adj:
        vis[node] = False
        dp[node] = 0
     
    # Call DFS for every unvisited vertex 
    dfs(n, adj, dp, vis) 
    ans = 0
    # Traverse and find the maximum of all dp[i] 
    ans = dp[n]
      
    return ans 