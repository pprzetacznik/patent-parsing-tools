# -*- coding: utf-8 -*-
#!/usr/bin/env python

from zipfile import is_zipfile, ZipFile
from sys import argv
from os import listdir
from os.path import join, isfile

class Unzipper():
    def __init__(self, directory):
        self.directory = directory

    def unzip_all(self):
        zip_files = [ join(self.directory, f)
                      for f in listdir(self.directory) if is_zipfile(join(self.directory, f)) ]
        for zip_name in zip_files:
            zip = ZipFile(zip_name)
            if self.should_be_unzipped(zip):
                print "unzip", zip_name
                zip.extractall(self.directory)

    def should_be_unzipped(self, zip):
        for file in zip.namelist():
            if not isfile(join(self.directory, file)):
                return True
        return False

if __name__ == '__main__':
    if len(argv) == 2:
        dir = argv[1]
        unzipper = Unzipper(dir)
        unzipper.unzip_all()
    else:
        print "python unzipper.py [directory]"