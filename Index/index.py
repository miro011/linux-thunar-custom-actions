# you can put extra things in text files that start with "index-static". For ex: files that don't exist but you want them included in the index anyway
# any file or folder that starts with "noindex" will not be indexed (if it's a folder, this means everything in it too)

import sys, os, re, subprocess
from datetime import datetime

FONT_DF = '\033[0m'
FONT_BOLD = '\033[1m'
FONT_UL = '\033[4m'
FONT_RD = '\033[91m'
FONT_PR = '\033[95m'

def run():
    # Init
    if len(sys.argv) != 2: input("Invalid arguments"); quit()
    startDir = sys.argv[1]
    if startDir.endswith("/"): startDir = startDir[:-1]
    if not os.path.isdir(startDir): input("Starting path is not a valid folder"); quit()
    if not os.access(startDir, os.W_OK): input("Write permission missing."); quit()

    # Get parameters user input
    print(f"{FONT_BOLD}{FONT_UL}OPTIONS{FONT_DF} help | [df][h][l]")
    userInput = None
    while True:
        userInput = input(f"{FONT_PR}INPUT:{FONT_DF}").strip().lower()
        userInput = re.sub(r"[ ]+", "", userInput)

        if userInput == "help":
            show_help_msg()
            continue

        if "d" in userInput and "f" in userInput:
            userInput = re.sub(r"[df]", "", userInput) # if the user has both d and f, it means they are searching for anything, so remove it

        if userInput != "" and not re.match(r"^[dfhl]+$", userInput):
            print(f"{FONT_RD}Invalid input, try again.{FONT_DF}")
            continue

        break

    # Generate find command
    findCmd = f"find '{sq(startDir)}' -mindepth 1 " # -mindepth 1 excludes the dir you're searching from the results
    if "d" in userInput: findCmd += "-type d "
    elif "f" in userInput: findCmd += "-type f "
    if "h" not in userInput: findCmd += "! -name '.*' " # don't show hidden files unless specified
    if "l" not in userInput: findCmd += "! -type l " # don't show links unless specified
    findCmd += "-printf \"%P\\n\" | sort" # -printf "%P\n" is to get rel path

    # Perform search and write to file
    ymdHms = datetime.now().strftime("%Y-%m-%d at %H-%M-%S")
    indexFilePath = f"{startDir}/index-{ymdHms}.txt"
    fileObj = open(indexFilePath, "w", encoding="utf-8")
    fileObj.write(subprocess.getoutput(findCmd))

def show_help_msg():
    msg = f"{FONT_BOLD}OPTIONS{FONT_DF}\n"
    msg += "Not providing an option means the default will be used\n"
    msg += "It makes no difference whether you use space or not with multiple options\n"
    msg += "[df][h][l]\n"
    msg += "d = list only directories, f = list only files (default: any)\n"
    msg += "h = list hidden files (default: hidden files not listed)\n"
    msg += "l = list lniks (default: links not listed)\n"
    msg += "n = non-recursive (df: recursive)\n\n"

    os.system(f"mate-terminal --name 'thunar' --title 'SEARCH INSTRUCTIONS' -- sh -c 'printf \"{sq(msg)}\"; echo \"\"; echo \"\"; read -p \"PRESS ENTER TO CLOSE\" hold;' > /dev/null 2>&1")


# when running commands either through os.system or subprocess, it is the equivalent of eval(), so the parameters included are exactly how they're printed
# first, use single quotes instead of double because they don't allow for special characters, escaped characters etc.
# the only thing left to deal with are single quotes within single quotes, so this function does that
def sq(str):
    return str.replace("'", "'\"'\"'")

run()