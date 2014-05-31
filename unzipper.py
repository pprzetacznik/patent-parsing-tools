# -*- coding: utf-8 -*-
#!/usr/bin/env python

from zipfile import is_zipfile, ZipFile
from sys import argv
from os import listdir
from os.path import join, isfile
from logger import Logger

class Unzipper():
    def __init__(self, directory):
        self.directory = directory
        self.logger = Logger().getLogger("Uzipper")

    def unzip_all(self):
        zip_files = [ join(self.directory, f)
                      for f in listdir(self.directory) if is_zipfile(join(self.directory, f)) ]
        for zip_name in zip_files:
            try:
                zip = ZipFile(zip_name)
                if self.should_be_unzipped(zip):
                    self.logger.info("unzip " + zip_name)
                    zip.extractall(self.directory)
            except Exception as e:
                self.logger.error(e.message)

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