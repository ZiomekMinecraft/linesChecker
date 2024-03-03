import time
import os
import yaml

if not os.path.exists("./config.yml"):
    with open("./config.yml", "w") as f:
        f.write("path: null\nlastPath: null\nwhite-list: null\nblack-list: null\n# if true write checked files to console\nlog-files: false")

with open("./config.yml", 'r') as f:
    CONFIG = yaml.load(f, yaml.loader.FullLoader)

def getPath():
    if "path" in CONFIG and CONFIG["path"] != None:
        return CONFIG["path"]
    else:

        print(f"Write the path of press enter to chouse last path "+ ("("+CONFIG["lastPath"]+")") if "lastPath" in CONFIG and CONFIG["lastPath"] else "", end="")
        _path = input()

        if _path == None or _path == "":
            if "lastPath" in CONFIG and CONFIG["lastPath"] != None or CONFIG["lastPath"]:
                return CONFIG["lastPath"]
            else:
                print("Cannot specify path!")
                exit()
        return _path

path: str = getPath()

CONFIG["lastPath"] = path

with open("./config.yml", 'w') as f:
    yaml.dump(CONFIG, f, yaml.dumper.Dumper)

lines = dict({})

def getLines(filePath: str):
    name = filePath.split("/")
    name = name[len(name)-1]
    starName = name.split(".")
    starName = "*." + starName[len(starName)-1]
    if (CONFIG["black-list"].__class__ == list and name in CONFIG["black-list"]) or (CONFIG["black-list"].__class__ == list and starName in CONFIG["black-list"]):
        return
    if CONFIG["white-list"].__class__ == list and not name in CONFIG["white-list"] != CONFIG["white-list"].__class__ == list and not starName in CONFIG["white-list"]:
        return
    try:
        with open(filePath, 'r') as f:
            _lines = len(f.readlines())
        ext = filePath.split("/")
        ext = ext[len(ext)-1].split(".")
        ext = ext[len(ext)-1]
        if ext in lines:
            lines[ext] += _lines
        else:
            lines[ext] = _lines
        
        if CONFIG["log-files"]:
            print(filePath)
    except:
        pass

def directory(dpath: str):
    name = dpath.split("/")
    name = name[len(name)-1]
    if CONFIG["black-list"].__class__ == list and name in CONFIG["black-list"]:
        return
    dpath = dpath+"/" if not dpath.endswith("/") else dpath
    for file in os.listdir(dpath):
        if(os.path.isdir(dpath+file)):
            directory(dpath+file)
        elif(os.path.isfile(dpath+file)):
            getLines(dpath+file)


directory(path)


with open("lines.txt", 'w') as f:
    f.write(f"path is {path}\n\n")
    for extension in lines.keys():
        f.write(f".{extension} -> {lines[extension]} lines of code.\n")