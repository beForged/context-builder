import xml.etree.ElementTree as ET
import random
import sys
from datetime import timedelta
from datetime import datetime

    #a class that contains a parent, a tag, and text id 
class Ele:
    #these defaults are probably not needed other than ele
    text = "default"
    tag = "no tag yet"
    ele = None
    #defined/initalized with a text, and a tag and none for child elements
    def __init__(self, text, tag, elem):
       self.text = text 
       self.tag = tag
       #child elements defined, can be a list of childs
       if elem is None:
           self.ele = None
       else:
            self.ele = elem
       
       #set the child elements, this rewrites, 
       #function
    def set_ele(self, ele):
        self.ele = ele

#appends elements, does not rewrite, but if it is none, then it will add one
    def add_ele(self, elem):
        if ele is None:
            self.ele = elem
        else:
            self.ele.append(elem)

#helper to make elements, can call this func
#instead of doing whatever strange constructer python has
#clarity sake
def make_ele(text, tag, ele):
    ele = Ele(text, tag, ele)
    return ele

#indents xml objects, cant be given tree, give it the root element object
#https://norwied.wordpress.com/2013/08/27/307/
def indent(elem, level=0):
  i = "\n" + level*"   "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "   "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

#list of elems
#recursivly generates sml based on a list of elems defined above
def context_builder(elems):
    root = ET.Element('Context_area')
    for elem in elems:
        helper(root, elem) 
    return root

def helper(root, element):
    sub = ET.SubElement(root, element.tag)
    if element.text is not None:
        sub.text = element.text
    if element.ele is not None:
        for subele in element.ele:
            helper(sub, subele)

#returns time element that consists of start and stop and sometimes the other two
#~can maybe control after, and before, so far they are going to be random times
#probably never to be used
def time_element():
    num = random.randint(2,5)
    time_titles = ['start_date_time','stop_date_time', 'local_mean_solar_time',
            'local_true_solar_time', 'solar_longitude']
    times = []
    for each in num:
        times.append(ele(time(), 'Context_Area', time_titles[each], None))
    time = ele(None, 'Context_area', 'Time_Coordinates', times)
    return time

#attempt to define a random time generator
def time():
    year = random.randint(1900, 2030)
    month = random.randint(1,12)
    day = random.randint(1,28)
    #missing time HH:MM:SSSS
    date = datetime(year, month, day)
    delta = timedelta(seconds = random.randint(200, 86399))
    start = date + abs(delta)
    end = start + abs(timedelta(seconds = random.randint(200, 50000)))
    return timeret(start) + " " + timeret(end)

def timeret(date):
    ret = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return ret
    
    

#this is probably a useless function, but the list of items are left here for future reference
def primary_results(facets):
    purposes = ['Calibration', 'Checkout', 'Engineering', 'Navigation', 'Observation Geometry', 'Science']
    processing_level = ['Calibrated', 'Derived', 'Partially Processed', 'Raw', 'Telemetry']
    #facets ~
    subs = []
    PrimRes = 'Primary_Result_Summary'
    subs.append(ele(random.choice(purposes), PrimRes, 'Purpose',
        None))
    subs.append(ele(random.choice(processing_level), PrimRes, 'processing_level',
        None))
    #adding facets
    if facets is not None:
        #can add filtering, so for example not all have a domain or whatever
        wavelengths = ['Far Infrared', 'Gamma Ray', 'Infrared', 'Microwave', 'Millimeter', 'Near Infrared', 'Radio', 'Submillimeter', 'Ultraviolet', 'Visible', 'X-ray']
        domains = ['Atmosphere','Heliosphere', 'Interior', 'Interstellar', 'Ionosphere', 'Magnetosphere', 'Surface']
        discipline_name = ['Atmospheres', 'Fields', 'Flux Measurements', 'Imaging', 'Particles', 'Ring-Moon Systems', 'Small Bodies', 'Spectroscopy']
    prim = ele(None, 'Context_Area', PrimRes , subs)

