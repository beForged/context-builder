#want to build a base context view 
import xml.etree.ElementTree as ET
import sys
from lxml import etree

tree = ET.parse('base-context.xml')
root = tree.getroot()
#time_dict = {'start':'2010','end':'2014'}#these can be made from 
#sample_dict = {'purpose':"agagagag",'abcd':"asfdasf"}
#do the time things
#root[0].find('start_date_time').text = time_dict['start']
#root[0].find('stop_date_time').text = time_dict['end']

#primary results summary
#primary_res = root[1]#this object is a subelement
#given some dict/hash of name->text
#for elem in sample_dict.keys():
#    if primary_res.find(elem) is None:
#        ET.SubElement(primary_res,elem)
#    primary_res.find(elem).text = sample_dict[elem]
#    print(sample_dict[elem])

#tree.write(sys.stdout, "unicode")

#https://norwied.wordpress.com/2013/08/27/307/
def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

#test out the create function 
def test():
    time_dict = {'start_date_time':'2014','stop_date_time':'2015'}
    prime_dict = {'purpose':'science','processing_level':'somewhat', 'test':'does this work?'}
    investig_dict = {'name':'abc','type':'type is thing', 'lid_reference':'ab-34-cf-16', 
            'reference_type':'collectiones', 'additional_obj': 'hopefully this works'}
    obs_dict = [{'name':'gondola','type':'balloon'},{'name':'enterprise','type':'spooceship'}]
    targ_dict = [{'name':'spooceship','type':'comet'},{'name':'achilles','type':'asteroid'}]
    name = "abc.xml"
    create_context_area(time_dict, prime_dict, investig_dict, obs_dict, targ_dict, name)

#given some dicts, this will generate a file that consists of an xml that is just the context area

#time and prime and investig are dicts that consist of the element name as key and its text as value
#obs dict should actually be an array of dicts, where each dict has element name as key and text as val
#as well as targ dict
def create_context_area(time_dict, prime_dict, investig_dict, obs_dict, targ_dict, name):
    #this creates a sample xml doc, just to build off of.
    #it consists of all of the required tags and thats it
    tree = ET.parse('base-context.xml')
    #get the root <context_area> as an Element object
    root = tree.getroot()
    #this section takes the base and assigns subelements as callable objects for manipulation
    #later, we delete observing system and target id so that we can build a bunch later without
    #weird numberting things
    time = root[0]
    primary_res = root[1]
    invest_area = root[2]
    obs_sys = root[3]#expansion
    obs = obs_sys[0]
    targ_id = root[4 ]#expansion
    #we remove observing system and target identification
    obs_sys.remove(obs)
    root.remove(targ_id)
    #set out subelements to start out with, we can add more of some of them later
    #could have an array of dicts. and order by number/index

    #these are basically the same just for different ones, 
    #for each element name, in the dictionary, which are the keys it looks for it
    for elem in time_dict.keys():
        if time.find(elem) is None:
            #if there is no element that coresspoinds, it makes a new subelement
            ET.SubElement(time,elem)
            #text is always assigned(i believe this is mandatoty
        time.find(elem).text = time_dict[elem]
        #it is possible to add attributes as well, but the dict does not supportit, would 
        #probably have to move to tuples/3-ples

    #same as the one above
    for elem in prime_dict.keys():
        if primary_res.find(elem) is None:
            ET.SubElement(primary_res,elem)
        primary_res.find(elem).text = prime_dict[elem]
    
    #need another layer of nesting here
    for elem in investig_dict.keys():
        #we get subelement of the investigation area
        int_ref = invest_area[2]
        #so if we get a lid ref or ref type, then it goes under int ref, down another level
        #i believe that this is the only way to go down another level,so hipefully we dont need
        #to automate that
        if elem == 'lid_reference' or elem == 'reference_type':
            #should probably be another is None if statement here
            if int_ref.find(elem) is None:
                ET.SubElement(int_ref, elem)
            int_ref.find(elem).text = investig_dict[elem]
        else:
            if invest_area.find(elem) is None:
                ET.SubElement(invest_area,elem)
            invest_area.find(elem).text = investig_dict[elem]



    #for each entry in obs, we make a new subelement, of type observing system and 
    #we assign it the relevant information in the dicts.
    for dictionary in obs_dict:
        #because this is a 2 deep thing, where we make a new observing system and there is 
        #another inner element that name and type go uinder, may need to make this one longer 
        #if there are tags outside of the inner one, observing system component
        o = ET.SubElement(obs_sys, obs.tag)
        #we pick out the dict and create a subelement in root, with as ab 
        for elem in dictionary.keys():
            if o.find(elem) is None:
                ET.SubElement(o, elem)
            o.find(elem).text = dictionary[elem]
    #need to do the same thing for target id
    for dictionary in targ_dict:
        t = ET.SubElement(root, targ_id.tag)
        for elem in dictionary.keys():
            if t.find(elem) is None:
                ET.SubElement(t, elem)
            t.find(elem).text = dictionary[elem]
#    tree.write(name) #this is unformatted
    indent(root)
    tree = ET.ElementTree(root)
    tree.write(name)


test()
