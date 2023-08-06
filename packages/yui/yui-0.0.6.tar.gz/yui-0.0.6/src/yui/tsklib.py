#!/usr/bin/env python
import os, glob, yaml, datetime, subprocess
from appdata import AppDataPaths
from sanitize_filename import sanitize
from pathlib import Path
from unidecode import unidecode
import platform

Title="Yui"
cmd="yui"
scopeNames = {
    "context":[],
    "project":[],
    }

def tskpath():
    default=cmd
    home = os.getenv("YUI_HOME", default)
    if platform.system() == "Windows":
        home = os.getenv('LOCALAPPDATA')+"/"+home 
        pass
    path = AppDataPaths(home).app_data_path
    os.makedirs(path, exist_ok=True)
    return path
    pass

def getTaskFilenameById(id, location="*"):
    files = findTaskFiles( location, "*."+id+".md")
    if len(files) == 0:
        suffix = ""
        if location !="*":
            suffix = " in "+location
        print("task with id="+id+" not found"+suffix)
        exit(1)
    pass;
    if len(files) != 1:
        print("more than one task with id="+id+" found. That should never happen")
        exit(1)
    pass;
    return files[0]
    pass

def getTaskFilenameByIdOrNum( idOrNum, location="*"):
    if idOrNum.isnumeric():
        return getTaskFilenameById( idOrNum, location )
        pass
    if idOrNum[:2] == "id":
        return getTaskFilenameById( idOrNum[2:], location )
        pass
    if idOrNum[:3] == "cur":
        return getTaskFilenameByNum( idOrNum[3:], "cur")
        pass
    if idOrNum[:4] == "heap":
        return getTaskFilenameByNum( idOrNum[4:], "heap")
        pass
    print("Unknown task id or number format");
    pass

def getTaskByIdOrNum( idOrNum, location="*"):
    if idOrNum.isnumeric():
        return getTaskById( idOrNum, location )
        pass
    if idOrNum[:2] == "id":
        return getTaskById( idOrNum[2:], location )
        pass
    if idOrNum[:3] == "cur":
        return getTaskByNum( idOrNum[3:], "cur")
        pass
    if idOrNum[:4] == "heap":
        return getTaskByNum( idOrNum[4:], "heap")
        pass
    print("Unknown task id or number format");
    pass



def getTaskFilenameByNum( num, location ):
    return getTaskByNum( num, location )["fullfilename"]
    pass

def getTaskById(id, location="*"):
    filename = getTaskFilenameById( str(id), location )
    task = loadYaml( filename )
    task["fullfilename"] = filename
    return task
    pass

def getTasksByIds( ids ):
    re = []
    for id in ids:
        re.append( getTaskById(id) )
        pass
    return re
    pass    

def getTaskByNum( num, location ):
    tasks = listTasks( location )
    for task in tasks:
        if int(task["No."]) == int(num):
            return task
    print("Task "+num+" not found in "+location)
    pass



def findTaskFiles(location, pattern):
    return glob.glob( tskpath() + "/"+location+"/*/"+pattern)
    pass

def listTasks(location, useScope=True):
    scope = getScope();
    files = findTaskFiles( location, "*.md" )
    tasks = []
    for filename in files:
        task = loadYaml(filename)
        task["fullfilename"] = filename
        addItem = True
        for key in scope:
            addItem = addItem and ( scope[key] == "" or scope[key] == task[key] )
            pass
        if useScope and not addItem:
            continue
            pass
        tasks.append( task )
        pass
    tasks = sorted(tasks, key = lambda task : task["id"])
    key = 0
    for task in tasks:
        key = key+1
        task["No."] = key
        pass
    return tasks
    pass

def getConfigParam(param):
    return loadYaml( tskpath() + "/config.yaml" )[param]
    pass

def loadYaml(filename):
    with open( filename, 'rb' ) as f:
        return next(yaml.load_all(f, Loader=yaml.loader.UnsafeLoader))
        pass
    pass

def saveYaml(filename, data):
    with open( filename, 'w' ) as f:
        yaml.dump( data, f )
        pass
    pass

