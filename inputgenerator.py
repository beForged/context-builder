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
    disc = random.choice(disc_name)
    facet = "wavelength_range " + random.choice(wavelength) + ", dicipline_name " + disc
    if random.uniform(0,1) == 1:
        facet = facet + ", facet1 "  
        if disc == 'Imaging':
            facet = facet + random.choice(["Greyscale", "Color", "Movie", "Color Movie"])
        elif disc == 'fields':
            facet = facet + random.choice(["Electric", "Magnetic"])
        else:
            facet = facet + random.choice(["Lightcurve", "Meteorics", "Physical Properties", "Taxonomy", "Historical Reference"])
    return facet

#returns a string with refernce types, depending on what category it goes in.
def reftype(sec):
    obsref= ["is_airborne", "is_facility", "is_instrument", "is_instrument_host", "is_other", "is_telescope"]
    investref = ["bundle_to_investigation", "collection_to_investigation", "document_to_investigation", "data_to_investigation"]
    if sec == 1:
        return "reference_type " + random.choice(investref)
    else:
        return " reference_type " + random.choice(obsref)

#should actually generate a lid reference sometime TODO i guess
def lidgen():
    return "sample_lid_reference"


#generates a prupose string
def purpose():
    perp = ["Navigation", "Science", "Calibration"]
    return "purpose " + random.choice(perp)

#processing level string generation
def processinglvl():
    lvls = ["Calibrated", "Derived", "Partially Processed", "Raw", "Telemetry"]
    return "processing_level " + random.choice(lvls)

#there are 3 different categories  for type, so this will return something for each
#one of them will randomly return 2 different types, although it needs to be modified so it doesnt repeat
def typegen(sec):
    invest = ["Individual Investigation", "Mission", "Observing Campaign", "Other Investigation"]
    obs = ["Asteroid",  "Comet", "Dust", "Dwarf Planet", "Meteorite", "Meteroid", "Satellite"]
    obssys = ["Airborne", "Aircraft", "Balloon", "Facility", "Instrument", "Laboratory", "Observatory", "Spacecraft", "Telescope"]
    if sec == 1:
        return "type " + random.choice(invest)
    elif sec == 2:
        return " type " + random.choice(obssys)
    else:
        string = " type " + random.choice(obs) 
        if random.uniform(0,1) == 1:
            string + random.choice(obs)
        return string


#just a small function that will make filenames, and also make the loop that will generate files
def defaultgeneration(num, default, name, obs, targ): #number of files you want to generate
    arr = []
    for x in range(0, num):
        filename = "generated-input" + str(x)
        arr.append(filename)
        if default == 1:
            filewriter(filename, x)
        else:
            commandline(filename, x, name, obs, targ) 
    testinput(arr)

#takes in a name, and some numbers to make a more specific input file
def commandline(filename, num, name, observers, targets):
    f = open(filename, "w+")
    f.write("time " + time() + "\n")
    f.write(purpose() + "\n")
    f.write(processinglvl() + "\n")
    f.write("science_facets " + generate_facet() + "\n")
    f.write("name " + name + str(num)+ "\n")
    f.write(typegen(1) + "\n") 
    f.write("lid_reference "+ lidgen() + str(num)+ "\n")
    f.write(reftype(1) + "\n")
    #some number of observers to be made, 
    for x in range(0,observers):
        f.write("Observing_System_Components name spaceship" + str(x) + typegen(2) +" lid_reference " + lidgen() +  reftype(2) + "\n")
        #some number of targets
    for x in range(1,targets):
        f.write("Target_Identification name randomname" + str(x) + typegen(3) + "\n")
    f.close()


#prompts for setting up the more specific input file
def cmdline(num):
    name = input("set a sample name: ")
    observers = int(input("set a number of observers: "))
    targets = int(input("set a number of targets: "))
    defaultgeneration(num,2, name, observers, targets)

#this is just like, make something that we build off of
#default input files.
def filewriter(filename, num):
    f = open(filename, "w+")
    f.write("time " + time() + "\n")
    f.write(purpose() + "\n")
    f.write(processinglvl() + "\n")
    f.write("science_facets " + generate_facet() + "\n")
    f.write("name spaceship" + str(num)+ "\n")
    f.write(typegen(1) + "\n") #choose from a list? input would be good here
    f.write("lid_reference "+ lidgen() + str(num)+ "\n")
    f.write(reftype(1) + "\n")
    for x in range(0,((num % 3) + 1)):
        f.write("Observing_System_Components name spaceship" + str(x) + typegen(2) +" lid_reference " + lidgen() +  reftype(2) + "\n")
    for x in range(1,3):
        f.write("Target_Identification name randomname" + str(x) +  typegen(3) + "\n")
    f.close()

#''main' function, will run this if you run 'python inputgenerator.py'
if __name__ == "__main__":
    num = input("how many files to generate: ")
    default = input("would you like to enter more specific information (y/n):")
    if default == 'y':
        cmdline(int(num))
    else:
        defaultgeneration(int(num), 1, None, None, None)

