# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import lxml.etree as ET
import json
from patent import Patent


class NotSupportedDTDConfiguration(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class Extractor():
    def __init__(self, extractor_xpath_configuration, dir="."):
        self.extractor_xpath = extractor_xpath_configuration
        self.dir = dir
        if not os.path.isdir(dir):
            os.makedirs(dir)
        json_data = open(extractor_xpath_configuration)
        self.structure = json.load(json_data)
        json_data.close()

    def parse_and_save_to_database(self, inputfile):
        tree = ET.parse(inputfile)
        root = tree.getroot()

        try:
            dtdStructure = self.getDTDXpathConfiguration(inputfile, tree)
        except NotSupportedDTDConfiguration as e:
            raise e

        patent = Patent()
        patent.documentID = root.findall(dtdStructure["documentID"])[0].text
        patent.title = root.findall(dtdStructure["inventionTitle"])[0].text
        patent.date = root.findall(dtdStructure["date"])[0].text
        patent.abstract = self.clean_html_tags(ET.tostring(root.findall(dtdStructure["abstract"])[0], pretty_print=True))
        patent.description = self.clean_html_tags(ET.tostring(root.findall(dtdStructure["description"])[0], pretty_print=True))
        patent.claims = self.clean_html_tags(ET.tostring(root.findall(dtdStructure["claims"])[0], pretty_print=True))

        patent.serialize(self.dir + '/' + root.attrib['file'] + '.save')

    def clean_html_tags(self, string):
        return re.sub('<[^<]+?>', '', string)

    def getDTDXpathConfiguration(self, inputfile, tree):
        try:
            dtdFile = tree.docinfo.internalDTD.system_url
        except Exception:
            raise NotSupportedDTDConfiguration('File: ' + inputfile + ' has not supported xml structure')

        try:
            return self.structure[dtdFile]
        except Exception:
            raise NotSupportedDTDConfiguration('File: ' + inputfile + ' has not implemented structure (' + dtdFile + ')')