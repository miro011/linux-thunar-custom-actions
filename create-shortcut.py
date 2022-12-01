# sys.argv[0] is the name of the script
# sys.argv[1] is the source folder

import os, sys

SOURCE_PATH = ""
DEST_PATH = ""

def run():
    init()
    dest_path_user_input()
    run_rsync_backup()
    
def init():
    global SOURCE_PATH
    if len(sys.argv) != 2: input("Invalid number of arguments. Try again."); quit()
    if not os.path.isdir(sys.argv[1]): input("Invalid source directory argument. Try again."); quit()
    SOURCE_PATH = sys.argv[1]
    if SOURCE_PATH.endswith("/"): SOURCE_PATH = SOURCE_PATH[:-1]
    
    print("*** WARNING, this will clone the source folder to the destination folder !!!\n")
    print(f"*** SOURCE FOLDER:\n{SOURCE_PATH}\n")
    input("Press ENTER to continue")

def dest_path_user_input():
    global DEST_PATH
    
    os.system("clear")
    while 1==1:
        usrInput = input("ENTER DESTINATION PATH:\n").strip()
        os.system("clear")
        
        if usrInput.endswith("/"): usrInput = usrInput[:-1]
        
        if not os.path.isdir(usrInput): print("*** Invalid directory, try again"); continue
        elif SOURCE_PATH in usrInput: print("*** Destination can't be a sub-directory of source, try again."); continue
        elif usrInput in SOURCE_PATH: print("*** Destination can't be a parent directory of source, try again."); continue
        
        while 1==1:
            usrInputConfirm = input(f"DESTINATION YOU ENTERED:\n{usrInput}\n\nARE YOU SURE? (y/n)\n").strip().lower()
            os.system("clear")
            if usrInputConfirm == "y": DEST_PATH = usrInput; return
            elif usrInputConfirm == "n": break
            else: print("*** Invalid response, try again"); continue

def run_rsync_backup():
    os.system("clear")
    print(f"SOURCE:\n{SOURCE_PATH}\n\nDESTINATION:\n{DEST_PATH}\n")
    print("----------------------------\nPERFORMING BACKUP\n----------------------------\n\n")
    # rsync -av --delete "/src/dir/" "/dest/dir/"
    os.system(f"rsync -av --delete \"{SOURCE_PATH}/\" \"{DEST_PATH}/\"")
    print("\n\n----------------------------\nOPERATION COMPLETE\n----------------------------\n")
    input("PRESS ENTER TO EXIT")

run()
