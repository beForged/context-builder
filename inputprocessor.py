import re
from builder import *
#might need to be import regex as re oops
def parse_file(filename):
    with open(filename, 'r') as fp:
        return fp.readlines()

def process(arr_line):
    elems = []
    targ_name = []
    targ_type = []
    obs_name = []
    obs_type = []

    for line in arr_line:
        line.rstrip()
        #remember group 0 is entire matched group 1 is first group
        m = re.match('^(?:purpose) (.*)', line)
        if m:
            elems.append(make_ele(m.group(1), "Purpose", None))

        m = re.match('^processing_level (.*)', line)
        if m:
            elems.append(make_ele(m.group(1), "Processing_level", None))

        m = re.match('^name (.*)', line)
        if m:
            elems.append(make_ele(m.group(1), "Name", None))

        m = re.match('^type (.*)', line)
        if m:
            elems.append(make_ele(m.group(1), "Type", None))

        m = re.match ('^lid_reference (.*)', line)
        if m:
            elems.append(make_ele(m.group(1), "Lid_Reference", None))

        m = re.match('^reference_types (.*)', line)
        if m:
            elems.append(make_ele(m.group(1), "Reference_Types", None))

        m = re.match('^observing_system_components name (.*) type (.*)', line)
        if m:
            obs_sys_comp =[(make_ele(m.group(1), "Name", None)), make_ele(m.group(2), "Type", None)]
            elems.append(make_ele("", "Observing_System_Componenets", obs_sys_comp))
            #object?

        m = re.match ('^Target_Identification name (.*) type (.*)', line)
            #multiple
        if m:
            targ_id =[(make_ele(m.group(1), "Name", None)), make_ele(m.group(2), "Type", None)]
            elems.append(make_ele("", "Target_Identification", targ_id))
    return elems


#print(process(parse_file("./inputs")))
#print(parse_file("./inputs"))

def testinput(arr):
    #want to take our input file and conver it useing builder.py into an xml file
    counter = 0
    for filename in arr:
        counter = counter + 1
        a = process(parse_file(filename))
        res = context_builder(a)
        indent(res)
        tree = ET.ElementTree(res)
        output = "output" + str(counter) + ".xml"
        tree.write(output)

def getinput():
    var = input("enter the filenames, comma separated:")
    arr = [x.strip() for x in var.split(',')]
    testinput(arr)

getinput()