def gitExist()->bool:
    try:
        re = subprocess.run(["git","-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        return False
    return re.returncode == 0
    pass

def gitInitIfNotPresent():
    workingdir = tskpath()
    if os.path.isdir( workingdir+"/.git"):
        return
        pass
    curpath = os.getcwd();
    os.chdir(workingdir);
    os.system("git init > /dev/null");
    os.chdir(curpath);
    pass

def gitAddCommitTask(message):
    if not gitExist():
        print("git not exist");
        return
        pass
    gitInitIfNotPresent()
    curpath = os.getcwd();
    os.chdir(tskpath());
    os.system("git add ./*.md > /dev/null && git commit -m '"+message+"' > /dev/null");
    os.chdir(curpath);
    pass

def getLastId():
    files = findTaskFiles("*", "*.md")
    maxId = -1
    for filename in files :
        # Open the file and load the file
        id = loadYaml( filename )["id"]
        if id > maxId:
            maxId = id
            pass
        pass
    return maxId
    pass

def newScope():
    return {
        "project":"",
        "context":""
        }
    pass

def loadScope():
    scope = newScope()
    try:
        data = loadYaml( tskpath()+"/scope.yaml")
        for key in scope:
            try:
                scope[key] = data[key]
            except:
                pass
            pass
    except:
        pass
    return scope
    pass

def mergeScope( orig, changes ):
    scope = orig
    for key in changes:
        if changes[key] == "":
            continue
        scope[key] = changes[key]
    return scope
    pass

def parseFilter( filterstring ):
    scope = newScope()
    if filterstring == "":
        return scope
        pass
    # split by ,
    pairs = filterstring.split(",")
    for pair in pairs:
        keyvalue = pair.split(":")
        key = keyvalue[0]
        value = keyvalue[1]
        if key == "c":
            key = "context"
            pass
        if key == "p":
            key = "project"
            pass
        scope[key] = value
        pass
    return scope
    pass

def getDefaultContextForProject( projectName ):
    try:
        return loadYaml( tskpath() + "/projects/" + projectName + ".yaml")["defaultContext"]
    except:
        return ""
    pass

def getScope():
    scope = loadScope()
    scope = mergeScope( scope, parseFilter(os.getenv(cmd.upper(),"")) )
    for key in scope:
        scope[key] = os.getenv(cmd.upper() + "_" + key.upper(), scope[key])
        pass
    if scope["context"] == "" and scope["project"] != "":
        scope["context"] = getDefaultContextForProject( scope["project"] )
        pass
    return scope
    pass

def saveScope( scope ):
    saveYaml( tskpath()+"/scope.yaml", scope)
    pass

def createTask( name ):
    name = name.strip()
    if name == "":
        return
    name = name.replace("\"","'")
    tasknameArr = name.split(" ")
    taskname = '_'.join( tasknameArr )
    taskname = unidecode( taskname )
    taskname = sanitize( taskname ).replace("'","").replace("\"","").replace("`","")
    taskDatetime = datetime.datetime.today()
    id = str( int( getLastId() )+1 )
    path = tskpath() + "/heap/new"
    filename = taskDatetime.strftime("%Y-%m-%d_%H.%M.%S_%z_")+taskname+"."+id+".md"
    os.makedirs(path, exist_ok=True)

    scope = getScope()

    Path( path + "/" + filename ).write_text("""---
name: \""""+name+"""\"
created: """+taskDatetime.strftime("%Y-%m-%d %H:%M:%S %z")+"""
context: """+scope["context"]+"""
project: """+scope["project"]+"""
filename:  """+filename+"""
status: new
id: """+id+"""
---
""", encoding='utf-8')
    
    gitAddCommitTask("created "+id);
    pass

def pickTask(id):
    filename = getTaskFilenameByIdOrNum(id, "heap")
    task = loadYaml(filename)
    targetPath = tskpath() + "/cur/" + task["status"]
    os.makedirs(targetPath, exist_ok=True)
    os.rename( filename, targetPath + "/" + task["filename"]);
    gitAddCommitTask("pick "+id);
    pass

def rangeQueryToArray(query):
    tasks = listTasks("heap")
    taskIds = []
    if ".." in query:
        for task in tasks:
            taskIds.append( task["id"] )
            pass
        pass
    #print(taskIds)
    ids = []
    queryElements = query.split(",")
    for queryElement in queryElements:
        taskRange = queryElement.split("..")
        if len(taskRange) == 1:
            ids.append( queryElement )
            continue
        pass
        if len(taskRange) > 2:
            raise Exception("Mailformed id range query")
        pass
        for item in range(int(taskRange[0]), int(taskRange[1])+1): # TODO generalize for curNNN, heapNNN
            if item in taskIds:
                ids.append(str(item))
                pass
            pass
        pass
    return ids
    pass

def pickTasks(query):
    '''
    pick one or more tasks using array and range, like pick 141,142,143..150
    pick only from results of listTasks(heap)
    '''
    pickTasksByIds( rangeQueryToArray(query) )
    pass

def pickTasksByIds( ids ):
    for id in ids:
        pickTask( str(id) )
        pass
    pass

def resetTask(idOrNum):
    task = getTaskByIdOrNum(idOrNum)
    if task["status"] in ["done","fail"]:
        return
        pass
    targetPath = tskpath() + "/heap/"+task["status"]
    os.makedirs(targetPath, exist_ok=True)
    os.rename( task["fullfilename"], targetPath + "/" + task["filename"]);
    pass

def resetTasksByIds( ids ):
    for id in ids:
        resetTask( str(id) )
        pass
    pass

def dropTask( id ):
    file = getTaskFilenameByIdOrNum(id)
    os.remove(file)
    pass

def dropTasksByIds(ids):
    for id in ids:
        dropTask( str(id) )
        pass
    pass

def loadScopeNames():
    tasks = listTasks("heap", useScope=False) + listTasks("cur", useScope=False)
    #print( tasks )
    for task in tasks:
        for key in ["context","project"]:
            if task[key] not in scopeNames[key]:
                if task[key] == None:
                    continue
                pass
                scopeNames[key].append( task[key] )
            pass
        pass
    print( scopeNames )
    pass

def getScopeNames( key ):
    if len( scopeNames[key]) == 0:
        loadScopeNames()
    return scopeNames[key]
    pass

