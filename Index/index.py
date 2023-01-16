import sys, os, re
from datetime import datetime

FONT_DF = '\033[0m'
FONT_BOLD = '\033[1m'
FONT_GR = '\033[92m'
FONT_RD = '\033[91m'

START_DIR = ""
INDEX_CONFIG = ""
OUTPUT = []
ERRORS = []

INDEX_PARAMS_MSG = f"""{FONT_BOLD}INDEX:       |   INCLUDE HIDDEN FILES?   |   INCLUDE LINKS?{FONT_DF}
[1]ALL       |   [4]yes                  |   [6]yes
[2]folders   |   [5]NO                   |   [7]NO
[3]files     |                           |"""

def run():
    init()
    index_params_user_input()
    print("\nWORKING")
    list_files(START_DIR)
    rm_prev_ln(1)
    write_results_to_file()
    finish()

def init():
    global START_DIR
    if len(sys.argv[1:]) > 1: input("Too many arguments included"); quit()
    if not sys.argv[1]: input("Missing starting folder argument"); quit()
    START_DIR = sys.argv[1]
    if START_DIR.endswith("/"): START_DIR = START_DIR[:-1]
    if not os.path.isdir(START_DIR): input("Starting path is not a valid folder"); quit()
    if not os.access(START_DIR, os.W_OK): input("Write permission missing."); quit()

def index_params_user_input():
    global INDEX_CONFIG
    errOnPrev = False
    print(INDEX_PARAMS_MSG)
    while 1==1:
        userInput = input().strip()
        rm_prev_ln(2) if errOnPrev else rm_prev_ln(1)
        userInput = re.sub(r"[ ]+", "", userInput)
        if userInput != "" and not re.match(r"^[1-5]+", userInput):
            errOnPrev = True
            print(f"{FONT_RD}--- input shall only contain numbers from selection{FONT_DF}")
        elif userInput != "" and re.match(r"^([1-3]{2,}|[4-5]{2,}|[6-7]{2,})$", userInput):
            errOnPrev = True
            print(f"{FONT_RD}--- can't have more than 1 number per cattegory{FONT_DF}")
        else:
            if not re.match(r"^.*[1-3].*$", userInput): userInput += "1"
            if not re.match(r"^.*[4-5].*$", userInput): userInput += "5"
            if not re.match(r"^.*[6-7].*$", userInput): userInput += "7"
            INDEX_CONFIG = "".join(sorted(list(userInput)))
            print(f"{FONT_BOLD}{FONT_GR}{INDEX_CONFIG}{FONT_DF}")
            break

def rm_prev_ln(numLinesToRemove):
    for i in range(numLinesToRemove):
        print("\033[A                                                                              \033[A")

def list_files(dir):
    global OUTPUT, ERRORS
    
    itemNameArr = []
    try: itemNameArr = os.listdir(dir)
    except: ERRORS.append(f"Couldn't list contents, likely a permissions error:\n{dir}\n"); return
    
    for itemName in itemNameArr:
        itemPath = f"{dir}/{itemName}"
        relPath = itemPath.replace(START_DIR, "")
        
        if itemName.startswith(".") and "5" in INDEX_CONFIG: continue # hidden-files-off
        elif os.path.islink(itemPath) and "7" in INDEX_CONFIG: continue # links-off
        elif os.path.isfile(itemPath) and "2" in INDEX_CONFIG: continue # folders-only
        
        if os.path.isdir(itemPath):
            if "3" not in INDEX_CONFIG: OUTPUT.append(relPath)
            list_files(itemPath)
        else:
            OUTPUT.append(relPath)

def write_results_to_file():
    dateAndTimeNow = datetime.now().strftime("%Y-%m-%d at %H-%M-%S")
    indexFilePath = f"{START_DIR}/index-{dateAndTimeNow}.txt"
    fileObj = open(indexFilePath, "w", encoding="utf-8")
    fileObj.write("\n".join(OUTPUT))

def finish():
    if not ERRORS: return
    print("OPERATION COMPLETED WITH ERRORS:\n\n")
    print("\n".join(ERRORS))
    input("PRESS ENTER TO CLOSE")

run()
