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
    #0-5, 0-2, 0-1, 0-4
def generate_facet(wave, disc, facet1, option):
    if (wave > 5 or disc > 2 or facet1 > 1):
        raise ValueError 
    if wave < 0 or disc < 0 or facet1 < 0 or option < 0:
        raise ValueError
    wavelength = ['Infrared', 'Microwave', 'Millimeter', 'Near Infrared', 'Radio', 'Submillimeter']
    disc_name = ['Imaging', 'fields', 'Small Bodies']
    imaging = ["Greyscale", "Color", "Movie", "Color Movie"]
    fields = ["Electric", "Magnetic"]
    section = ["Lightcurve", "Meteorics", "Physical Properties", "Taxonomy", "Historical Reference"]

    disc = disc_name[disc]
    facet = "wavelength_range " + wavelength[wave] + ", discipline_name " + disc
    if facet1 == 1:
        facet = facet + ", facet1 "  
        if disc == 'Imaging':
            facet = facet + imaging[option % 4]
        elif disc == 'fields':
            facet = facet + fields[option % 2]
        else:
            if option > 4: 
                raise ValueError 
            facet = facet + section[option]
    return facet

#returns a string with refernce types, depending on what category it goes in.
#let t be a number which corresponds to the index of the array
def reftype(sec, t):
    investref = ["bundle_to_investigation", "collection_to_investigation", "document_to_investigation", "data_to_investigation"]
    obsref= ["is_airborne", "is_facility", "is_instrument", "is_instrument_host", "is_other", "is_telescope"]
    if sec == 1:
        if t > 3 or t < 0:
            raise ValueError("bad number given")  
        return "reference_type " + investref[t]
    else:
        if t > 5 or t < 0:
            raise ValueError("bad number given")
        return " reference_type " + obsref[t]

#should actually generate a lid reference sometime TODO i guess
def lidgen(where, what):
    lid = "urn:nasa:pds:" + where + ":" + what +":sample"
    return lid


#generates a prupose string
def purpose(t):
    if t < 0:
        raise ValueError
    perp = ["Navigation", "Science", "Calibration"]
    return "purpose " + perp[t%3]

#processing level string generation
def processinglvl(t):
    if t < 0:
        raise ValueError
    lvls = ["Calibrated", "Derived", "Partially Processed", "Raw", "Telemetry"]
    return "processing_level " + lvls[t%5]

#there are 3 different categories  for type, so this will return something for each
#one of them will randomly return 2 different types, although it needs to be modified so it doesnt repeat
def typegen(sec, t):
    invest = ["Individual Investigation", "Mission", "Observing Campaign", "Other Investigation"]
    obs = ["Asteroid",  "Comet", "Dust", "Dwarf Planet", "Meteorite", "Meteroid", "Satellite"]
    obssys = ["Airborne", "Aircraft", "Balloon", "Facility", "Instrument", "Laboratory", "Observatory", "Spacecraft", "Telescope"]
    if sec == 1:
        return "type " + invest[t%4]
    elif sec == 2:
        return " type " + obssys[t%7]
    else:
        string = " type " + obs[t%9]
        if t%2== 1:
            string + obs[(t + 1) % 9]
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
    #5,2,1,4
    f.write("science_facets " + generate_facet(random.randint(0,5), random.randint(0,2), random.randint(0,1), random.randint(0,4)) + "\n")
    f.write("name " + name + str(num)+ "\n")
    f.write(typegen(1) + "\n") 
    f.write("lid_reference "+ lidgen("sbn", "sample" + str(num)) + "\n")
    f.write(reftype(1, random.randint(0,3)) + "\n")
    #some number of observers to be made, 
    for x in range(0,observers):
        f.write("Observing_System_Components name spaceship" + str(x) + typegen(2) +" lid_reference " + lidgen("context", "observing") +  reftype(2, random.randint(0,3)) + "\n")
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
    f.write("science_facets " + generate_facet(random.randint(0,5), random.randint(0,2), random.randint(0,1), random.randint(0,4)) + "\n")
    f.write("name spaceship" + str(num)+ "\n")
    f.write(typegen(1) + "\n") #choose from a list? input would be good here
    f.write("lid_reference "+ lidgen("sbn", "sample" + str(num)) + str(num)+ "\n")
    f.write(reftype(1) + "\n")
    for x in range(0,((num % 3) + 1)):
        f.write("Observing_System_Components name spaceship" + str(x) + typegen(2) +" lid_reference " + lidgen("context", "observing") +  reftype(2) + "\n")
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

