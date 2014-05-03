# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import lxml.etree as ET
import json
import cPickle
from patent import Patent


class Extractor():
    def __init__(self, extractor_xpath, dir = "."):
        self.extractor_xpath = extractor_xpath
        self.dir = dir
        if not os.path.isdir(dir):
            os.makedirs(dir)
        json_data = open(extractor_xpath)
        self.structure = json.load(json_data)
        json_data.close()

    def parse_and_save_to_database(self, inputfile):
        tree = ET.parse(inputfile)
        root = tree.getroot()

        dtdFile = tree.docinfo.internalDTD.system_url if tree.docinfo.internalDTD.system_url else 'default'
        dtdStructure = self.structure[dtdFile]

        patent = Patent()
        patent.documentID = root.findall(dtdStructure["documentID"])[0].text
        patent.title = root.findall(dtdStructure["inventionTitle"])[0].text
        patent.date = root.findall(dtdStructure["date"])[0].text
        description = ET.tostring(root.findall(dtdStructure["description"])[0], pretty_print=True)
        patent.description = re.sub('<[^<]+?>', '', description)
        claims = ET.tostring(root.findall(dtdStructure["claims"])[0], pretty_print=True)
        patent.claims = re.sub('<[^<]+?>', '', claims)

        f = file(self.dir + '/' + root.attrib['file'] + '.save', 'wb')
        cPickle.dump(patent, f, protocol=cPickle.HIGHEST_PROTOCOL)
        f.close()
