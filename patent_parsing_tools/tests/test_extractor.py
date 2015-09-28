# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
from patent_parsing_tools.extractor import Extractor, NotSupportedDTDConfiguration
import lxml.etree as ET
from pkg_resources import resource_filename


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = Extractor("test_data")

    def tearDown(self):
        pass

    def test_should_load_json_file(self):
        self.assertIsNotNone(self.extractor.structure["us-patent-grant-v44-2013-05-16.dtd"]["documentID"])

    def test_xpaths(self):
        inputfile = resource_filename("patent_parsing_tools.tests", "US08613112-20131224.XML")

        tree = ET.parse(inputfile)
        root = tree.getroot()

        dtdStructure = self.extractor.structure[tree.docinfo.internalDTD.system_url]
        patent = self.extractor.parse(inputfile)

        self.assertEqual(patent.documentID, root.findall(dtdStructure["documentID"])[0].text)
        self.assertEqual(patent.title, root.findall(dtdStructure["inventionTitle"])[0].text)
        self.assertEqual(patent.date, root.findall(dtdStructure["date"])[0].text)
        self.assertIsNotNone(patent.abstract)
        self.assertIsNotNone(patent.description)
        self.assertIsNotNone(patent.claims)

    def test_xml_structures(self):
        inputfiles = ["US08613112-20131224.XML",
                     "US08927386-20150106.XML"]
        for inputfile in inputfiles:
            patent = self.extractor.parse(resource_filename("patent_parsing_tools.tests", inputfile))
            self.assertIsNotNone(patent.documentID)
            self.assertIsNotNone(patent.title)
            self.assertIsNotNone(patent.date)
            self.assertIsNotNone(patent.abstract)
            self.assertIsNotNone(patent.description)
            self.assertIsNotNone(patent.claims)

    def test_exception_not_supported_xml_structure(self):
        inputfile = resource_filename("patent_parsing_tools.tests", "US08613112-noDTDFile.XML")
        self.assertRaises(NotSupportedDTDConfiguration, self.extractor.parse, inputfile)

    def test_exception_not_implemented_dtd_structure(self):
        inputfile = resource_filename("patent_parsing_tools.tests", "US08613112-notSupportedDTD.XML")
        self.assertRaises(NotSupportedDTDConfiguration, self.extractor.parse, inputfile)

    def test_no_exception_when_lack_of_node(self):
        inputfile = resource_filename("patent_parsing_tools.tests", "US08613112-lackofnode.XML")
        self.extractor.parse(inputfile)

    def test_throw_exception_and_go_through(self):
        inputfile = resource_filename("patent_parsing_tools.tests", "US08613112-noDTDFile.XML")
        try:
            self.extractor.parse(resource_filename("patent_parsing_tools.tests", "US08613112-noDTDFile.XML"))
        except NotSupportedDTDConfiguration as r:
            print "Catched first Exception with message: \"" + r.message + "\""

        try:
            self.extractor.parse(resource_filename("patent_parsing_tools.tests", "US08613112-notSupportedDTD.XML"))
        except NotSupportedDTDConfiguration as r:
            print "Catched second Exception with message: \"" + r.message + "\""

if __name__ == '__main__':
    unittest.main()

