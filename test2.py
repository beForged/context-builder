import re
#might need to be import regex as re oops
def parse_file(filename):
    with open(filename, 'r') as fp:
        return lines = fp.readlines

def process(arr_line):
    
    for line in arr_line:
        if m = re.match('^purpose (.*)', line):
            purpose = m.group(0)
        else if m = re.match('^processing_level (.*)', line):
            processing_level = m.group(0)
        else if m = re.match('^name (.*)', line):
            name = m.group(0)
        else if m = re.match('^type (.*)', line):
            typ = m.group(0)
        else if m = re.match ('^lid_reference (.*)', line):
            lid_ref = m.group(0)
        else if m = re.match('^reference_types (.*)', line):
            ref_type = m.group(0)
        else if m = re.match('^observing_system_components name (.*) type (.*)', line):
            obs_name = m.group(0)
            obs_type = m.group(1)
            #object?
        else if m = re.match ('^Target_Identification name (.*) type (.*)', line):
            #multiple
            




#time coord, prim results summ, invest area, observing system, targ id
top_level = []
root = ele("", None, 'root', arr)

