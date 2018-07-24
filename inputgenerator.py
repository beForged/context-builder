#we want to build files that can be fed to inputprocessor.py that 
#can then be built into xml.
#we want to keep the files as a middle step to verify the information, but 
#should also have functionality to directly make xml files

from inputprocessor import *
from builder import *

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
    
def generate_facet():
    wavelength = ['Infrared', 'Microwave', 'Millimeter', 'Near Infrared', 'Radio', 'Submillimeter']
    disc_name = ['Imaging', 'fields', 'Small Bodies']
    return "wavelength_range " + random.choice(wavelength) + " dicipline_name " + random.choice(disc_name)

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

#this is just like, make something that we build off of
#default input files.
def filewriter(filename, num):
    f = open(filename, "w+")
    f.write("time " + time() + "\n")
    f.write("purpose Science\n")
    f.write("processing_level Partially Processed\n")
    f.write("science_facets " + generate_facet() + "\n")
    f.write("name spaceship" + str(num)+ "\n")
    f.write("type mission\n") #choose from a list? input would be good here
    f.write("lid_reference urn:nasa:pds:context:investigation:mission" + str(num)+ "\n")
    f.write("reference_types collection_to_investigation\n")
    for x in range(1..((num % 3) + 1)):
        f.write("Observing_System_Components name \n")
    f.close()

