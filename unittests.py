import unittest
from inputgenerator import generate_facet
import re

class TestGenerator(unittest.TestCase):
    def test_facet(self):
        string = generate_facet()
        comp   = re.compile('wavelength_range .*, dicipline_name (.*),?.*')
        self.assertTrue(re.match(comp, string) )

    def test_ref(self):
        invest = reftype(1)
        obs = reftype(2)
        comp = re.compile('reference_type ')

if __name__ == '__main__':
    unittest.main()
