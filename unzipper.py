# -*- coding: utf-8 -*-
#!/usr/bin/env python

from zipfile import is_zipfile, ZipFile
from sys import argv
from os import *
from os.path import *
from splitter import Splitter
from logger import Logger

class Unzipper():
    def __init__(self, directory):
        self.working_directory = directory
        self.temp_dir = join(directory, "temp")
        self.logger = Logger().getLogger("Uzipper")
        self.patentDir = "patents"

    def unzip_all(self):
        zip_files = [ join(self.working_directory, f)
                      for f in listdir(self.working_directory) if is_zipfile(join(self.working_directory, f)) ]
        for zip_name in zip_files:
            try:
                zip = ZipFile(zip_name)
                if self.should_be_unzipped(zip):
                    self.logger.info("unzip " + zip_name)
                    zip.extractall(self.temp_dir)
                self.split_patents(self.temp_dir, splitext(basename(zip_name))[0])
                self.clear_temp()
            except Exception as e:
                self.logger.error(e.message)

    def should_be_unzipped(self, zip):
        for file in zip.namelist():
            if not isfile(join(self.working_directory, file)):
                return True
        return False

    def split_patents(self, temp_dir, filename):
        self.logger.info("splitting files")
        xmls = get_files(temp_dir, ".xml")
        splitter = Splitter()

        for file in xmls:
            splitter.split_file(file, join(self.working_directory, self.patentDir, filename))


    def clear_temp(self):
        for file in listdir(self.temp_dir):
            file_path = join(self.temp_dir, file)
            try:
                if isfile(file_path):
                    unlink(file_path)
            except Exception, e:
                print e


def get_files(directory, type):
    return [join(directory, f) for f in listdir(directory) if f.endswith(type)]

if __name__ == '__main__':
    if len(argv) == 2:
        dir = argv[1]
        unzipper = Unzipper(dir)
        unzipper.unzip_all()
    else:
        print "python unzipper.py [directory]"