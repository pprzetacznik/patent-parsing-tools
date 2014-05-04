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
        self.extractor = Extractor('../extractor_configuration.json', 'test_data')

    def tearDown(self):
        for root, dirs, files in os.walk('test_data', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('test_data')

    def test_should_load_json_file(self):
        self.assertIsNotNone(self.extractor.structure["us-patent-grant-v44-2013-05-16.dtd"]["documentID"])
        pprint(self.extractor.structure)

    def test_serialization(self):
        inputfile = 'US08613112-20131224.XML'

        tree = ET.parse(inputfile)
        root = tree.getroot()

        dtdStructure = self.extractor.structure[tree.docinfo.internalDTD.system_url]

        print "Document ID:", root.findall(dtdStructure["documentID"])[0].text
        print "Invention Title:", root.findall('.//us-bibliographic-data-grant//invention-title')[0].text
        print "Date:", root.findall('.//application-reference//document-id//date')[0].text

        self.extractor.parse_and_save_to_database(inputfile)

        f = file(self.extractor.dir + '/' + root.attrib['file'] + '.save', 'rb')
        loaded_obj = cPickle.load(f)
        f.close()

        self.assertEqual(loaded_obj.documentID, root.findall(dtdStructure["documentID"])[0].text)
        self.assertEqual(loaded_obj.title, root.findall(dtdStructure["inventionTitle"])[0].text)
        self.assertEqual(loaded_obj.date, root.findall(dtdStructure["date"])[0].text)
        self.assertIsNotNone(loaded_obj.abstract)
        self.assertIsNotNone(loaded_obj.description)
        self.assertIsNotNone(loaded_obj.claims)

    def test_exception_not_supported_xml_structure(self):
        inputfile = 'US08613112-noDTDFile.xml'
        self.assertRaises(NotSupportedDTDConfiguration, self.extractor.parse_and_save_to_database, inputfile)

    def test_exception_not_implemented_dtd_structure(self):
        inputfile = 'US08613112-notSupportedDTD.xml'
        self.assertRaises(NotSupportedDTDConfiguration, self.extractor.parse_and_save_to_database, inputfile)

    def test_throw_exception_and_go_through(self):
        try:
            self.extractor.parse_and_save_to_database('US08613112-noDTDFile.xml')
        except NotSupportedDTDConfiguration as r:
            print "Catched first Exception with message: \"" + r.message + "\""

        try:
            self.extractor.parse_and_save_to_database('US08613112-notSupportedDTD.xml')
        except NotSupportedDTDConfiguration as r:
            print "Catched second Exception with message: \"" + r.message + "\""

if __name__ == '__main__':
    unittest.main()