import re
from builder import *

#this opens the file and makes it into an array of lines that gets returned
def parse_file(filename):
    with open(filename, 'r') as fp:
        return fp.readlines()

def getele(elems, string):
    if type(elems) is list:
        for ele in elems:
            if ele.tag == string:
                return ele
    else:
        return None


def timematch(start, end):
    time = [(make_ele(start, "start_date_time", None)),make_ele(end, "stop_date_time", None)]
    return time

#def timematch2(arr):
#    for line in arr:
#        m = re.match ('^time (.*) (.*)',line, re.IGNORECASE)
#        if m:
#            time = [(make_ele(m.group(1), "start_date_time", None)),make_ele(m.group(2), "stop_date_time", None)]


def process(arr_line):
    #this is what we return in the end, it is a list of elems as defined in the builder class
    elems = []
    primary_res = []

#for each line in the file, we match it to a specific regex, and then insert it into the elems
#list, as elem objects, so that they can be easily turned into xml files, 
#commented into different sections. each of the match statements can be read to see
#what input format is.
    for line in arr_line:
        line.rstrip()
        
        #comments
        m = re.match ('^#.*', line)
        if m:
            pass
            continue

#########################
#time math


        #remember group 0 is entire matched group 1 is first group
        m = re.match ('^time (.*) (.*)',line, re.IGNORECASE)
        if m: 
            time = timematch(m.group(1), m.group(2))
            elems.append(make_ele("","Time_Coordinates", time))
            continue

################################################
#Primary Results Summary

        m = re.match('^(?:purpose) (.*)', line, re.IGNORECASE)
        if m:
            perp = make_ele(m.group(1), "Purpose", None)
            elems.append(make_ele("", "Primary_Result_Summary", perp))
            continue

        m = re.match('^processing_level (.*)', line, re.IGNORECASE)
        if m:
            for ele in elems:
                if ele.tag == "Primary_Result_Summary":
                    sub = [ele.ele,make_ele(m.group(1), "processing_level", None)]
                    ele.set_ele(sub)
            continue

        m = re.match('science_facets (.*)', line, re.IGNORECASE)
        #facets will just be in a big line I guess
        if m: 
            fac = []
            lst = m.group(1)
            lst = [x.strip() for x in lst.split(',')]#should be in form tag text, ...
            for each in lst:
                #print(each)
                r = re.match('([^\s]*) (.*)', each)
                #print(r)
                fac.append(make_ele(r.group(2), r.group(1), None))
            for ele in elems:
                if ele.tag == "Primary_Result_Summary":
                    sub = ele.ele
                    sub.append(make_ele("", "Science_Facets", fac))
                    ele.set_ele(sub)
            continue




###########################################
#Investigation Area


        invest = []
        m = re.match('^name (.*)', line, re.IGNORECASE)
        if m:
            invest.append(make_ele(m.group(1), "name", None))
            inv = make_ele("", "Investigation_Area", invest)
            elems.append(inv)
            continue


        m = re.match('^type (.*)', line, re.IGNORECASE)
        if m:
            for ele in elems:
                if ele.tag == "Investigation_Area":
                    ele.ele.append(make_ele(m.group(1), "Type", None))
            continue

        refs = []
        m = re.match ('^lid_reference (.*)', line, re.IGNORECASE)
        if m:
            refs.append(make_ele(m.group(1), "Lid_Reference", None))
            investigation = getele(elems, "Investigation_Area")
            investigation.ele.append(make_ele("", "Internal_Reference", refs))
            continue


        m = re.match('^reference_types? (.*)', line, re.IGNORECASE)
        if m:
            investigation = getele(elems, "Investigation_Area")
            intref = getele(investigation.ele, "Internal_Reference")
            intref.ele.append(make_ele(m.group(1), "Reference_Types", None))
            continue

#############################
#this is observing system components and target id which are fairly mature at this time
#only need a little bit of work to more or less fully flesh them out.

        m = re.match('^Observing_System_Components name (\w*) (type (.*)) lid_reference (.*) reference_type (.*)', line, re.IGNORECASE)
        if m:
            types = m.group(3).split("type")
            obs_sys_comp =[(make_ele(m.group(1), "Name", None))]
            for x in types:
                obs_sys_comp.append(make_ele(x, "Type", None))
            types = []
            types.append(make_ele(m.group(4), "Lid_Reference", None))
            types.append(make_ele(m.group(5), "Reference_Type", None))
            obs_sys_comp.append(make_ele("", "Internal_Reference", types))
            if getele(elems, "Observing_System") is None:
                elems.append(make_ele("", "Observing_System",[(make_ele("", "Observing_System_Components", obs_sys_comp))]))
            else:
                obssys = getele(elems, "Observing_System")
                obssys.ele.append(make_ele("","Observing_System_Components", obs_sys_comp))
            continue
            #object?

####################
#target identification

        m = re.match ('^Target_Identification name (\w*) (type (.*))', line, re.IGNORECASE)
            #multiple
        if m:
            types = m.group(3).split("type")
            
            targ_id =[(make_ele(m.group(1), "Name", None))]
            for x in types:
                targ_id.append(make_ele(x, "Type", None))
            elems.append(make_ele("", "Target_Identification", targ_id))
            continue

        #this is a general case, where if there are 2 words it will add it to the end.
        #this is not 
#        m = re.match('(\w+) (\w+)', line, re.IGNORECASE)
#        if m:
#            gen = make_ele(m.group(1), m.group(2), None)
#            elems.append(gen)
    return elems


#print(process(parse_file("./inputs")))
#print(parse_file("./inputs"))

def testinput(arr):
    #want to take our input file and conver it useing builder.py into an xml file
    counter = 0
    for filename in arr:
        #this counts,for each file in the array, it processes it, creates an file name, and
        #outputs them as "output#.xml" where # is a number.
        counter = counter + 1
        #process the files into element objects
        a = process(parse_file(filename))
        #makes these element objects into python xml tree
        res = context_builder(a)
        #indent/format the tree
        indent(res)
        #transform it from a collection of elements into a tree
        tree = ET.ElementTree(res)
        #and then writing the tree into a file 
        output = "output" + str(counter) + ".xml"
        tree.write(output)

def getinput():
    var = input("enter the filenames, comma separated:")
    #takes the string of filenames, strips the whitespace and splits by comma
    arr = [x.strip() for x in var.split(',')]
    testinput(arr)

if __name__ == "__main__":
    getinput()
