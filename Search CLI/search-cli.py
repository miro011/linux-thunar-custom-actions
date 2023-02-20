# CALL SYNTAX: python3 "path/to/script.py" "folder/to/search/dir"

import os, sys, re, subprocess, shutil

###########################################################
# GLOBALS

#......................................................... 
# COLORS

FONT_PR = '\033[95m'
FONT_BU = '\033[94m'
FONT_CY = '\033[96m'
FONT_GR = '\033[92m'
FONT_OR = '\033[38;5;95;38;5;214m'
FONT_YE = '\033[33m'
FONT_RD = '\033[91m'
FONT_DF = '\033[0m'
FONT_BOLD = '\033[1m'
FONT_UL = '\033[4m'

RESULTS_COLORS_DICT = {"d":FONT_OR, "dl":FONT_YE, "f":FONT_BU, "fl":FONT_CY}

#.........................................................
# MESSAGES

SEARCH_MSG = f"{FONT_BOLD}{FONT_UL}SEARCH{FONT_DF} (/[d|f][s|e][c][n] searchText) (/h for help)"

RESULTS_MSG = f"\n{FONT_BOLD}{FONT_UL}RESULTS{FONT_DF} {RESULTS_COLORS_DICT['d']}dir {RESULTS_COLORS_DICT['dl']}dir-link {RESULTS_COLORS_DICT['f']}file {RESULTS_COLORS_DICT['fl']}file-link{FONT_DF}"

SELECTION_MSG = f"\n{FONT_BOLD}{FONT_UL}SELECT{FONT_DF} (r || d|o|s nums || c|m[s|r|o] nums /out) (/out=>/rr=relroot, [s|r|o]=>r=df)"

#.........................................................
# REGEX

SEARCH_WITH_ARGS_REGEX = r"^\/[sedfcn]+ .+$"
COPY_MOVE_REGEX = r"^[cm](?:[sro])? (?:(([0-9]+ )|([0-9]+-[0-9]+ ))+)?(([0-9]+)|([0-9]+-[0-9]+)) \/.+$"
DELETE_SHOW_OPEN_REGEX = r"^[dso] (?:(([0-9]+ )|([0-9]+-[0-9]+ ))+)?(([0-9]+)|([0-9]+-[0-9]+))$"

#.........................................................
# DYNAMIC

START_DIR = ""

SEARCH_TEXT = ""
SEARCH_ARGS = ""

SEARCH_RESULTS_ARR = []

ACTION = ""
SELECTED_INDEXES_ARR = []
OUTPUT_DIR = ""
ERRORS = ""

###########################################################

def run():
    global START_DIR

    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        input("Invalid parameters")
        quit()

    START_DIR = sys.argv[1]
    if START_DIR.endswith("/"):
        START_DIR = START_DIR[:-1]

    search_text_uin()

###########################################################

def search_text_uin(prevSearchNoResults=False, usePrevInput=False):
    global SEARCH_TEXT, SEARCH_ARGS

    os.system("clear")

    if (prevSearchNoResults):
        print(f"{FONT_RD}Nothing found, try again{FONT_DF}\n")

    print(SEARCH_MSG)

    if (usePrevInput):
        print(f"{FONT_PR}INPUT:{FONT_DF} {SEARCH_ARGS} {SEARCH_TEXT}")
        search_results()

    while True:
        SEARCH_TEXT = ""; SEARCH_ARGS = ""

        userInput = input(f"{FONT_PR}INPUT:{FONT_DF}")

        if userInput == "/h":
            show_help_msg()
            continue

        if userInput == "":
            print(f"{FONT_RD}Invalid input, try again.{FONT_DF}")
            continue

        if re.match(SEARCH_WITH_ARGS_REGEX, userInput):
            SEARCH_ARGS = userInput.split(" ")[0]
            SEARCH_TEXT = " ".join(userInput.split(" ")[1:])
        else:
            SEARCH_TEXT = userInput

        if "/" in SEARCH_TEXT:
            print(f"{FONT_RD}Search text can't include forward slash, try again.{FONT_DF}")
            continue

        break
        
    search_results()

