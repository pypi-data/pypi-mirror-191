#!/usr/bin/env python
import os, sys, glob, yaml, subprocess, datetime
from yui import tsklib
from pathlib import Path
from sanitize_filename import sanitize

def main():
    argv = sys.argv;
    argv.pop(0); # remove first element, pointing to script itself
    if len(argv) == 0 :
        print("""
    Usage:
        """+tsklib.cmd+""" create %taskname%   - create new task
    Example:
        """+tsklib.cmd+""" create do this and do that
        """)
        exit(1);
        pass;
    tasknameArr = argv
    tsklib.createTask( " ".join(tasknameArr) )
    pass

if __name__=="__main__":
    main()
    pass

