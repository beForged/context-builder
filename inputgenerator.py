#we want to build files that can be fed to inputprocessor.py that 
#can then be built into xml.
#we want to keep the files as a middle step to verify the information, but 
#should also have functionality to directly make xml files

from inputprocessor import *
from builder import time

def cmdline():
    names = input("give a comma separated list of names: ")
    names = [x.strip() for x in names.split(',')]


def fileinp():
    filename = input("give a filename with seed values: ")
    names = [x.strip() for x in filename.split(',')]
    for f in names:
        arr.append(parse_file(filename))
    return arr
    #arr is a list of a list of file line
    

def namelater(arr):
    for line in arr:
        #we take a line in and 
       line = line.strip()
       m = re.match('name (.*)' , line) 
       if m:
            a = m.group(1)
            name = [x.strip() for x in a.split(' ')]
        m = re.match('type (.*)', line)
        if m:
            a = m.group(1)
            types = [x.strip() for x in a.split(' ')]
        m = re.match('time (.*)', line)
        if m:
            a = m.group(1)
            types = [x.strip() for x in a.split(' ')]

def defaultgeneration(num): #number of files you want to generate
    for x in range(0, num):
        filename = "generated-input" + str(x)
        filewriter(filename, x)

def filewriter(filename, num):
    f = open(filename, "w+")
    f.write("time " + time())
    f.write("purpose Science")
    f.write("processing_level Partially Processed")
    f.write
    f.close()

