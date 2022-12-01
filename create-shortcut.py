# Creates shortcuts to the selected file/s
# Syntact python3 "script name" "filepath1" "filepath2"...

# sys.argv[0] is the name of the script
# sys.argv[1:] the filepaths

#########################################################

import os, sys

#########################################################
ERRORS = ""

def run():
    global ERRORS
    for filePath in sys.argv[1:]:
        if not os.path.exists(filePath): ERRORS += f"Invalid path:\n{filePath}\n\n"; continue
        parentFolder = os.path.dirname(filePath)
        if not os.access(parentFolder, os.W_OK): ERRORS += f"No write permission to:\n{parentFolder}\n\n"; break
        shortcutPath = get_unused_path(f"{filePath} - Shortcut")
        os.system(f"ln -s '{sq(filePath)}' '{sq(shortcutPath)}' > /dev/null 2>&1")
    if ERRORS:
        os.system(f"mate-terminal --name 'thunar' --title 'CREATE SHORTCUT ERRORS' -- sh -c 'printf \"{sq(ERRORS)}\"; read -p \"PRESS ENTER TO CLOSE\" hold;' > /dev/null 2>&1")
        
# given the path of a file/folder, it returns one that doesn't exist (numbered if original one exists)
def get_unused_path(filePath):
    if not os.path.exists(filePath): return filePath
    counter = 1
    while 1==1:
        newFilePath = f"{filePath} ({counter})"
        if not os.path.exists(newFilePath): return newFilePath
        counter += 1

def sq(str):
    return str.replace("'", "'\"'\"'")

run()
