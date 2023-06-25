# CALL SYNTAX: python3 "script name" "dir structure" "filepath1" "filepath2"...
# sys.argv[0] is the name of the script
# sys.argv[1] the dir structure: "inner"/"outer"
# sys.argv[2:] the filepaths

# Unar is used to handle everything except ".rar" files. Unrar handles ".rar" files exclusevly
# Extracted files are put inside of a temporary folder, and then moved (skip, rename, replace)
# Min versions: Unrar v6.11+ and unar v1.10.7+

import os, sys, re, subprocess

FILE_PATHS_ARR = []
BASE_DIR = ""
TEMP_PATH = ""
PASSWORD = "test"
BLOCK_PASS_POPUPS = False
DUPE_ACTION = None
ERRORS = ""

def run():
    init()
    extract()
    finish()

####################################
# INITIALIZE
####################################

def init():
    global FILE_PATHS_ARR, BASE_DIR, TEMP_PATH

    if len(sys.argv) - 2 <= 0: input("Not enough arguments provided. Press Enter to exit."); quit()
    if sys.argv[1] != "inner" and sys.argv[1] != "outer": input("The dir structure argument is wrong. Press Enter to exit."); quit()

    for filePath in sys.argv[2:]:
        if filePath.endswith("/"): filePath = filePath[:-1]
        if not os.path.exists(filePath): continue
        # unrar automatically finds the other parts - if other parts are not removed, it would extraxt the same thing however many times over
        if re.match(r"(?i)^.+\.part[0-9]+\.rar$", filePath) and not re.match(r"(?i)^.+\.part(1|01|001)\.rar$", filePath): continue
        FILE_PATHS_ARR.append(filePath)

    BASE_DIR = os.path.dirname(FILE_PATHS_ARR[0])

    if not os.access(BASE_DIR, os.W_OK): input("Write permission missing. Press Enter to exit."); quit()
    if not os.access(BASE_DIR, os.R_OK): input("Read permission missing. Press Enter to exit."); quit()

    TEMP_PATH = f"{BASE_DIR}/.tempExtract"
    if os.path.exists(TEMP_PATH): TEMP_PATH = get_unused_item_path(TEMP_PATH)
    os.makedirs(TEMP_PATH)

####################################
# PERFORM EXTRACTION
####################################

def extract():
    global ERRORS
    
    counter = 1
    for filePath in FILE_PATHS_ARR:
        while 1==1:
            if not os.path.exists(filePath): ERRORS += f"{os.path.basename(filePath)}:\nFile removed before extraction began\n\n"; continue
            os.system("clear")
            empty_temp()
            
            sys.stdout.write(f"\x1b]2;Extr {counter}/{len(FILE_PATHS_ARR)}\x07") # changes terminal title
            print(f"Extr {counter}/{len(FILE_PATHS_ARR)}")

            extractCmdOutput = subprocess.run(generate_extract_command(filePath), shell=True, text=True, capture_output=True)
            errMsg = extractCmdOutput.stderr.strip()

            if errMsg:
                empty_temp()
                if "password" in errMsg.split("\n")[0].lower():
                    if not BLOCK_PASS_POPUPS and password_user_input(filePath) == "password changed": continue
                    errMsg = "Wrong password. Archive skipped."
                ERRORS += f"{os.path.basename(filePath)}:\n{errMsg}\n\n"

            move_files_from_temp(TEMP_PATH, os.path.basename(filePath))
            break

        counter += 1

    rm_temp()

#-----------------------------------
# HELPERS

def empty_temp():
    os.system(f"rm -r '{sq(TEMP_PATH)}/'* > /dev/null 2>&1")
    
def rm_temp():
    os.system(f"rm -r '{sq(TEMP_PATH)}' > /dev/null 2>&1")

