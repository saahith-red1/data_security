import sys, shutil, os

STORE = "files"  # folder where save everything
HOME = os.path.expanduser("~")  # gets your home directory like /Users/
SEARCH = [os.getcwd(), HOME, HOME+"/Desktop", HOME+"/Downloads", HOME+"/Documents"]  # all places to look for the file

os.makedirs(STORE, exist_ok=True)  # create the files folder

if len(sys.argv) < 2:  # no file was given
    print("python store.py <filepath>")
else:
    path = sys.argv[1]  # grab whatever the user typed after store.py
    # if it's not a direct path to a file, try finding it in common folders
    if not os.path.isfile(path):
        for folder in SEARCH:  # loop through desktop, downloads etc...
            check = os.path.join(folder, path)  
            if os.path.isfile(check):  
                path = check
                break
    else:
        shutil.copy(path, STORE)  # copy the file into our files folder
        name = os.path.basename(path)  # just the filename without the path
        print(f"Stored {name}")
        print(open(os.path.join(STORE, name)).read())  # print out what's in the file
