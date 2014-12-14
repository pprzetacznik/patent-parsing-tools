# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
from os import listdir
from os.path import join
import cPickle
from downloader import Downloader
from unzipper import Unzipper
from extractor import Extractor
from logger import Logger


class Supervisor():
    def __init__(self, working_dir, destination):
        self.working_dir = working_dir
        self.destination = destination
        self.logger = Logger().getLogger("Supervisor")

    def begin(self, begin_year, end_year):
        # self.download_archives(begin_year, end_year)
        # self.unzip_patents()
        self.extract_data()

    def download_archives(self, begin_year, end_year):
        self.logger.info("downloading archives")
        print 'downloading archives'
        downloader = Downloader('https://www.google.com/googlebooks/uspto-patents-grants-text.html')
        downloader.download_archives(self.working_dir, begin_year, end_year)

    def unzip_patents(self):
        self.logger.info("unzipping patents")
        unzipper = Unzipper(self.working_dir)
        unzipper.unzip_all()

    def extract_data(self):
        self.logger.info("extracting data")
        extractor = Extractor("extractor_configuration.json", self.destination)
        patents = get_files(join(self.working_dir, "patents"), ".XML")
        tuple = []
        tuple_number = 1

        for patent in patents:
            self.logger.info("extracting " + patent)
            try:
                parsed_patent = extractor.parse(patent)
                tuple.append(parsed_patent)
            except Exception as e:
                self.logger.error(e.message)
            if(len(tuple) >= 1024):
                f = file(self.destination + os.sep + "xml_tuple_" + str(tuple_number), 'wb')
                tuple_number += 1
                cPickle.dump(self, f, protocol=cPickle.HIGHEST_PROTOCOL)
                f.close()


def get_files(directory, type):
    return [join(directory, f) for f in listdir(directory) if f.endswith(type)]

def process_args(argv):
    src = argv[1]
    dest = argv[2]

    if not os.path.isdir(dest):
        os.makedirs(dest)
    try:
        begin_year = int(argv[3])
        end_year = int(argv[4])
    except:
        print "incorrect year"

    return src, dest, begin_year, end_year


if __name__ == '__main__':
    if len(sys.argv) == 5:
        src, dest, begin_year, end_year = process_args(sys.argv)

        supervisor = Supervisor(src, dest)
        supervisor.begin(begin_year, end_year)
    else:
        print "python supervisor.py [working_directory] [destination] [year_from] [year_to]"