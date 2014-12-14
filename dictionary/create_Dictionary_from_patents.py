import os
import sys
import cPickle
import operator
import re
import time
from nltk.corpus import stopwords
from porter2 import stem

__author__ = 'vreal'

word_dictionary = {}

def parse_text(text):
    clear = re.sub("[^a-zA-Z \n]", "", text)
    for _, word_from_patent in enumerate(clear.split()):
        if word_from_patent in word_dictionary:
            word_dictionary[word_from_patent] += 1
        else:
            word_dictionary[word_from_patent] = 1

def dump_dictionary(sorted_dictionary):
    f = open("dictionary.txt", "w")
    stop = stopwords.words('english')
    dict_max_size = 4048
    list_of_valid_words = []
    for (word,counter) in sorted_dictionary:
        if (len(word) > 2) and (not any(ch.isdigit() for ch in word)) and (not word in stop):
            list_of_valid_words.append(word.lower())
            dict_max_size -= 1
            if dict_max_size < 0:
                my_set = set()
                for valid_word in list_of_valid_words:
                    my_set.add(stem(valid_word))
                for my_word in sorted(my_set):
                    f.write(my_word + "\n")
                break;
    f.close()
    print "Done"
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        src = sys.argv[1]

        n = 0
        start = time.time()
        for fn in os.listdir(src):
            patent_list = cPickle.load(open(src + os.sep + fn, "rb"))

            for patent in patent_list:
                parse_text(patent.abstract)
                parse_text(patent.description)
                parse_text(patent.claims)
                parse_text(patent.title)
                n += 1
                if n > 10:
                    print "Parsing took %f s" % (time.time() - start)
                    start = time.time()
                    sorted_dictionary = sorted(word_dictionary.items(), key=operator.itemgetter(1), reverse=True)
                    print "Sorting took %f s" % (time.time() - start)
                    dump_dictionary(sorted_dictionary)



