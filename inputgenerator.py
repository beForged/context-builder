#we want to build files that can be fed to inputprocessor.py that 
#can then be built into xml.
#we want to keep the files as a middle step to verify the information, but 
#should also have functionality to directly make xml files

from inputprocessor import *
from builder import *


#this is deprecated and unused for now
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
    if wave == None:
        return ""
    
    facet = "science_facets wavelength_range " + wavelength[wave] 
    if disc == None:
        return facet
    disc = disc_name[disc]
    facet = facet + ", discipline_name " + disc
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
#now can take user input
def lidgen(where, what):
    lid = "lid_reference " + "urn:nasa:pds:" + where + ":" + what +":sample"
    return lid


#generates a prupose string
def purpose(t):
    if t < 0:
        raise ValueError
    perp = ["Navigation", "Science", "Calibration"]
    return "purpose " + perp[t%3]

#processing level string generation
#given the number t, it takes what number t is from the list, t is the index.
#to prevent against 
def processinglvl(t):
    if t < 0:
        raise ValueError
    lvls = ["Calibrated", "Derived", "Partially Processed", "Raw", "Telemetry"]
    return "processing_level " + lvls[t%5] 

#there are 3 different categories  for type, so this will return something for each
#one of them will randomly return 2 different types, although it needs to be modified so it doesnt repeat
def typegen(sec, t):
    if t < 0:
        raise ValueError
    invest = ["Individual Investigation", "Mission", "Observing Campaign", "Other Investigation"]
    obs = ["Asteroid",  "Comet", "Dust", "Dwarf Planet", "Meteorite", "Meteroid", "Satellite"]
    obssys = ["Airborne", "Aircraft", "Balloon", "Facility", "Instrument", "Laboratory", "Observatory", "Spacecraft", "Telescope"]
    if sec == 1:
        return "type " + invest[t%4] 
    elif sec == 2:
        return " type " + obssys[t%9]
    else:
        string = " type " + obs[t%7]
        if (t%2)== 1:
            string = string + " " + obs[(t + 1) % 7]
        return string

#generates time string
def timegen():
    string = "time " + time() 
    return string 

#generates a name string
def namegen(name, num):
    string = "name " + name + str(num) 
    return string

#adds a \n to the end of the string
def addret(string):
    return string + "\n"

#generates a observing system component string
def obs(name, num, t, ref):
    if num is None:
        string = "Observing_System_Components name " + name + typegen(2, t) + " " + lidgen("context", "observing") +  reftype(2, ref) 
    else:
        string = "Observing_System_Components name " + name + str(num) + typegen(2, t) + " " + lidgen("context", "observing") +  reftype(2, ref) 
    return string

#generates a target identification string
def target(name, num, t):
    if num is None:
        string = "Target_Identification name " + name + typegen(3, t)
    else:
        string = "Target_Identification name " + name + str(num) + typegen(3, t)
    return string


#just a small function that will make filenames, and also make the loop that will generate files
def defaultgeneration(num, default, name, obs, targ): #number of files you want to generate
    arr = []
    for x in range(0, num):
        filename = "generated-input" + str(x + 1)
        arr.append(filename)
        if default == 1:
            filewriter(filename, x)
        elif default == 2:
            commandline(filename, x, name, obs, targ) 
        elif default == 3:
            specific(filename, x, name, obs, targ)
    testinput(arr)


