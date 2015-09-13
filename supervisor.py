# -*- coding: utf-8 -*-
#!/usr/bin/env python

from random import randint, shuffle
import sys
import os
from os import listdir
from os.path import join
import cPickle
from downloader import Downloader
from unzipper import Unzipper
from extractor import Extractor
from utils.log import log

@log
class Supervisor():
    def __init__(self, working_dir, train_destination, test_destination):
        self.working_dir = working_dir
        self.train_destination = train_destination
        self.test_destination = test_destination
        self.__create_directory_if_not_exists(self.working_dir)
        self.__create_directory_if_not_exists(self.train_destination)
        self.__create_directory_if_not_exists(self.test_destination)

    def __create_directory_if_not_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def begin(self, begin_year, end_year):
        self.download_archives(begin_year, end_year)
        self.unzip_patents()
        self.extract_data()

    def download_archives(self, begin_year, end_year):
        self.logger.info("downloading archives")
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
        num_of_valid_patents = 0
        num_of_unvalid_patents = 0
        total_number_of_test_patents = 0

        for patent in patents:
            self.logger.info("extracting " + patent)
            try:
                parsed_patent = extractor.parse(patent)
                if self.is_patent_valid(parsed_patent):
                    num_of_valid_patents += 1
                    if len(test_patent_list) % 1000 == 0:
                        self.logger.info("train_patent_list has length %d" % (len(train_patent_list)))
                    if randint(1, 10) == 10: # 10% szansy
                        test_patent_list.append(parsed_patent)
                        total_number_of_test_patents += 1
                    else:
                        train_patent_list.append(parsed_patent)
                else:
                    num_of_unvalid_patents += 1
            except Exception as e:
                self.logger.error(e.message)
                self.logger.error("Number of valid patents was %d, number of unvalid patents was %d" % (num_of_valid_patents, num_of_unvalid_patents))
        self.save_list(test_patent_list, self.test_destination)
        self.save_list(train_patent_list, self.train_destination)
        self.logger.info("Final number of valid patents was %d, number of unvalid patents was %d" % (num_of_valid_patents, num_of_unvalid_patents))
        self.logger.info("Total number of test examples is %d" % (total_number_of_test_patents))


    def save_list(self, patent_list, patent_list_destination):
        shuffle(patent_list)
        ind = 0
        patent_list_number = 1
        while ind < len(patent_list):
            f = file(patent_list_destination + os.sep + "xml_tuple_" + str(patent_list_number), 'wb')
            if ind + 1023 > len(patent_list):
                cPickle.dump(patent_list[ind:], f, protocol=cPickle.HIGHEST_PROTOCOL)
            else:
                cPickle.dump(patent_list[ind: ind + 1023], f, protocol=cPickle.HIGHEST_PROTOCOL)
            f.close()
            patent_list_number += 1
            ind += 1024
        del patent_list[:]


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
    l = []
    for d in listdir(directory):
        if d.endswith(type):
            l.append(join(directory, d))
        else:
            for f in listdir(join(directory, d)):
                if f.endswith(type):
                    l.append(join(directory, d, f))
    return l

def process_args(argv):
    working_directory = argv[1]
    train_dest = argv[2]
    test_dest = argv[3]

    try:
        begin_year = int(argv[4])
        end_year = int(argv[5])
    except:
        print "incorrect year"

    return working_directory, train_dest, test_dest, begin_year, end_year


if __name__ == '__main__':
    if len(sys.argv) == 6:
        working_directory, train_dest, test_dest, begin_year, end_year = process_args(sys.argv)

        supervisor = Supervisor(working_directory, train_dest, test_dest)
        supervisor.begin(begin_year, end_year)
    else:
        print "python supervisor.py [working_directory] [train_destination] [test_destination] [year_from] [year_to]"

