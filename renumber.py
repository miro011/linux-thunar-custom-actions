# renumbers files that have already been numbered (works with format 1.txt, 1 blah.txt, 1.1... blah.txt)
# the main purpose is to preserve sub numbers or other text after the original numbers
# sys_argv[1:] are the paths to all the files

import os, sys, re

def run():
    validItemPathsArr = validate_item_paths()
    if len(validItemPathsArr) == 0: return
    
    startingNum = starting_number_user_input()
    curNum = startingNum
    
    for itemPath in validItemPathsArr:
        itemName = os.path.basename(itemPath)
        itemNamePartsArr = itemName.split(".")
        firstPartSpacePartsArr = itemNamePartsArr[0].split(" ")
        if not re.match(r"^\d+$", firstPartSpacePartsArr[0]): continue
        
        firstPartSpacePartsArr[0] = f"{curNum}"
        itemNamePartsArr[0] = " ".join(firstPartSpacePartsArr)
        newItemName = ".".join(itemNamePartsArr)
        newItemPath = f"{os.path.dirname(itemPath)}/{newItemName}"
        
        os.rename(itemPath, newItemPath)
        
        curNum += 1
    
def path_fixer(path):
    if path.endswith("/"): path = path[:-1]
    return path
    
def validate_item_paths():
    outputArr = []
    for itemPath in sys.argv[1:]:
        itemPath = path_fixer(itemPath)
        if not os.path.exists(itemPath): continue
        outputArr.append(itemPath)
    # remove dupes
    outputArr = list(dict.fromkeys(outputArr))
    return outputArr
    
def starting_number_user_input():
    os.system("clear")
    while 1==1:
        usrIn = input("ENTER STARTING NUMBER\n").strip()
        os.system("clear")
        if re.match(r"^\d+$", usrIn): return int(usrIn)
        print("*** Invalid input, try again");

run()
