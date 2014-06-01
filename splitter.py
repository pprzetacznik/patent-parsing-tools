# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import sys
from logger import Logger

PATENT_TAG = 'us-patent-grant'


class Splitter:
    def __init__(self):
        self.logger = Logger().getLogger("Splitter")

    def get_headers_and_filename(self, file):
        headers = []
        for i in range(3):
            line = file.readline()
            headers.append(line)

        if not headers[2].startswith('<%s' % PATENT_TAG):
            self.logger.info("ignoring " + headers[2][1:headers[2].index(' ')])
            return None, None

        node = re.match(r'.*file=.([^ ]*)\".*', headers[2])
        if node is None:
            self.logger.warning("file attribute not found")
            raise Exception("file attribute not found")
        return headers, node.group(1)

    def ingore_file(self, fread):
        while True:
            line = fread.readline()
            if line.startswith('</%s' % PATENT_TAG):
                break

    def save_file(self, dir, filename, fread, headers):
        fwrite = open(os.path.join(dir, filename), 'w')
        for line in headers:
            fwrite.write(line)
        while True:
            line = fread.readline()
            fwrite.write(line)
            if line.startswith('</%s' % PATENT_TAG):
                break

    def split_file(self, input_file, dir):
        fread = open(input_file)

        if not os.path.isdir(dir):
            os.makedirs(dir)

        eof = os.fstat(fread.fileno()).st_size
        while fread.tell() < eof:
            headers, filename = self.get_headers_and_filename(fread)
            if filename is None:
                self.ingore_file(fread)
                continue
            self.save_file(dir, filename, fread, headers)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        input = sys.argv[1]
        dir = sys.argv[2]
        if os.path.isfile(input):
            splitter = Splitter()
            splitter.split_file(input, dir)
        else:
            print "File: " + input + " doesn't exist"
    else:
        print "python splitter.py [input] [output_dir]"
