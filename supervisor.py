# -*- coding: utf-8 -*-
#!/usr/bin/env python
from random import randint
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
    def __init__(self, working_dir, train_destination, test_destination):
        self.working_dir = working_dir
        self.train_destination = train_destination
        self.test_destination = test_destination
        self.logger = Logger().getLogger("Supervisor")

    def begin(self, begin_year, end_year):
        self.download_archives(begin_year, end_year)
        self.unzip_patents()
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
        extractor = Extractor("extractor_configuration.json", self.train_destination)
        patents = get_files(join(self.working_dir, "patents"), ".XML")
        train_patent_list = []
        test_patent_list = []
        test_list_number = 1
        train_list_number = 1
        num_of_valid_patents = 0
        num_of_unvalid_patents = 0
        total_number_of_test_patents = 0

        for patent in patents:
            self.logger.info("extracting " + patent)
            try:
                parsed_patent = extractor.parse(patent)
                if self.is_patent_valid(parsed_patent):
                    num_of_valid_patents += 1
                    if randint(1, 10) == 10: # 10% szansy
                        test_patent_list.append(parsed_patent)
                        total_number_of_test_patents += 1
                    else:
                        train_patent_list.append(parsed_patent)
                else:
                    num_of_unvalid_patents += 1
            except Exception as e:
                self.logger.error(e.message)
            if(len(test_patent_list) >= 1024):
                self.save_list(test_patent_list, test_list_number, self.test_destination)
                test_list_number += 1
            if(len(train_patent_list) >= 1024):
                self.save_list(train_patent_list, train_list_number, self.train_destination)
                train_list_number += 1
                print "Number of valid patents was %d, number of unvalid patents was %d" % (num_of_valid_patents, num_of_unvalid_patents)
        self.save_list(test_patent_list, test_list_number, self.test_destination)
        self.save_list(train_patent_list, train_list_number, self.train_destination)
        print "Final number of valid patents was %d, number of unvalid patents was %d" % (num_of_valid_patents, num_of_unvalid_patents)
        print "Total number of test examples is %d" % (total_number_of_test_patents)


    def save_list(self, patent_list, patent_list_number, patent_list_destination):
        f = file(patent_list_destination + os.sep + "xml_tuple_" + str(patent_list_number), 'wb')
        cPickle.dump(patent_list, f, protocol=cPickle.HIGHEST_PROTOCOL)
        del patent_list[:]
        f.close()

    def is_patent_valid(self, patent):
        if patent is not None and \
            len(patent.classification) > 0 and \
            patent.abstract is not None and \
            patent.title is not None and \
            patent.description is not None and \
            patent.claims is not None:
            return True
        self.logger.warn("patent not valid")
        return False

def get_files(directory, type):
    return [join(directory, f) for f in listdir(directory) if f.endswith(type)]

def process_args(argv):
    src = argv[1]
    train_dest = argv[2]
    test_dest = argv[3]

    if not os.path.isdir(train_dest):
        os.makedirs(train_dest)

    if not os.path.isdir(test_dest):
        os.makedirs(test_dest)
    try:
        begin_year = int(argv[4])
        end_year = int(argv[5])
    except:
        print "incorrect year"

    return src, train_dest, test_dest, begin_year, end_year


if __name__ == '__main__':
    if len(sys.argv) == 6:
        src, train_dest, test_dest, begin_year, end_year = process_args(sys.argv)

        supervisor = Supervisor(src, train_dest, test_dest)
        supervisor.begin(begin_year, end_year)
    else:
        print "python supervisor.py [working_directory] [train_destination] [test_destination] [year_from] [year_to]"