def generate_extract_command(filePath):
    if re.match(r"(?i)^.+\.rar$", filePath):
        outputDir = ""
        if sys.argv[1] == "outer": # with unrar you implement extract to seperate folder by specifying the folder (no flag for this)
            folderName = re.sub(r"(?i)(?:\.part[0-9]+)?\.rar$", "", os.path.basename(filePath)) # replace optional .part# and .rar with nothing
            outputDir = f"{TEMP_PATH}/{folderName}"
        else:
            outputDir = TEMP_PATH
        return f"unrar x -op'{sq(outputDir)}' -p'{sq(PASSWORD)}' '{sq(filePath)}' > /dev/null" # unrar doesnt have a quite mode (I just need errors)
    else:
        outputDir = TEMP_PATH
        dirStructureFlag = "-force-directory" if sys.argv[1] == "outer" else "-no-directory"
        return f"unar -quiet -output-directory '{sq(outputDir)}' {dirStructureFlag} -password '{sq(PASSWORD)}' '{sq(filePath)}'"

def password_user_input(filePath):
    global PASSWORD, BLOCK_PASS_POPUPS
    
    os.system("clear")
    while 1==1:
        userInput = input(f"PASSWORD NEEDED FOR \"{os.path.basename(filePath)}\"\n(1) Enter password [default]\n(2) Skip archive\n(3) Skip all remaining\n").strip()
        os.system("clear")
        if not re.match(r"^[123]$", userInput) and userInput != "": print("*** Invalid input. Try again."); continue

        if userInput == "1" or userInput == "":
            pswEnteredByUser = input("ENTER PASSWORD TO USE:\n").strip()
            if pswEnteredByUser != "": PASSWORD = pswEnteredByUser
            return "password changed"
        elif userInput == "3": BLOCK_PASS_POPUPS = True
        break

# start with TEMP_PATH
def move_files_from_temp(dir, archiveName):
    global ERRORS
    
    for tempItemName in os.listdir(dir):
        tempItemPath = f"{dir}/{tempItemName}"
        if os.path.isdir(tempItemPath):
            move_files_from_temp(tempItemPath, archiveName)
        else:
            newItemPath = tempItemPath.replace(f"/{os.path.basename(TEMP_PATH)}", "")
            try:
                if os.path.exists(newItemPath):
                    if not DUPE_ACTION: dupe_action_user_input()
                    if DUPE_ACTION == "skip": continue
                    elif DUPE_ACTION == "rename": newItemPath = get_unused_item_path(newItemPath)
                    elif DUPE_ACTION == "overwrite": os.remove(newItemPath)
                os.makedirs(os.path.dirname(newItemPath), exist_ok=True)
                os.rename(tempItemPath, newItemPath)
            except:
                ERRORS += f"{archiveName}:\nPartially or not extracted at all, due to missing permissions moving\n{tempItemPath}\n\n"
                

def dupe_action_user_input():
    global DUPE_ACTION
    os.system("clear")
    while 1==1:
        userInput = input("DUPLICATES FOUND (this will apply to future duplicates):\n(1) Skip [default]\n(2) Rename\n(3) Overwrite\n").strip()
        os.system("clear")
        if not re.match(r"^[123]$", userInput) and userInput != "": print("*** Invalid input. Try again."); continue
        if userInput == "1" or userInput == "": DUPE_ACTION = "skip"
        elif userInput == "2": DUPE_ACTION = "rename"
        elif userInput == "3": DUPE_ACTION = "overwrite"
        break

####################################
# FINISH
####################################

def finish():
    if not ERRORS: quit()
    os.system("clear")
    print(ERRORS)
    input("Press ENTER to close")

####################################
# GENERAL HELPERS
####################################

def get_unused_item_path(itemPath):
    name = os.path.basename(itemPath)
    nameWoExt = re.sub(r"\.[a-zA-Z]{3,4}$", "", name)
    ext = name.replace(nameWoExt, "")
    counter = 1
    while 1==1:
        newItemPath = f"{os.path.dirname(itemPath)}/{nameWoExt} ({counter}){ext}"
        if not os.path.exists(newItemPath): return newItemPath
        counter += 1
    
# when running commands either through os.system or subprocess, it is the equivalent of eval(), so the parameters included are exactly how they're printed
# first, use single quotes instead of double because they don't allow for special characters, escaped characters etc.
# the only thing left to deal with are single quotes within single quotes, so this function does that
def sq(str):
    return str.replace("'", "'\"'\"'")


run()

