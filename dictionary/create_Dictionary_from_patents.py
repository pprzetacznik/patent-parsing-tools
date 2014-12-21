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

def dump_dictionary(sorted_dictionary, dict_max_size, dictionary_name):
    f = open(dictionary_name, "w")
    stop = stopwords.words('english')
    #wartosc lekko z dupy, ze wzledu na stop wordy i steming odpadnie ich okolo polowy
    set_of_valid_words = set()
    for (word,counter) in sorted_dictionary:
        if (len(word) > 2) and (not any(ch.isdigit() for ch in word)) and (not word in stop):
            set_of_valid_words.add(word.lower())
            if len(set_of_valid_words) >= dict_max_size:
                for my_word in sorted(set_of_valid_words):
                    f.write(my_word + "\n")
                break;
    f.close()
    print "Done"
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Wrong arguments"
        print "python create_Dictionary_from_patents  src max_parsed_patents dict_max_size dictionary_name"
    else:
        src = sys.argv[1]

        max_parsed_patents = int(sys.argv[2])
        dict_max_size = int(sys.argv[3])
        dictionary_name = sys.argv[4]
        n= 0
        start = time.time()
        for fn in os.listdir(src):
            patent_list = cPickle.load(open(src + os.sep + fn, "rb"))

            for patent in patent_list:
                parse_text(patent.abstract)
                parse_text(patent.description)
                parse_text(patent.claims)
                parse_text(patent.title)
                n += 1
                if n > max_parsed_patents:#6,7s dla stem tylko dla topu, 368s dla wszystkich
                    break

        print "Parsing took %f s" % (time.time() - start)
        start = time.time()
        sorted_dictionary = sorted(word_dictionary.items(), key=operator.itemgetter(1), reverse=True)
        print "Sorting took %f s" % (time.time() - start)
        dump_dictionary(sorted_dictionary, dict_max_size, dictionary_name)

