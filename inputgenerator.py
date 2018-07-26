#we want to build files that can be fed to inputprocessor.py that 
#can then be built into xml.
#we want to keep the files as a middle step to verify the information, but 
#should also have functionality to directly make xml files

from inputprocessor import *
from builder import *



def fileinp():
    filename = input("give a filename with seed values: ")
    names = [x.strip() for x in filename.split(',')]
    for f in names:
        arr.append(parse_file(filename))
    return arr
    #arr is a list of a list of file line


    
    #returns a string with wavelength and discipline name fascets, could be expanded easily
def generate_facet():
    wavelength = ['Infrared', 'Microwave', 'Millimeter', 'Near Infrared', 'Radio', 'Submillimeter']
    disc_name = ['Imaging', 'fields', 'Small Bodies']
    return "wavelength_range " + random.choice(wavelength) + ", dicipline_name " + random.choice(disc_name)

def lidgen():
    return "sample_lid_reference"


def purpose():
    perp = ["Navigation", "Science", "Calibration"]
    return "purpose " + random.choice(perp)

def processinglvl():
    lvls = ["Calibrated", "Derived", "Partially Processed", "Raw", "Telemetry"]
    return "processing_level " + random.choice(lvls)

#TODO
def namelater(arr):
    pass
        #we take a line in and 

def defaultgeneration(num, default, name, obs, targ): #number of files you want to generate
    arr = []
    for x in range(0, num):
        filename = "generated-input" + str(x)
        arr.append(filename)
        if default == 1
            filewriter(filename, x)
        else:
            commandline(filename, x, name, obs, targ) 
    testinput(arr)

def commandline(filename, num, name, observers, targets):
    f = open(filename, "w+")
    f.write("time " + time() + "\n")
    f.write(purpose() + "\n")
    f.write(processinglvl() + "\n")
    f.write("science_facets " + generate_facet() + "\n")
    f.write("name " + name + str(num)+ "\n")
    f.write("type mission\n") #choose from a list? input would be good here
    f.write("lid_reference urn:nasa:pds:context:investigation:mission" + str(num)+ "\n")
    f.write("reference_types collection_to_investigation\n")
    for x in range(0,observers):
        f.write("Observing_System_Components name spaceship" + str(x) + " type observer " +"lid_reference" + lidgen() +  "reference_type is_something" + "\n")
    for x in range(1,targets):
        f.write("Target_Identification name randomname" + str(x) + " type comet" + "\n")
    f.close()


def cmdline():
    num = int(input("how many files in the collection"))
    name = input("set a sample name")
    observers = int(input("set a number of observers"))
    targets = int(input("set a number of targets"))
    commandline(name, observers, targets)

#this is just like, make something that we build off of
#default input files.
def filewriter(filename, num):
    f = open(filename, "w+")
    f.write("time " + time() + "\n")
    f.write(purpose() + "\n")
    f.write(processinglvl() + "\n")
    f.write("science_facets " + generate_facet() + "\n")
    f.write("name spaceship" + str(num)+ "\n")
    f.write("type mission\n") #choose from a list? input would be good here
    f.write("lid_reference urn:nasa:pds:context:investigation:mission" + str(num)+ "\n")
    f.write("reference_types collection_to_investigation\n")
    for x in range(0,((num % 3) + 1)):
        f.write("Observing_System_Components name spaceship" + str(x) + " type observer " +"lid_reference" + lidgen() +  "reference_type is_something" + "\n")
    for x in range(1,3):
        f.write("Target_Identification name randomname" + str(x) + " type comet" + "\n")
    f.close()

if __name__ == "__main__":
    num = input("how many files to generate: ")
    defaultgeneration(int(num), 1, None, None, None)

