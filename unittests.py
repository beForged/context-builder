import unittest
from inputgenerator import generate_facet
from inputgenerator import *
import re

class TestGenerator(unittest.TestCase):

    def test_facet(self):
        string = generate_facet(0,0,0,0)
        self.assertEqual(string, "science_facets wavelength_range Infrared, discipline_name Imaging" )
        string = generate_facet(3, 1, 1, 3)
        self.assertEqual(string, "science_facets wavelength_range Near Infrared, discipline_name fields, facet1 Magnetic")
        string = generate_facet(5, 2, 1, 4)
        self.assertEqual(string, "science_facets wavelength_range Submillimeter, discipline_name Small Bodies, facet1 Historical Reference")
        self.assertRaises(ValueError, generate_facet, 13, 123,124,2)
        

    def test_ref(self):
        invest = reftype(1, 0)
        obs = reftype(2, 2)
        self.assertEqual("reference_type bundle_to_investigation", invest)
        self.assertEqual(" reference_type is_instrument", obs)
        self.assertEqual("reference_type data_to_investigation", reftype(1,3))

    def test_lid(self):
        lid = lidgen("abcdef", "ghijk")
        self.assertEqual(lid, "lid_reference urn:nasa:pds:abcdef:ghijk:sample")

    def test_purpose(self):
        string = purpose(2)
        self.assertEqual(string, "purpose Calibration")
        string = purpose(4)
        self.assertEqual(string, "purpose Science")
        
    def test_processinglevel(self):
        string = processinglvl(0)
        self.assertEqual(string,"processing_level Calibrated")
        string = processinglvl(3)
        self.assertEqual(string,"processing_level Raw")
        string = processinglvl(10)
        self.assertEqual(string,"processing_level Calibrated")
        self.assertRaises(ValueError, processinglvl, -2)
        
    def test_type(self):
        string = typegen(1, 3)
        self.assertEqual(string, "type Other Investigation")
        string = typegen(2, 8)
        self.assertEqual(string, " type Telescope")
        string = typegen(3, 3)
        self.assertEqual(string, " type Dwarf Planet Meteorite")
        string = typegen(3, 6)
        self.assertEqual(string, " type Satellite")

    def test_name(self):
        self.assertEqual(namegen("abcd", 4), "name abcd4")

    def test_ret(self):
        self.assertEqual(addret("test"), "test\n")

    def test_obs(self):
        string = obs("spaceship", 4, 2, 2)
        self.assertEqual(string, "Observing_System_Components name spaceship4 type Balloon lid_reference urn:nasa:pds:context:observing:sample reference_type is_instrument")

    def test_target(self):
        string = target("sample_name", 7, 3)
        comp = "Target_Identification name sample_name7 type Telescope"


if __name__ == '__main__':
    unittest.main()