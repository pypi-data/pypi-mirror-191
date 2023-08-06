#!/usr/bin/env python
import os, sys, glob
from yui import tsklib


def main():
    argv = sys.argv;
    argv.pop(0); # remove first element, pointing to script itself
    if len(argv) != 1 :
        print("""
        completely remove single task with specified id or order number
        Usage:
            """+tsklib.cmd+""" drop %taskId%        - use task id
            """+tsklib.cmd+""" drop id%taskId%      - use task id
            """+tsklib.cmd+""" drop cur%taskNum%    - use order number from `"""+tsklib.cmd+""" list cur`
            """+tsklib.cmd+""" drop heap%taskNum%   - use order number from `"""+tsklib.cmd+""" list heap`
        Example:
            """+tsklib.cmd+""" drop 3
            """+tsklib.cmd+""" drop id3
            """+tsklib.cmd+""" drop cur1
            """+tsklib.cmd+""" drop heap2
            """)
        exit(1);
        pass;
    id = argv[0]
    file = tsklib.getTaskFilenameByIdOrNum(id)
    print("Deleting task "+file+" .. ", end="")
    os.remove(file)
    print("done")
    pass

if __name__=="__main__":
    main()
    pass

