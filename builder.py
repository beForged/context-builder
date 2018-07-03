import xml.etree.ElementTree as ET
import random
import sys

    #a class that contains a parent, a tag, and text id 
class ele:
    def __init__(self, text, parent, tag, ele):
       self.text = text 
       self.parent = parent # if we make this a list..
       self.tag = tag
       if ele is None:
           self.ele = None
       else:
            self.ele = ele

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


#list of elems
def context_builder(elems):
    root = ET.Element('Context_area')
    for elem in elems:
        helper(root, elem) 

def helper(root, element):
    sub = ET.SubElement(root, element.tag)
    if element.test is not None:
        sub.text = element.text
    if element.ele is not None:
        for subele in element.ele:
            helper(sub, subele)

#returns time element that consists of start and stop and sometimes the other two
#~can maybe control after, and before, so far they are going to be random times
def time_element():
    num = random.randint(2,5)
    time_titles = ['start_date_time','stop_date_time', 'local_mean_solar_time',
            'local_true_solar_time', 'solar_longitude']
    times = []
    for each in num:
        times.append(ele(time(), 'Context_Area', time_titles[each], None))
    time = ele(None, 'Context_area', 'Time_Coordinates', times)
    return time


def time():
    year = random.randint(1900, 2030)
    month = random.randint(1,12)
    day = random.randint(1,30)
    #missing time HH:MM:SSSS
    date = str(year) + "-" + str(month + "-" + str(day) + "Z"
    return date
    
def timemath():
    import time

return 

def primary_results(facets):
    purposes = ['Calibration', 'Checkout', 'Engineering', 'Navigation', 'Observation Geometry', 'Science']
    processing_level = ['Calibrated', 'Derived', 'Partially Processed', 
        'Raw', 'Telemetry']
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
        wavelengths = ['Far Infrared', 'Gamma Ray', 'Infrared', 'Microwave', 'Millimeter', 'Near Infrared', 'Radio'. 'Submillimeter', 'Ultraviolet', 'Visible', 'X-ray']
        domains = ['Atmosphere','Heliosphere', 'Interior', 'Interstellar', 'Ionosphere', 'Magnetosphere', 'Surface']
        discipline_name = ['Atmospheres', 'Fields', 'Flux Measurements', 'Imaging', 'Particles', 'Ring-Moon Systems', 'Small Bodies', 'Spectroscopy']
    prim = ele(None, 'Context_Area', PrimRes , subs)

