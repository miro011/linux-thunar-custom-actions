# sys.argv[0] is the name of the script
# sys.argv[1] is the starting folder

# characters that need replacing: <>:"/\|?*
# replace with: < => (l) , > => (g) , : => (c) , " => (d) , / => (f) , \ => (b) , | => (p) , ? => (q) , * => (a)

import sys, os, re

######################################

START_PATH = ""

######################################

def run():
    init()
    recrsv_fix_invalid_chars(START_PATH)
    input("OPERATION COMPLETE, PRESS ENTER TO CLOSE")

######################################
    
def init():
    global START_PATH
    if len(sys.argv) != 2: input("Invalid number of arguments. Try again."); quit()
    if not os.path.isdir(sys.argv[1]): input("Invalid source directory argument. Try again."); quit()
    START_PATH = sys.argv[1]
    if START_PATH.endswith("/"): START_PATH = START_PATH[:-1]
    
    print("*** WARNING, this will recursivly rename files that contains invalid NTFS chars !!!\n")
    print(f"*** STARTING FOLDER:\n{START_PATH}\n")
    input("Press ENTER to start")

######################################

def recrsv_fix_invalid_chars(pdir):
    for itemName in os.listdir(pdir):

        fullPath = f"{pdir}/{itemName}"

        if not os.path.islink(fullPath) and os.path.isdir(fullPath):
            recrsv_fix_invalid_chars(fullPath)

        if contains_invalid_chars(itemName):
            rename_item(pdir, itemName, fullPath)


def get_fixed_name(itemName):
    itemName = itemName.replace("<", "(l)")
    itemName = itemName.replace(">", "(g)")
    itemName = itemName.replace(":", "(c)")
    itemName = itemName.replace("\"", "(d)")
    itemName = itemName.replace("/", "(f)")
    itemName = itemName.replace("\\", "(b)")
    itemName = itemName.replace("|", "(p)")
    itemName = itemName.replace("?", "(q)")
    itemName = itemName.replace("*", "(a)")
    return itemName


def contains_invalid_chars(itemName):
    return True if re.match(r".*[<>:\"\/\\\|\?\*].*$", itemName) else False


def rename_item(pdir, itemName, fullPath):
    newFullPath = f"{pdir}/{get_fixed_name(itemName)}"
    try: os.rename(fullPath, newFullPath)
    except: print(f"FAILED: {fullPath}")

######################################

run()
