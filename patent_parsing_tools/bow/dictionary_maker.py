# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import cPickle
import operator
from patent_parsing_tools.patent import Patent
from patent_parsing_tools.bow.wordcount import WordCount
from patent_parsing_tools.utils.log import log, log_timer


@log
class DictionaryMaker:
    """
    >>> dictionary_maker = DictionaryMaker() #doctest: +ELLIPSIS
    [...
    """

    def __init__(self):
        self.wordcount = WordCount()
        self.wordcount_dictionary = {}

    @log_timer
    def parse(self, directory, max_parsed_patents):
        n = 0
        for fn in os.listdir(directory):
            self.logger.info(directory + os.sep + fn)
            patent_list = cPickle.load(open(directory + os.sep + fn, "rb"))

            for patent in patent_list:
                self.wordcount.parse_text(patent.abstract, self.wordcount_dictionary)
                self.wordcount.parse_text(patent.description, self.wordcount_dictionary)
                self.wordcount.parse_text(patent.claims, self.wordcount_dictionary)
                self.wordcount.parse_text(patent.title, self.wordcount_dictionary)
                n += 1
                if n > max_parsed_patents:
                    break
        self.logger.info("Parsed: " + str(n) + " patents")

    @log_timer
    def dump(self, dictionary_name, dict_max_size):
        sorted_wordcount = sorted(self.wordcount_dictionary.items(), key=operator.itemgetter(1), reverse=True)[:dict_max_size]
        with open (dictionary_name, 'w') as f:
            keys = [item[0] for item in sorted_wordcount]
            f.write('\n'.join(keys))


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "python -m patent_parsing_tools.bow.dictionary_maker [train_directory] [max_parsed_patents] [dict_max_size] [dictionary_name]"
    else:
        train_directory = sys.argv[1]

        max_parsed_patents = int(sys.argv[2])
        dict_max_size = int(sys.argv[3])
        dictionary_name = sys.argv[4]

        dictionary_maker = DictionaryMaker()
        dictionary_maker.parse(train_directory, max_parsed_patents)
        dictionary_maker.dump(dictionary_name, dict_max_size)
