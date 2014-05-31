# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
from os import listdir
from os.path import join
from downloader import Downloader
from unzipper import Unzipper
import splitter
from extractor import Extractor
from logger import Logger


class Supervisor():
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.logger = Logger().getLogger("Supervisor")

    def begin(self, begin_year, end_year):
        self.download_archives(begin_year, end_year)
        self.unzip_archives()
        self.split_archives()
        self.extract_data()

    def download_archives(self, begin_year, end_year):
        self.logger.info("downloading archives")
        print 'downloading archives'
        downloader = Downloader('https://www.google.com/googlebooks/uspto-patents-grants-text.html')
        downloader.download_archives(self.working_dir, begin_year, end_year)

    def unzip_archives(self):
        self.logger.info("unzipping archives")
        unzipper = Unzipper(self.working_dir)
        unzipper.unzip_all()

    def split_archives(self):
        self.logger.info("splitting files")
        xmls = get_files(self.working_dir, ".xml")
        for file in xmls:
            splitter.split_file(file, join(self.working_dir, "patents"))

    def extract_data(self):
        self.logger.info("extracting data")
        extractor = Extractor("extractor_configuration.json", self.working_dir)
        patents = get_files(join(self.working_dir, "patents"), ".XML")
        for patent in patents:
            self.logger.info("extracting " + patent)
            try:
                extractor.parse_and_save_to_database(patent)
            except Exception as e:
                self.logger.error(e.message, e.args)


def get_files(directory, type):
    return [join(directory, f) for f in listdir(directory) if f.endswith(type)]


def process_args(argv):
    dir = argv[1]

    if not os.path.isdir(dir):
        os.makedirs(dir)
    try:
        begin_year = int(argv[2])
        end_year = int(argv[3])
    except:
        print "incorrect year"

    return dir, begin_year, end_year


if __name__ == '__main__':
    if len(sys.argv) == 4:
        dir, begin_year, end_year = process_args(sys.argv)

        supervisor = Supervisor(dir)
        supervisor.begin(begin_year, end_year)
    else:
        print "python supervisor.py [directory] [year_from] [year_to]"