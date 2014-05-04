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


class Supervisor():
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def begin(self, begin_year, end_year):
        self.download_archives(begin_year, end_year)
        self.unzip_archives()
        self.split_archives()
        self.extract_data()

    def download_archives(self, begin_year, end_year):
        print 'downloading archives'
        downloader = Downloader('https://www.google.com/googlebooks/uspto-patents-grants-text.html')
        downloader.download_archives(self.working_dir, begin_year, end_year)

    def unzip_archives(self):
        print 'unzipping archives'
        unzipper = Unzipper(self.working_dir)
        unzipper.unzip_all()

    def split_archives(self):
        print 'splitting files'
        xmls = get_files(self.working_dir, ".xml")
        for file in xmls:
            splitter.split_file(file, join(self.working_dir, "patents"))

    def extract_data(self):
        print 'extracting data'
        extractor = Extractor("extractor_xpath.json", self.working_dir)
        patents = get_files(join(self.working_dir, "patents"), ".XML")
        for patent in patents:
            print "extracting", patent
            extractor.parse_and_save_to_database(patent)


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