def show_help_msg():
    msg = f"{FONT_BOLD}SEARCH PARAMS{FONT_DF}\n"
    msg += "Preceeded by forward-slash at the begining, followed by space and the search string\n"
    msg += "/[d|f][s|e][c][n][h] searchText\n"
    msg += "d = search only directories, f = search only files (df: any)\n"
    msg += "s = starts with, e = ends with (df: contains)\n"
    msg += "c = case-sensitive (df: insensitive)\n"
    msg += "n = non-recursive (df: recursive)\n\n"

    msg += f"{FONT_BOLD}SELECT{FONT_DF}\n"
    msg += "FORMAT1: r\n"
    msg += "r = restart\n"
    msg += "FORMAT2: d|o|s nums\n"
    msg += "d = delete, o = open, s = show in thunar\n"
    msg += "FORMAT3: c|m[s|r|o] nums /out\n"
    msg += "c = copy, m = move\n"
    msg += "s = skip, r = rename (df), o = overwrite\n"
    msg += "if can use /rr in the output directory to refer to refer to the folder in which you're searching\n"
    msg += "NOTE: The numbers you select need to be seperated by space if multiple. Ranges are allowed too (ex. 1 3-6 9)"

    os.system(f"mate-terminal --name 'thunar' --title 'SEARCH INSTRUCTIONS' -- sh -c 'printf \"{sq(msg)}\"; echo \"\"; echo \"\"; read -p \"PRESS ENTER TO CLOSE\" hold;' > /dev/null 2>&1")

###########################################################

def search_results():
    global SEARCH_RESULTS_ARR

    print(RESULTS_MSG)

    #input(generate_find_command())
    result = subprocess.getoutput(generate_find_command())
    if result == "":
        search_text_uin(True)
        return

    counter = 1

    SEARCH_RESULTS_ARR = []

    for path in result.split("\n"):
        relPath = path.replace(START_DIR, "")
        fontColorCode = RESULTS_COLORS_DICT[get_path_type(path)]

        print(f"[{counter}]{fontColorCode}{relPath}{FONT_DF}")
        SEARCH_RESULTS_ARR.append(path)
        counter += 1

    select_and_action()

#.........................................................

def generate_find_command():
    formattedSearchText = sq(SEARCH_TEXT).replace("*", "\*") # escpate single quotes and stars

    cmd = f"find '{sq(START_DIR)}' -mindepth 1 " # -mindepth 1 excludes the dir you're searching from the results

    if "n" in SEARCH_ARGS: cmd += "-maxdepth 1 "

    if "d" in SEARCH_ARGS: cmd += "-type d "
    elif "f" in SEARCH_ARGS: cmd += "-type f "

    if "c" in SEARCH_ARGS: cmd += "-name "
    else: cmd += "-iname "

    cmd += "'"
    if "s" not in SEARCH_ARGS: cmd += "*"
    cmd += formattedSearchText
    if "e" not in SEARCH_ARGS: cmd += "*"
    cmd += "'"

    return cmd

def get_path_type(path):
    pathType = ""

    if os.path.isdir(path):
        pathType += "d"
    else:
        pathType += "f"

    if os.path.islink(path):
        pathType += "l"

    return pathType

###########################################################

def select_and_action():
    global ACTION, SELECTED_INDEXES_ARR, OUTPUT_DIR, ERRORS

    print(SELECTION_MSG)
    
    while 1==1:
        ACTION = ""; SELECTED_INDEXES_ARR = ""; OUTPUT_DIR = ""; ERRORS = ""

        userInput = input(f"{FONT_PR}INPUT:{FONT_DF}").strip()

        if userInput == "r":
            search_text_uin()
            return

        # validate / seperate user input
        if re.match(COPY_MOVE_REGEX, userInput):
            OUTPUT_DIR = re.search(r" \/.+", userInput).group()
            selectedItems = re.search(r"[0-9].*", userInput.replace(OUTPUT_DIR, "")).group()
            OUTPUT_DIR = OUTPUT_DIR.strip()

            if OUTPUT_DIR.startswith("/rr"):
                OUTPUT_DIR = OUTPUT_DIR.replace("/rr", START_DIR, 1)

            if not os.path.isdir(OUTPUT_DIR):
                print(f"{FONT_RD}Invalid output directory, try again.{FONT_DF}")
                continue
        elif re.match(DELETE_SHOW_OPEN_REGEX, userInput):
            selectedItems = re.search(r"[0-9].*", userInput).group()
        else:
            print(f"{FONT_RD}Invalid input format, try again.{FONT_DF}")
            continue

        SELECTED_INDEXES_ARR = item_selection_uin_to_indexes(selectedItems)
        if not SELECTED_INDEXES_ARR:
            print(f"{FONT_RD}Invalid items selected, try again.{FONT_DF}")
            continue

        ACTION = userInput.split(" ")[0]
        if re.match(r"^[cm]$", ACTION):
            ACTION += "r" # add the default duplucate action if non provided

        # perform action
        for i in SELECTED_INDEXES_ARR:
            if ACTION == "d":
                if os.path.isdir(SEARCH_RESULTS_ARR[i]) and not os.path.islink(SEARCH_RESULTS_ARR[i]):
                    try: shutil.rmtree(SEARCH_RESULTS_ARR[i])
                    except: ERRORS += f"ERROR deleting - {SEARCH_RESULTS_ARR[i]}\n\n"
                else:
                    try: os.remove(SEARCH_RESULTS_ARR[i])
                    except: ERRORS += f"ERROR deleting - {SEARCH_RESULTS_ARR[i]}\n\n"
            elif re.match(r"^[cm]", ACTION):
                recurse_move_or_copy(SEARCH_RESULTS_ARR[i], os.path.dirname(SEARCH_RESULTS_ARR[i]))
            elif ACTION == "o":
                os.system(f"nohup xdg-open '{sq(SEARCH_RESULTS_ARR[i])}' 1>/dev/null 2>&1")
            elif ACTION == "s":
                os.system(f"thunar '{sq(SEARCH_RESULTS_ARR[i])}'")

        if ERRORS:
            os.system(f"mate-terminal --name 'thunar' --title 'ERRORS' -- sh -c 'printf \"{sq(ERRORS)}\"; read -p \"PRESS ENTER TO CLOSE\" hold;' > /dev/null 2>&1")

        # either repeat loop (open and show), or repeat search with delete/move/copy
        if re.match(r"^[cmd]", ACTION):
            search_text_uin(False, True)
            
