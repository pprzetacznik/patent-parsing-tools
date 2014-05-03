# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
import cPickle
from extractor import Extractor
from pprint import pprint
import lxml.etree as ET
import os


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = Extractor('extractor_xpath.json', 'test_data')

    def tearDown(self):
        for root, dirs, files in os.walk('test_data', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('test_data')

    def test_should_load_json_file(self):
        self.assertIsNotNone(self.extractor.structure["default"]["documentID"])
        pprint(self.extractor.structure)

    def test_serialization(self):
        inputfile = 'c:\\patenty\\ipg131224\\concated\\US08613112-20131224.XML'

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
        self.assertIsNotNone(loaded_obj.description)
        self.assertIsNotNone(loaded_obj.claims)

if __name__ == '__main__':
    unittest.main()