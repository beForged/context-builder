from lxml import etree
from io import StringIO
from lxml.etree import fromstring
import sys

filename_xml = sys.argv[1]
filename_xsd = sys.argv[2]


# open and read schema file
with open(filename_xsd, 'rb') as schema_file:
    schema_to_check = schema_file.read()

# open and read xml file
with open(filename_xml, 'r', encoding='utf-8') as xml_file:
    xml_to_check = xml_file.read()

#parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
xmlschema_doc = etree.parse(StringIO(schema_to_check))
xmlschema = etree.XMLSchema(xmlschema_doc)

# parse xml
try:
    doc = etree.parse(StringIO(xml_to_check))
    print('XML well formed, syntax ok.')

# check for file IO error
except IOError:
    print('Invalid File')

# check for XML syntax errors
except etree.XMLSyntaxError as err:
    print('XML Syntax Error, see error_syntax.log')
    with open('error_syntax.log', 'w') as error_log_file:
        error_log_file.write(str(err.error_log))
    quit()

except:
    print('Unknown error, exiting.')
    quit()

# validate against schema
try:
    xmlschema.assertValid(doc)
    print('XML valid, schema validation ok.')

except etree.DocumentInvalid as err:
    print('Schema validation error, see error_schema.log')
    with open('error_schema.log', 'w') as error_log_file:
        error_log_file.write(str(err.error_log))
    quit()

except:
    print('Unknown error, exiting.')
    quit()
