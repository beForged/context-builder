import unittest
from inputgenerator import generate_facet
import re

class TestGenerator(unittest.TestCase):
    def test_generatefacet(self):
        s = generate_facet()
        print(s)
        m = re.compile('wavelength (.*)')
        self.assertTrue(re.match(m,s))
        

if __name__ == '__main__':
    unittest.main()
