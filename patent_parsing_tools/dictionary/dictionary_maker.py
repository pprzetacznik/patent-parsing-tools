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
        download('stopwords')
        self.stopwords = stopwords.words('english')
        self.wordcount = {}
        self.parse_regexp = re.compile(r"([0-9]*[a-zA-Z][a-zA-Z0-9]+)", re.DOTALL)

    @log_timer
    def parse(self, directory, max_parsed_patents):
        n = 0
        for fn in os.listdir(directory):
            self.logger.info(directory + os.sep + fn)
            patent_list = cPickle.load(open(directory + os.sep + fn, "rb"))

            for patent in patent_list:
                self._parse_text(patent.abstract)
                self._parse_text(patent.description)
                self._parse_text(patent.claims)
                self._parse_text(patent.title)
                n += 1
                if n > max_parsed_patents:
                    break
        self.logger.info("Parsed: " + str(n) + " patents")

    @log_timer
    def dump(self, dictionary_name, dict_max_size):
        sorted_wordcount = sorted(self.wordcount.items(), key=operator.itemgetter(1), reverse=True)[:dict_max_size]
        with open (dictionary_name, 'w') as f:
            keys = [item[0] for item in sorted_wordcount]
            f.write('\n'.join(keys))

    def _parse_text(self, text):
        """
        >>> dictionary_maker = DictionaryMaker() #doctest: +ELLIPSIS
        [nltk_data] ...
        >>> dictionary_maker._parse_text_fast("a1a ma kota")
        >>> print dictionary_maker.wordcount
        {'ma': 1, 'a1a': 1, 'kota': 1}
        """
        words = self.parse_regexp.findall(text)
        for word in words:
            new_word = stem(word.lower())
            if new_word not in self.stopwords:
                if new_word in self.wordcount:
                    self.wordcount[new_word] += 1
                else:
                    self.wordcount[new_word] = 1

    @log_timer
    def _parse_text_fast(self, text):
        """
        >>> dictionary_maker = DictionaryMaker() #doctest: +ELLIPSIS
        [nltk_data] ...
        >>> dictionary_maker._parse_text_fast("a1a ma kota")
        >>> print dictionary_maker.wordcount
        {'ma': 1, 'a1a': 1, 'kota': 1}
        """
        split_regexp = re.compile(ur"[^a-zA-Z0-9 \n]", re.DOTALL)
        new_text = split_regexp.sub(" ", text)
        words = new_text.split()
        for word in words:
            new_word = word.lower()
            if new_word.isalnum() and new_word not in self.stopwords:
                if new_word in self.wordcount:
                    self.wordcount[new_word] += 1
                else:
                    self.wordcount[new_word] = 1



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
        dictionary_maker.dump(dictionary_name, dict_max_size)
