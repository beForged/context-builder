import re
#might need to be import regex as re oops
def parse_file(filename):
    with open(filename, 'r') as fp:
        return fp.readlines()

def process(arr_line):

    for line in arr_line:
        line.rstrip()
        m = re.match('^(?:purpose) (.*)', line)
        if m:
            purpose = m.group(0)
        m = re.match('^processing_level (.*)', line)
        if m:
            processing_level = m.group(0)

        m = re.match('^name (.*)', line)
        if m:
            name = m.group(0)

        m = re.match('^type (.*)', line)
        if m:
            typ = m.group(0)

        m = re.match ('^lid_reference (.*)', line)
        if m:
            lid_ref = m.group(0)

        m = re.match('^reference_types (.*)', line)
        if m:
            ref_type = m.group(0)

        m = re.match('^observing_system_components name (.*) type (.*)', line)
        if m:
            obs_name = m.group(0)
            obs_type = m.group(1)
            #object?

        m = re.match ('^Target_Identification name (.*) type (.*)', line)
            #multiple
        if m:
            targ_name = m.group(0)
            targ_type = m.group(0)
    print(locals())

process(parse_file("./inputs"))
#print(parse_file("./inputs"))


#time coord, prim results summ, invest area, observing system, targ id
#top_level = []
#root = ele("", None, 'root', arr)

