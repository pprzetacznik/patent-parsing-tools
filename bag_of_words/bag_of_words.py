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
        self.map_of_words = dict(zip(self.list_of_words, xrange(0, self.dictSize)))


    def getDictionary(self, text, dictionary = None):
        if dictionary is None:
            start = time.time()

            # vec = numpy.zeros(self.dictSize, dtype=int)
            dictionary = {}
            for word in self.list_of_words:
                dictionary[word] = 0
            # print time.time() - start
        # print 'text size = ' + str(len(text.split()))
        for _, word_from_patent in enumerate(text.split()):
            parsedWord = stem(word_from_patent.lower())
            if self.validWord(word_from_patent) :
                dictionary[word_from_patent] += 1
                # index = self.bisection(parsedWord, 0, self.dictSize)
                # if index != None:
                #     vec[index] += 1;

        return dictionary

        # patent = Patent()
        # patent.documentID = root.findall(dtdStructure["documentID"])[0].text
        # patent.title = root.findall(dtdStructure["inventionTitle"])[0].text
        # patent.date = root.findall(dtdStructure["date"])[0].text
        # patent.abstract = self.node_to_text(inputfile, root, dtdStructure, "abstract")
        # patent.description = self.node_to_text(inputfile, root, dtdStructure, "description")
        # patent.claims = self.node_to_text(inputfile, root, dtdStructure, "claims")


    def parsePatent(self, patent):
        try:
            if patent.title is None or patent.description is None or patent.claims is None:
                return None
            start = time.time()
            dictionary = self.getDictionary(patent.title)
            dictionary = self.getDictionary(patent.description, dictionary)
            dictionary = self.getDictionary(patent.claims, dictionary)
            vec = self.dictionary_to_vec(dictionary)
            print time.time() - start
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
        dictionary = open("./dictionary/myDict.txt", "r").read()
        bag = BagOfWords(dictionary)

        data = {}
        n = 0

        for fn in os.listdir(src):
            vec_name = dest + os.sep + fn
            # if not os.path.isfile(vec_name):   #skip vectors already created
            patent = cPickle.load(open(src + os.sep + fn, "rb"))
            vec = bag.parsePatent(patent)
            if vec is not None:
                data[vec_name] = vec
                    # vec.tofile(fname)
            if len(data) > 1000:
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