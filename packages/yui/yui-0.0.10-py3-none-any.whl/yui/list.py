#!/usr/bin/env python
import os, sys, glob, yaml, subprocess, datetime
from yui import tsklib
from pathlib import Path



def addTitle( dataString, title ):
    gap = 2
    titleString = "[ "+title+" ]"
    if title == "cur":
        titleString = "[ Current tasks ]"
        pass
    if title == "heap":
        titleString = "[ Heap/Backlog ]"
        pass
    startPos = len(dataString) - gap - len(titleString)
    return dataString[0:startPos] + titleString + dataString[startPos+len(titleString):len(dataString)]
    pass


def main():
    argv = sys.argv;
    argv.pop(0); # remove first element, pointing to script itself
    noColor = tsklib.color("noColor")
    if len(argv) == 0 :
        print("""
        Usage:
            """+tsklib.cmd+""" list heap   - list task from heap / global backlog
            """+tsklib.cmd+""" list cur    - list task picked for current day
            """)
        exit(1);
        pass;

    location = argv[0]

    def mb_strlen( s ):
        return len(str(s)) #.encode('utf-16-le'))
        pass

    tasks = tsklib.listTasks( location )

    if len(tasks) == 0:
        print("No tasks found in "+location+noColor)
        exit(1)
        pass
    keys = ["No.", "id", "context", "project", "name", "status"];

    maxLenghts = {};
    for key in keys:
        #print(key)
        maxLenghts[key] = mb_strlen(key);
        for task in tasks:
            length = mb_strlen(task[key]);
            if length > maxLenghts[key]:
                maxLenghts[key] = length;
                pass
            pass
        pass

    columnNames = {};
    horizontalLines = {};
    rows = []
    for task in tasks:
        rows.append({})
        pass
    for key in keys:
        columnNames[key] = key.ljust( maxLenghts[key])
        horizontalLines[key] = "".ljust( maxLenghts[key], "─")
        for i, task in enumerate(tasks):
            rows[i][key] = str(task[key]).ljust( maxLenghts[key] )
            pass
        pass

    print("╭─"+"─┬─".join(horizontalLines.values())+"─╮");
    print("│ "+" │ ".join(columnNames.values()    )+" │");
    print("├─"+"─┼─".join(horizontalLines.values())+"─┤");
    for i, task in enumerate(tasks):
        row = rows[i]
        color = tsklib.statusColor( task["status"] )
        print("│ "+color+(noColor+" │ "+color).join(row.values())+noColor+" │")
        pass
    print( addTitle("╰─"+"─┴─".join(horizontalLines.values())+"─╯", location ))
    print( tsklib.color("gray")+"  ", end="" )
    if location == "heap":
        print("Hint: use `"+tsklib.cmd+" pick %taskId%` to pick task from the Heap to Current tasks ")
        pass
    if location == "cur":
        print("""Hint: use `"""+tsklib.cmd+""" open` to open task in text editor, `"""+tsklib.cmd+""" reset` to move task(s) back to the Heap, `"""+tsklib.cmd+""" archive` to archive done tasks""")
        pass

    print(tsklib.color("noColor"))
    pass

if __name__ == "__main__":
    main()
    pass
