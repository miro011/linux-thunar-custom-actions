# This script renames the files in each folder (starting from whatever folder was provided) to whatever the name of the folder is + a number.
# The original order of the files will be preserved

# sys.argv[0] is the name of the script
# sys.argv[1] should be the temp directory

import os, sys, re

ERRORS = ""

# files are renamed twice - once using temporary names (so that no conflicts later), then using the "real" name.
# The list below is used to determine which word to use for the temporary names (word-num)
# Later it will be tested whether any of the files in a given folder start with any of these words, and whichever doesn't have any matches will be the one used
TEMP_NAME_LEADING_WORDS = ["temp", "interim", "brief", "momentary", "transient", "passing", "abc123", "abczyx", "blah", "random", "gf894d9j45"]


def run():
    global ERRORS
    
    # Init
    if len(sys.argv) != 2: input("Script called invalid number of arguments, try again."); quit()
    startDir = sys.argv[1]
    if startDir.endswith("/"): startDir = startDir[:-1]
    if not os.path.exists(startDir): input("Directory doesn't exist, try again"); quit()
    if not os.path.isdir(startDir): input("Directory given is not a folder, try again"); quit()

    input(f"!!!WARNING!!!\n\nEvery file will be recursively renamed.\nNew filename will be that of the folder, followed by a number.\n\nSTARTING FOLDER:\n{startDir}\n\nPRESS ENTER TO BEGIN")

    recurse_rename(startDir)

    if not ERRORS: quit()
    os.system("clear")
    print("OPERATION COMPLETED WITH ERRORS\n")
    print(ERRORS)
    input("Press ENTER to close")

def recurse_rename(folderPath):
    global ERRORS

    if not os.access(folderPath, os.R_OK) or not os.access(folderPath, os.W_OK):
        ERRORS += f"{folderPath}\nERROR WITH FOLDER - no write/read permission\n\n"
        return

    for itemName in os.listdir(folderPath):
        itemPath = f"{folderPath}/{itemName}"
        if os.path.isdir(itemPath):
            recurse_rename(itemPath)

    rename_files_in_folder(folderPath)


def rename_files_in_folder(folderPath):
    global ERRORS

    # sorted file names
    fileNamesArr = get_sorted_filename_list(folderPath)
    
    if len(fileNamesArr) == 0:
        return

    # figure out temp leading word
    tempNameLeadingWord = get_temp_name_leading_word(fileNamesArr)
    if not tempNameLeadingWord:
        ERRORS += f"{folderPath}\nERROR RENAMING FILES IN FOLDER - couldn't come up with a temp name\n\n"
        return

    # perform temp rename
    tempRenameResult = rename_files(folderPath, fileNamesArr, tempNameLeadingWord)
    if tempRenameResult != "success":
        ERRORS += tempRenameResult
        return

    # Regen sorted file names, as they just changed
    fileNamesArr = get_sorted_filename_list(folderPath)

    # Perform actual rename
    realRenameResult = rename_files(folderPath, fileNamesArr, os.path.basename(folderPath))
    if realRenameResult != "success":
        ERRORS += tempRenameResult

def get_sorted_filename_list(folderPath):
    fileNamesArr = []
    for itemName in os.listdir(folderPath):
        itemPath = f"{folderPath}/{itemName}"
        if not os.path.isdir(itemPath):
            fileNamesArr.append(itemName)
    return natural_sort(fileNamesArr)

def get_temp_name_leading_word(fileNamesArr):
    tempNameLeadingWord = None

    for i in range(len(TEMP_NAME_LEADING_WORDS)):
        tempNameLeadingWordWorks = True

        for fileName in fileNamesArr:
            if fileName.startswith(TEMP_NAME_LEADING_WORDS[i]):
                tempNameLeadingWordWorks = False
                break

        if tempNameLeadingWordWorks:
            tempNameLeadingWord = TEMP_NAME_LEADING_WORDS[i]
            break

    return tempNameLeadingWord


# returns "success" if everything was renamed properly, error message if not
def rename_files(folderPath, fileNamesArr, newNameLeadingText):
    allRenamed = True
    maxNumDigits = len(f"{len(fileNamesArr)}")
    counter = 1

    for fileName in fileNamesArr:
        filePath = f"{folderPath}/{fileName}"
        fileExt = "." + fileName.split(".").pop() if re.match(r"^.+\.[a-zA-Z]{3,4}$", fileName) else ""
        filePathNew = f"{folderPath}/{newNameLeadingText} - {get_adjusted_num(counter, maxNumDigits)}{fileExt}"

        try: os.rename(filePath, filePathNew)
        except: allRenamed = False

        counter += 1

    if not allRenamed:
        return f"{folderPath}\nERROR RENAMING FILES IN FOLDER - error trying to rename files\n\n"

    return "success"

#############################################################

# [a1, a10, a2] => [a1, a2, a10]
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

# 1 => 01 if maxNum is two-digits // 1 => 001 if maxNum is three-digits etc.
def get_adjusted_num(curNum, maxNumDigits):
    curNumStr = f"{curNum}"
    for i in range(maxNumDigits - len(curNumStr)):
        curNumStr = "0" + curNumStr
    return curNumStr


run()