# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import cPickle
import operator
import re
from nltk import download
from nltk.corpus import stopwords
from stemming.porter2 import stem
from patent_parsing_tools.patent import Patent
from patent_parsing_tools.utils.log import log, log_timer


@log
class DictionaryMaker:
    def __init__(self):
        self.word_dictionary = {}

    @log_timer
    def parse(self, directory, max_parsed_patents):
        n = 0
        for fn in os.listdir(directory):
            self.logger.info(directory + os.sep + fn)
            patent_list = cPickle.load(open(directory + os.sep + fn, "rb"))

            for patent in patent_list:
                self.parse_text(patent.abstract)
                self.parse_text(patent.description)
                self.parse_text(patent.claims)
                self.parse_text(patent.title)
                n += 1
                if n > max_parsed_patents:#6,7s dla stem tylko dla topu, 368s dla wszystkich
                    break

    @log_timer
    def sort(self):
        self.word_dictionary = sorted(self.word_dictionary.items(), key=operator.itemgetter(1), reverse=True)

    @log_timer
    def dump(self, dictionary_name, dict_max_size):
        f = open(dictionary_name, "w")
        download('stopwords')
        stop = stopwords.words('english')
        set_of_valid_words = set()
        for (word, counter) in self.word_dictionary:
            if (len(word) > 2) and (not any(ch.isdigit() for ch in word)) and (not word in stop):
                set_of_valid_words.add(stem(word.lower()))
                if len(set_of_valid_words) >= dict_max_size:
                    f.write('\n'.join(set_of_valid_words))
                    break
        f.close()

    def parse_text(self, text):
        clear = re.sub("[^a-zA-Z \n]", "", text)
        for _, word_from_patent in enumerate(clear.split()):
            if word_from_patent in self.word_dictionary:
                self.word_dictionary[word_from_patent] += 1
            else:
                self.word_dictionary[word_from_patent] = 1


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "python -m dictionary_maker [train_directory] [max_parsed_patents] [dict_max_size] [dictionary_name]"
    else:
        train_directory = sys.argv[1]

        max_parsed_patents = int(sys.argv[2])
        dict_max_size = int(sys.argv[3])
        dictionary_name = sys.argv[4]

        dictionary_maker = DictionaryMaker()
        dictionary_maker.parse(train_directory, max_parsed_patents)
        dictionary_maker.sort()
        dictionary_maker.dump(dictionary_name, dict_max_size)

