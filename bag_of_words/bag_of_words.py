import os
import sys
import cPickle
import patent
import time

from porter2 import stem


__author__ = 'vreal'

import numpy
import cPickle

class BagOfWords():

    def __init__(self, dictionary):
        self.list_of_words = dictionary.split("\n")
        self.dictSize = len(self.list_of_words)
        self.map_of_words = dict(zip(self.list_of_words, xrange(0, self.dictSize))) #only for checking if words is as key in dict


    def getDictionary(self, text, dictionary = None):
        if dictionary is None:
            # TODO making that dictionary ones and cloning it may speed up execution by 0.001s
            dictionary = {}
            for word in self.list_of_words:
                dictionary[word] = 0
        for _, word_from_patent in enumerate(text.split()):
            parsedWord = stem(word_from_patent.lower())
            if self.validWord(parsedWord) :
                dictionary[parsedWord] += 1
        return dictionary

    def parsePatent(self, patent):
        try:
            if patent.title is None or patent.description is None or patent.claims is None:
                print "patent %s have None in title, description or claims" % (patent.documentID)
                return None
            start = time.time()
            dictionary = self.getDictionary(patent.title)
            dictionary = self.getDictionary(patent.abstract, dictionary)
            dictionary = self.getDictionary(patent.description, dictionary)
            dictionary = self.getDictionary(patent.claims, dictionary)
            vec = self.dictionary_to_vec(dictionary)
            documentLength = len(patent.title) + len(patent.description) + len(patent.claims)
            if documentLength < 1000:
                print "Parsing patent %s with %d words is too short!" % (patent.documentID, documentLength)
                return None
            print "Parsing patent %s with %d words took %f s" % (patent.documentID, documentLength, (time.time() - start))
            return vec
        except Exception as e:
            print "Problem with parsing " + patent.documentID
            print e

    def dictionary_to_vec(self, dictionary):
        vec =  numpy.zeros(self.dictSize, dtype=int)
        index = 0
        for word in self.list_of_words:
            vec[index] = dictionary[word]
            index += 1
        return vec

    def validWord(self, word):
        if len(word) > 2 and word in self.map_of_words:
            return True
        return False

if __name__ == '__main__':
    if len(sys.argv) == 3:
        src = sys.argv[1]
        dest = sys.argv[2]
        dictionary = open("./dictionary/dictionary.txt", "r").read()
        bag = BagOfWords(dictionary)

        data = {}
        n = 0

        for fn in os.listdir(src):
            vec_name = dest + os.sep + fn
            patent_list = cPickle.load(open(src + os.sep + fn, "rb"))
            for patent in patent_list:
                vec = bag.parsePatent(patent)
                if vec is not None:
                    # data[vec_name] = vec
                    data[patent.documentID] = [vec, patent.classification]
                if len(data) >= 1023:
                    filename = dest + os.sep + "vectors_" + str(n)
                    print("Saving vectors to " + filename);
                    f = file(filename, 'wb')
                    cPickle.dump(data, f, protocol=cPickle.HIGHEST_PROTOCOL)
                    data = {}
                    n += 1
        if len(data) > 0:
                filename = dest + os.sep + "vectors_" + str(n)
                print("Saving last " + str(len(data)) + " vectors to " + filename);
                f = file(filename, 'wb')
                cPickle.dump(data, f, protocol=cPickle.HIGHEST_PROTOCOL)

    else:
        print "python bag_of_words.py [working_directory] [destination]"