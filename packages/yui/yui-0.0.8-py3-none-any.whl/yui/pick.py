#!/usr/bin/env python
import os, sys, glob, yaml, subprocess
from yui import tsklib

def main():
    argv = sys.argv;
    argv.pop(0); # remove first element, pointing to script itself
    if len(argv) != 1 :
        print("""
        pick single task to current day
        Usage:
            """+tsklib.cmd+""" pick %taskId%
            """+tsklib.cmd+""" pick id%taskId%
            """+tsklib.cmd+""" pick heap%taskNum%  - taskNum is order number from `"""+tsklib.cmd+""" list heap` command
            """+tsklib.cmd+""" pick %taskId1%,%taskId2%,%taskId3%,%taskId4%..%taskId100%    - pick array of ids and/or ranges of ids
        Example:
            """+tsklib.cmd+""" pick 3
            """+tsklib.cmd+""" pick id3
            """+tsklib.cmd+""" pick heap1
            """+tsklib.cmd+""" pick 141,142,143..150
            """)
        exit(1);
        pass;
    tsklib.pickTasks( argv[0] )
    pass

if __name__=="__main__":
    main()
    pass

