import os,platform

def color( key ):
    linuxColors = {
        "red":"\033[1;31m",
        "green":"\033[1;32m",
        "yellow":"\033[1;93m",
        "gray":"\033[2;37m",
        "noColor":"\033[0m", # No Color
        }
    windowsColors = {
        "red":"4",
        "green":"2",
        "yellow":"6",
        "gray":"8",
        "noColor":"7", # No Color        
        }
    if platform.system() == "Windows":
        os.system("color "+windowsColors[key])
        return
    print(linuxColors[key], end="")
    pass
#print("|", end="")
color("green")
print("|", end="")
print("greentext", end="")
print("|")
#color("noColor")
#print("|")
