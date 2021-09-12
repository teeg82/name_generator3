import unittest
from xml.etree import ElementTree

class TestXMLLoad(unittest.TestCase):

    def test_xml_load(self):
        tree = ElementTree.parse("../resources/LetterFrequency.xml")
        root = tree.getroot()
        self.assertEqual(root.tag, "letters")
