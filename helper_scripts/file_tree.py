import textwrap

class Tree:
    def __init__(self, name=None, size=0):
        self.name = name
        self.size = size
        self.container = {}

    def add_to_directory(self, tree, dir):
        if dir == self.name:
            self.container[tree.name] = tree
        elif len(self.container) > 0:
            for file in self.container.values():
                file.add_to_directory(tree, dir)
        
    def compute_size(self):
        if len(self.container) == 0:
            return self.size
        self.size = 0
        for file in self.container.values():
            self.size += file.compute_size()
        return self.size
        
    def get_small_directories(self):
        val = 0
        if len(self.container) == 0:
            return val
        if self.size <= 100000:
            val += self.size
        for file in self.container.values():
            val += file.get_small_directories()
        return val

    def find_previous_directory(self, curdir):
        if curdir in self.container:
            return self.name
        for tree in self.container.values():
            dir = tree.find_previous_directory(curdir)
            if dir:
                return dir
        return None

    def num_children(self):
        return len(self.container)

    def find_smallest_to_delete(self, needed):
        if len(self.container) == 0:
            return None
        if self.size < needed:
            return None
        val = self.size
        for tree in self.container.values():
            small = tree.find_smallest_to_delete(needed)
            if small and small < val:
                val = small
        return val

    def __print_r(self, prefix, last, kformat, vformat, maxdepth, paths):
        """
        Recursive method to print out the tree. Should not be
        called directly. See print() method for more details.
        """

        if maxdepth is not None:
            if maxdepth == 0:
                return
            else:
                maxdepth -= 1    

        if len(prefix) > 0:
            if last:
                lprefix1 = prefix[:-3] + u"  └──"
            else:
                lprefix1 = prefix[:-3] + u"  ├──"
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
        
        if paths:
            if hasattr(self, 'path'):
                value = self.path
            else:
                value = "no path attribute"
        else:
            value = self.size

        ltext = (kformat + ": " + vformat).format(self.name, value)

        ltextlines = textwrap.wrap(ltext, 80, initial_indent=lprefix1, 
            subsequent_indent=lprefix3)

        print(lprefix2)
        print(u"\n".join(ltextlines))

        for i, st in enumerate(self.container.values()):
            if i == self.num_children() - 1:
                newprefix = prefix + u"   "
                newlast = True
            else:
                newprefix = prefix + u"  │"
                newlast = False

            st.__print_r(newprefix, newlast, kformat, vformat, maxdepth, paths)
    
    
    def print(self, kformat="{}", vformat="{}", maxdepth=None, paths=False):
        """
        Prints out the tree.
        
        Parameters:
        - kformat, vformat: Format strings for the key and value.
        - maxdepth: Maximum depth to print.
        """
        
        self.__print_r(u"", False, kformat, vformat, maxdepth, paths)
