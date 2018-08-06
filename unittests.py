import unittest
from inputgenerator import generate_facet
import re
from lxml import etree
from IO import stringIO

class TestGenerator(unittest.TestCase):
    def validate(filename):
        with open("tester.xsd", 'r') as schema_file:
            schema_to_check = schema_file.read()
        with open(filename, 'r') as xml_file:
            xml_to_check = xml_file.read()

        xmlschema_doc = etree.parse(StringIO(schema_to_check))
        xmlschema = etree.XMLSchema(xmlschema_doc)

        try:
            doc = etree.parse(StringIO(xml_to_check))
            print("xml well formed")
        except IOError:
            print("invalid")


if __name__ == '__main__':
    unittest.main()
