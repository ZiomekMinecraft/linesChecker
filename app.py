import time
import os
import yaml

if not os.path.exists("./config.yml"):
    with open("./config.yml", "w") as f:
        f.write("path: null\nlastPath: null\nwhite-list: null\nblack-list: null")

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
    except:
        pass

def directory(dpath: str):
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