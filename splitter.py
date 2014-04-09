# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os, re
import sys


def get_headers_and_filename(file):
    headers = []
    for i in range(3):
        line = file.readline()
        headers.append(line)
    node = re.match(r'.*file=.([^ ]*)\".*', headers[2])
    if node:
        return headers, re.match(r'.*file=.([^ ]*)\".*', headers[2]).group(1)
    return None, None


def split_file(input_file, dir):
    fread = open(input_file)
    os.makedirs(dir)
    eof = os.fstat(fread.fileno()).st_size
    while fread.tell() < eof:
        headers, filename = get_headers_and_filename(fread)
        if filename is None:
            break

        print filename
        print headers[2]
        print "============================================="

        fwrite = open(os.path.join(dir, filename), 'w')
        for line in headers: fwrite.write(line)
        while True:
            line = fread.readline()
            fwrite.write(line)
            if line.startswith('</us-patent-grant'):
                break


if __name__ == '__main__':
    if len(sys.argv) == 3:
        input = sys.argv[1]
        dir = sys.argv[2]
    else:
        input = "c:\\patenty\\ipg131224\\ipg131224.xml"
        dir = "c:\\patenty\\ipg131224\\concated"

    if os.path.isfile(input):
        split_file(input, dir)
    else:
        print "File: " + input + " doesn't exist"