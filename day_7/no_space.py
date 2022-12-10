# want to run systems update on the device, but no space
# Input: terminal output from browsing
# commands start with $ - 
#   cd - change directory
#       cd x - move to directory x in current directory
#       cd .. - move out one level
#       cd /  - move to outermost directory
#   ls - list
#       123 abc - current directory has file abc with size 123
#       dir xyz - current directory contains directory xyz
# find total size of each directory:
#   sum of files in directory and the size of any directory within it
# sum up all the directories with total size at most 100000
import argparse
import sys
import re 

sys.path.insert(0, '../helper_scripts/')
import file_tree

def build_filetree(filename):
    tree = file_tree.Tree(name='/')
    cur_dir ='/'
    with open(filename) as f:
        for line in f.readlines():
            if '$' not in line:
                m = re.search('(?<=dir )(.*)(?=)', line)
                if m:
                    if cur_dir == '/':
                        name = cur_dir + m.group(1)
                    else:
                        name = cur_dir + '/' + m.group(1)
                    val = file_tree.Tree(name=name)
                else:
                    size, filename = line.split()
                    val = file_tree.Tree(name=filename, size=int(size))
                tree.add_to_directory(val, cur_dir)
            else:
                m = line.split("cd ")
                if len(m) > 1: 
                    val = m[1].strip()
                    if val == '..':
                        if cur_dir != '/':
                            cur_dir, _ = cur_dir.rsplit('/', 1)
                            if '/' not in cur_dir:
                                cur_dir = '/'
                    elif val == '/':
                        cur_dir = '/'
                    else:
                        if cur_dir[-1] == '/':
                            cur_dir += val
                        else:
                            cur_dir += '/' + val
    tree.compute_size()
    tree.print()
    return tree
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog = "NoSpace",
                description = 'find space on the device for update'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    files = build_filetree(args.filename)
    print("size of smallest files: ",files.get_small_directories())
    cur_disk_used = files.size
    cur_disk_free = 70000000 - cur_disk_used
    space_needed = 30000000 - cur_disk_free
    print("the size of file to delete: ",
          files.find_smallest_to_delete(space_needed))