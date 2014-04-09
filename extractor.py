# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET
import sys


def main(inputfile):
    tree = ET.parse(inputfile)
    root = tree.getroot()
    print "Document ID:", root.findall('.//publication-reference//document-id//doc-number')[0].text
    print "Invention Title:", root.findall('.//us-bibliographic-data-grant//invention-title')[0].text



if __name__ == '__main__':
    if len(sys.argv) == 2:
        inputfile = sys.argv[1]
    else:
        inputfile = 'c:\\patenty\\ipg131224\\concated\\US08613112-20131224.XML'

    if os.path.isfile(inputfile):
        main(inputfile)
    else:
        print "File: " + inputfile + " doesn't exist"
