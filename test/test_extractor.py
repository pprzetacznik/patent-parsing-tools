# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
import cPickle
from extractor import Extractor, NotSupportedDTDConfiguration
from pprint import pprint
import lxml.etree as ET
import os


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = Extractor('extractor_configuration.json', 'test_data')

    def tearDown(self):
        pass

    def test_should_load_json_file(self):
        self.assertIsNotNone(self.extractor.structure["us-patent-grant-v44-2013-05-16.dtd"]["documentID"])
        pprint(self.extractor.structure)

    def test_xpaths(self):
        inputfile = 'test/US08613112-20131224.XML'

        tree = ET.parse(inputfile)
        root = tree.getroot()

        dtdStructure = self.extractor.structure[tree.docinfo.internalDTD.system_url]

        print "Document ID:", root.findall(dtdStructure["documentID"])[0].text
        print "Invention Title:", root.findall('.//us-bibliographic-data-grant//invention-title')[0].text
        print "Date:", root.findall('.//application-reference//document-id//date')[0].text

        patent = self.extractor.parse(inputfile)

        self.assertEqual(patent.documentID, root.findall(dtdStructure["documentID"])[0].text)
        self.assertEqual(patent.title, root.findall(dtdStructure["inventionTitle"])[0].text)
        self.assertEqual(patent.date, root.findall(dtdStructure["date"])[0].text)
        self.assertIsNotNone(patent.abstract)
        self.assertIsNotNone(patent.description)
        self.assertIsNotNone(patent.claims)

    def test_xml_structures(self):
        inputfiles = ["test/US08613112-20131224.XML",
                     "test/US08927386-20150106.XML"]
        for inputfile in inputfiles:
            patent = self.extractor.parse(inputfile)
            self.assertIsNotNone(patent.documentID)
            self.assertIsNotNone(patent.title)
            self.assertIsNotNone(patent.date)
            self.assertIsNotNone(patent.abstract)
            self.assertIsNotNone(patent.description)
            self.assertIsNotNone(patent.claims)

    def test_exception_not_supported_xml_structure(self):
        inputfile = 'test/US08613112-noDTDFile.XML'
        self.assertRaises(NotSupportedDTDConfiguration, self.extractor.parse, inputfile)

    def test_exception_not_implemented_dtd_structure(self):
        inputfile = 'test/US08613112-notSupportedDTD.XML'
        self.assertRaises(NotSupportedDTDConfiguration, self.extractor.parse, inputfile)

    def test_no_exception_when_lack_of_node(self):
        inputfile = 'test/US08613112-lackofnode.XML'
        self.extractor.parse(inputfile)

    def test_throw_exception_and_go_through(self):
        try:
            self.extractor.parse('test/US08613112-noDTDFile.XML')
        except NotSupportedDTDConfiguration as r:
            print "Catched first Exception with message: \"" + r.message + "\""

        try:
            self.extractor.parse('test/US08613112-notSupportedDTD.XML')
        except NotSupportedDTDConfiguration as r:
            print "Catched second Exception with message: \"" + r.message + "\""

if __name__ == '__main__':
    unittest.main()