#.........................................................

# converts the user input into an array of proper INDEXES, and ranges are converted to single numbers as well
def item_selection_uin_to_indexes(selectedItems):
    arr = []
    for num in selectedItems.split(" "):
        if "-" in num:
            splitArr = num.split("-")
            num1 = int(splitArr[0]) - 1
            num2 = int(splitArr[1]) # no -1 needed here as range() below doesn't include the max
            
            if num2 <= num1:
                return []

            for i in range(num1, num2):
                if i >= len(SEARCH_RESULTS_ARR):
                    return []
                arr.append(i)
        else:
            num = int(num) - 1 # the numbers shown beside files are +1 the actual index in the array

            if num >= len(SEARCH_RESULTS_ARR):
                return []
                
            arr.append(num)

    arr = list(dict.fromkeys(arr))
    arr.sort()

    return arr

def recurse_move_or_copy(path, firstPathParent):
    global ERRORS

    if os.path.isdir(path) and not os.path.islink(path):
        for itemName in os.listdir(path):
            recurse_move_or_copy(f"{path}/{itemName}", firstPathParent)

        if ACTION.startswith("m"):
            try: os.rmdir(path)
            except: ERRORS += f"ERROR removing dir that should be empty during move.\n{path}\nThis happens if there was an error with one or more of the files in it.\n\n"
    
    else:
        relPath = path.replace(firstPathParent, "")
        if relPath.startswith("/"):
            relPath = relPath[1:]
        newPath = f"{OUTPUT_DIR}/{relPath}"

        if os.path.exists(newPath):
            newPath = duplicate_handler(newPath)
            if not newPath: return

        os.makedirs(os.path.dirname(newPath), exist_ok=True)
        
        if ACTION.startswith("m"):
            try: os.rename(path, newPath)
            except: ERRORS += f"ERROR moving {path}\n\n"
        elif ACTION.startswith("c"):
            try: shutil.copy(path, newPath)
            except: ERRORS += f"ERROR copying {path} to {newPath}\n\n"

# returns False with skip, newPath with overwrite (after removing the old one), altered newPath with rename
def duplicate_handler(newPath):
    global ERRORS

    if ACTION.endswith("s"):
        return False
    elif ACTION.endswith("r"):
        return get_unused_item_path(newPath)
    elif ACTION.endswith("o"):
        try:
            os.remove(newPath)
            return newPath
        except:
            ERRORS += f"ERROR removing for overwrite: {newPath}\n\n"
            return False

def get_unused_item_path(itemPath):
    name = os.path.basename(itemPath)
    nameWoExt = re.sub(r"\.[a-zA-Z0-9]{3,4}$", "", name)
    ext = name.replace(nameWoExt, "")

    counter = 1
    while 1==1:
        newItemPath = f"{os.path.dirname(itemPath)}/{nameWoExt} ({counter}){ext}"
        if not os.path.exists(newItemPath):
            return newItemPath
        counter += 1

###########################################################

# when running commands either through os.system or subprocess, it is the equivalent of eval(), so the parameters included are exactly how they're printed
# first, use single quotes instead of double because they don't allow for special characters, escaped characters etc.
# the only thing left to deal with are single quotes within single quotes, so this function does that
def sq(str):
    return str.replace("'", "'\"'\"'")

###########################################################

run()
