# CALL SYNTAX: python3 "script name" "filepath1" "filename2"...
# sys.argv[0] is the name of the script
# sys.argv[1:] the filenames

# The "zip" module requires you to use the parent directory and only include filenames for the zips you want to extract

import os, sys, re, subprocess

####################################
# HELP FUNCTIONS
####################################

def get_zip_method_user_input():
    os.system("clear")
    while 1==1:
        userInput = input("PUT FILES:\n(1) In a single zip file [default]\n(2) Each in a separate zip\n").strip()
        os.system("clear")
        if userInput == "1" or userInput == "": return "single"
        elif userInput == "2": return "separate"
        else: print("Invalid input. Try again.")

def get_cust_zip_name_user_input():
    os.system("clear")
    while 1==1:
        userInput = input("NAME OF ZIP FILE:\n").strip()
        os.system("clear")
        if userInput == "": print("Can't have an empty name. Try again.")
        elif re.match(r"^.*(\\|\/|:|\*|\?|\"|<|>|\|).*$", userInput): print("\/:*?\"<>| not allowed. Try again.")
        else: return userInput

def get_dupe_action_user_input():
    os.system("clear")
    while 1==1:
        userInput = input("DUPLICATE ZIP/s FOUND. ACTION TO TAKE:\n(1) Skip [default]\n(2) Rename\n(3) Replace\n").strip()
        os.system("clear")
        if userInput == "1" or userInput == "": return "skip"
        elif userInput == "2": return "rename"
        elif userInput == "3": return "replace"
        else: print("Invalid input. Try again.")

def get_unused_zip_name(zipNameWoExt, baseDir):
    counter = 1
    while 1==1:
        newZipNameWoExt = f"{zipNameWoExt} ({counter})"
        if not os.path.exists(f"{baseDir}/{newZipNameWoExt}.zip"): return newZipNameWoExt
        counter += 1

def get_zip_password_user_input():
    os.system("clear")
    userInput = input("ENTER PASSWORD TO USE (or leave empty)\n").strip()
    os.system("clear")
    return userInput

# when running commands either through os.system or subprocess, it is the equivalent of eval(), so the parameters included are exactly how they're printed
# first, use single quotes instead of double because they don't allow for special characters, escaped characters etc.
# the only thing left to deal with are single quotes within single quotes, so this function does that
def sq(str):
    return str.replace("'", "'\"'\"'")

####################################
# INITIALIZE & PREP
####################################

if len(sys.argv) - 1 <= 0: input("Not enough arguments provided. Press Enter to exit."); quit()

baseDir = None
zipMethod = "single" if len(sys.argv[1:]) == 1 else get_zip_method_user_input()
custZipNameWoExt = get_cust_zip_name_user_input() if zipMethod == "single" and len(sys.argv[1:]) > 1 else None
dupeAction = None
zipsDict = {} # zip1.zip: '"file1" "file2"...'

for filePath in sys.argv[1:]:
    if filePath.endswith("/"): filePath = filePath[:-1]
    if not os.path.exists(filePath): continue

    if not baseDir:
        baseDir = os.path.dirname(filePath)
        if not os.access(baseDir, os.W_OK): input("Write permission missing. Press Enter to exit."); quit()
        if not os.access(baseDir, os.R_OK): input("Read permission missing. Press Enter to exit."); quit()

    if os.path.dirname(filePath) != baseDir: input("Files provided have different parent folders. Press Enter to exit."); quit()

    zipNameWoExt = None
    if zipMethod == "single" and len(sys.argv[1:]) > 1: zipNameWoExt = custZipNameWoExt
    else: zipNameWoExt = os.path.basename(filePath)

    if os.path.exists(f"{baseDir}/{zipNameWoExt}.zip"):
        if not dupeAction: dupeAction = get_dupe_action_user_input()
        if dupeAction == "skip": continue
        elif dupeAction == "rename": zipNameWoExt = get_unused_zip_name(zipNameWoExt, baseDir)
        elif dupeAction == "replace": os.system(f"rm '{sq(baseDir)}/{sq(zipNameWoExt)}.zip' > /dev/null 2>&1")

    if f"{zipNameWoExt}.zip" not in zipsDict: zipsDict[f"{zipNameWoExt}.zip"] = ""
    zipsDict[f"{zipNameWoExt}.zip"] += f"'{sq(os.path.basename(filePath))}' "

password = get_zip_password_user_input()

####################################
# ZIP
####################################

os.chdir(baseDir)
errors = ""
zipFileCounter = 1
for zipName in zipsDict:
    os.system("clear")
    if zipMethod == "single":
        print(f"Adding files to {zipName}")
    else:
        sys.stdout.write(f"\x1b]2;Zip {zipFileCounter}/{len(zipsDict)}\x07") # changes terminal title
        print(f"Zip {zipFileCounter}/{len(zipsDict)}")

    print(f"Adding files to {zipName}") if zipMethod == "single" else print(f"Working on zip file {zipFileCounter}/{len(zipsDict)}")
    cmdToRun = "zip -q -r "
    if password: cmdToRun += f"--password '{sq(password)}' "
    cmdToRun += f"'{sq(zipName)}' {zipsDict[zipName].strip()}"
    cmdOutput = subprocess.run(cmdToRun, shell=True, text=True, capture_output=True)
    if cmdOutput.stdout.strip(): errors += f"{zipName}:\n{commandOutput.stdout}\n\n" # for some reason zip outputs errors in stdout instead of stderr
    zipFileCounter += 1

if errors:
    os.system("clear")
    print(errors)
    input("PRESS ENTER TO EXIT")

