import os, sys, re

FILE_PATHS_ARR = []

def run():
    init()
    fix()
    input("PRESS ENTER TO CLOSE")

def init():
    global FILE_PATHS_ARR
    
    if len(sys.argv) <= 1: input("No zip files specified, try again."); quit()
    fileErrors = ""
    for filePath in sys.argv[1:]:
        if filePath.endswith("/"): filePath = filePath[:-1]
        if os.path.isfile(filePath) and re.match(r"(?i)^.+\.zip$", filePath): FILE_PATHS_ARR.append(filePath)
        else: fileErrors += f"Not a valid zip file:\n{filePath}\n\n"
    if fileErrors:
        print(fileErrors)
        input("Press ENTER to continue")
    if len(FILE_PATHS_ARR) == 0: quit()

def fix():
    os.system("clear")
    for zipPath in FILE_PATHS_ARR:
        print(f"\n******************************\nWORKING ON:\n{zipPath}\n******************************\n")
        os.chdir(os.path.dirname(zipPath))
        # zip -FF fm-25-06.zip --out New.zip
        os.system(f"zip -FF '{sq(zipPath)}' --out '{sq(get_fixed_zip_name(zipPath))}'")
        
def sq(str):
    return str.replace("'", "'\"'\"'")
    
def get_fixed_zip_name(zipPath):
    zipNameWoExt = re.sub(r"(?i)\.zip$", "", os.path.basename(zipPath))
    return f"{zipNameWoExt} (FIXED).zip"
    
run()
