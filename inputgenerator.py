#we want to build files that can be fed to inputprocessor.py that 
#can then be built into xml.
#we want to keep the files as a middle step to verify the information, but 
#should also have functionality to directly make xml files

from inputprocessor import *

def cmdline():
    names = input("give a comma separated list of names: ")
    names = [x.strip() for x in names.split(',')]


def fileinp():
    filename = input("give a filename with seed values: ")
    names = [x.strip() for x in filename.split(',')]
    for f in names:
        arr.append(parse_file(filename))

    #arr is a list of a list of file line
    for f in arr:

