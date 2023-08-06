#!/usr/bin/env python
import os, sys, glob, yaml, subprocess
from yui import tsklib

def main():
    argv = sys.argv;
    argv.pop(0); # remove first element, pointing to script itself
    if len(argv) != 1 :
        print("""
        open single task with text editor ( see ~/.tsk/config.yaml )
        Usage:
            """+tsklib.cmd+""" open %taskId%   - by default parameter is interprited as taskId
            """+tsklib.cmd+""" open id%taskId%   - parameter is task id
            """+tsklib.cmd+""" open cur%taskNo%   - parameter is task order number as it is shown by `"""+tsklib.cmd+""" list cur` command
            """+tsklib.cmd+""" open heap%taskNo%   - parameter is task order number as it is shown by `"""+tsklib.cmd+""" list heap` command
        Examples:
            """+tsklib.cmd+""" open 3
            """+tsklib.cmd+""" open id3
            """+tsklib.cmd+""" open cur1
            """+tsklib.cmd+""" open heap1            
            """)
        exit(1);
        pass;
    id = argv[0]
    filename = tsklib.getTaskFilenameByIdOrNum(id)
    #print("filename: "+filename)
    try:
        editor = tsklib.getConfigParam("editor")
    except:
        candidates = [ os.getenv("EDITOR"), "mcedit","nano", "vim", "vi","ee"]
        for candidate in candidates:
            if subprocess.call("which " + candidate + "> /dev/null", shell=True) == 0:
                editor = candidate+" %"
                break
            pass
    if editor=="":
        print("Can't detect text editor, use "+tsklib.tskpath()+"/config.yaml to specify");
        exit(1);
        pass

    cmd = editor.replace("%", filename)
    subprocess.call( cmd, shell=True );
    pass

if __name__=="__main__":
    main()
    pass