def specific(filename, num, name, observers, targets):
    time = timegen()
    purp= int(input("input purpose \n 1.Navigation \n2.Science\n3.Calibration\n")) - 1
    proc = int(input("input a processing level\n1.Calibrated\n2.Derived\n3.Partially Processed\n4.Raw\n5.Telemetry\n")) - 1
    facbool = int(input("input number of facets, 0-3\n"))
    wavelength = None
    facoptions = None
    disc = None
    while(facbool > 0):
        wavelength = int(input("input wavelength\n1.Infrared\n2.Microwave\n3.Millimeter\n4.Near Infrared\n5.Radio\n6.Submillimeter\n")) - 1
        if facbool == 1:
            break
        disc = int(input ("input discipline name\n1.Imaging\n2.Fields\n3.Small Bodies\n")) - 1
        if facbool == 2:
            break
        if disc == 0:
            facoptions = int(input("input facet numbers\n1.Greyscale\n2.Color\n3.Movie\n4.Color Movie\n")) - 1
        if disc == 1:
            facoptions = int(input("input facet numbers\n1.Electric\n2.Magnetic\n")) - 1
        if disc == 2:
            facoptions = int(input("input facet numbers\n1.Lightcurve\n2.Meteorics\n3.Physical Properties\n4.Taxonomy\n5.Historical Reference\n")) - 1
        break
    type1 = int(input("input a type from the list\n1.Individual Investigation\n2.Mission\n3.Observing Campaign\n4.Other Investigations\n")) - 1
    lid = input("enter 2 space separated words for the lid reference\n")
    ref1 = int(input("input a number for reference type\n1.bundle_to_investigation\n2.collection_to_investigation\n3.document_to_investigation\n4.data_to_investigation\n")) - 1
    obstype = []
    obsref = []
    obsname = []
    for each in range(0,observers):
        obsname.append(input("input a name"))
        obstype.append(int(input("input a number for type\n1.Airborne\n2.Aircraft\n3.Balloon\n4.Facility\n5.Instrument\n6.Laboratory\n7.Observatory\n8.Spacecraft\n9.Telescope\n")) - 1)
        obsref.append(int(input("input a number for reference\n1.is_airborne\n2.is_facility\n3.is_instrument\n4.is_instrument_host\n5.is_other\n6.is_telescope\n")) - 1)##
    targnames = []
    targtypes = []
    for each in range(0,targets):
        targname.append(input("input target " + str(each) + " name"))
        targtypes.append(int(input("input what types the target is\n1.Asteroid\n2.Comet\n3.Dust\n4.Dwarf Planet\n5.Meteorite\n6.Meteroid\n7.Satellite\n")) - 1)###

    f = open(filename, "w+")
    f.write(addret(time))
    f.write(addret(purpose(purp)))
    f.write(addret(processinglvl(proc)))
    if facbool == 3:
        a = 1
    else: 
        a = 0
    f.write(addret(generate_facet(wavelength,disc, a, facoptions )))#facet
    f.write(addret(typegen(1, type1)))
    lid = lid.split(" ")
    f.write(addret(lidgen(lid[0], lid[1])))
    f.write(addret(reftype(1, ref1)))
    for x in range(0,observers):
        f.write(addret(obs(obsname[x],None, obstype[x], obsref[x])))
    for x in range(0, targets):
        f.write(addret(target(targname[x], None, targtypes[x])))
    f.close()



#takes in a name, and some numbers to make a more specific input file
#random generation of numbers here to just randomly make appropriate strings,
#consideration for non random generation(user prompted) but too long maybe?
def commandline(filename, num, name, observers, targets):
    f = open(filename, "w+")
    f.write(addret(timegen()))
    f.write(addret(purpose(random.randint(0,3))))
    f.write(addret(processinglvl(random.randint(0,5))))
    #5,2,1,4
    f.write(addret(generate_facet(random.randint(0,5), random.randint(0,2), random.randint(0,1), random.randint(0,4))))
    f.write(addret(namegen(name, num)))
    f.write(addret(typegen(1, random.randint(0,10))))
    f.write(addret(lidgen("sbn", "sample" + str(num))))
    f.write(addret(reftype(1, random.randint(0,3))))
    #some number of observers to be made, 
    for x in range(1,observers):
        f.write(addret(obs("sample_obs_name", x, random.randint(0,10), random.randint(0,3))))
        #some number of targets
    for x in range(1,targets):
        f.write(addret(target("sample_target_name", x, random.randint(0,10))))
    f.close()


#prompts for setting up the more specific input file
def cmdline(num):
    name = input("set a sample name: ")
    observers = int(input("set a number of observers: "))
    targets = int(input("set a number of targets: "))
    spec= input("would you like to enter all information manually y/n")
    if spec== "y":
        defaultgeneration(num, 3, name, observers, targets)
    else:
        defaultgeneration(num,2, name, observers, targets)

#default input files.
#this makes a random input file to be turned into a  xml fragment 
def filewriter(filename, num):
    f = open(filename, "w+")
    f.write(addret(timegen()))
    f.write(addret(purpose(random.randint(0,3))))
    f.write(addret(processinglvl(random.randint(0,5))))
    f.write(addret(generate_facet(random.randint(0,5), random.randint(0,2), random.randint(0,1), random.randint(0,4))))
    f.write(addret(namegen("spaceship", num)))
    f.write(addret(typegen(1, random.randint(0,10))))
    f.write(addret(lidgen("sbn", "sample" + str(num))))
    f.write(addret(reftype(1, random.randint(0,3))))
    for x in range(0,((num % 3) + 1)):
        f.write(addret(obs("sample_obs_name", x, random.randint(0,10), random.randint(0,3))))
    for x in range(1,3):
        f.write(addret(target("sample_target_name", x, random.randint(0,10))))
    f.close()

#''main' function, will run this if you run 'python inputgenerator.py'
if __name__ == "__main__":
    num = input("how many files to generate: ")
    default = input("would you like to enter more specific information (y/n):")
    if default == 'y':
        cmdline(int(num))
    else:
        defaultgeneration(int(num), 1, None, None, None)

