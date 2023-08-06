#!/usr/bin/env python
"""
move unfinished tasks back to heap
"""
import os, sys, glob, yaml, subprocess
from yui import tsklib

def main():
    argv = sys.argv;
    argv.pop(0); # remove first element, pointing to script itself
    if len(argv) != 1 :
        print("""
        Usage:
            """+tsklib.cmd+""" reset %taskId%   - move single task back to heap by id
            """+tsklib.cmd+""" reset id%taskId%   - move single task back to heap by id
            """+tsklib.cmd+""" reset cur%taskNum%   - move single task back to heap, using order number from """+tsklib.cmd+""" list cur
            """+tsklib.cmd+""" reset all        - move all unfinished tasks back to heap
        Example:
            """+tsklib.cmd+""" pick 3
            """+tsklib.cmd+""" pick id3
            """+tsklib.cmd+""" pick cur3
            """)
        exit(1);
        pass;
    id = argv[0]
    tasks = []

    if id == "all":
        tasks = tsklib.listTasks( "cur" );
        pass
    else:
        tasks.append( tsklib.getTaskByIdOrNum( id, "cur") )
        pass
    
    if len(tasks) == 0:
        print("task with id="+id+" not found in cur")
        exit(1)
        pass

    for task in tasks:
        if task["status"] in ["done","fail"] :
            continue
        pass
        targetPath = tsklib.tskpath() + "/heap/"+task["status"]
        os.makedirs(targetPath, exist_ok=True)
        print("moving " + task["filename"] + " back to heap .. ", end="")
        os.rename( task["fullfilename"], targetPath + "/" + task["filename"]);
        print("done")
    pass
    tsklib.gitAddCommitTask("reset "+id);
    pass

if __name__=="__main__":
    main()
    pass


