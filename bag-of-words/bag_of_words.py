import os
import sys
import cPickle

from porter2 import stem


__author__ = 'vreal'

import numpy

class BagOfWords():

    def __init__(self, dict):
        self.list_of_words = dict.split("\n")
        self.dictSize = len(self.list_of_words)


    def getVec(self, text, vec = None):
        if vec is None:
            vec = numpy.zeros(self.dictSize, dtype=int)
        for i, str in enumerate(text.split()):
            parsedWord = stem(str.lower())
            if self.validWord(parsedWord):

                index = self.bisection(parsedWord, 0, self.dictSize)
                if index != None:
                    vec[index] += 1;

        return vec

        # patent = Patent()
        # patent.documentID = root.findall(dtdStructure["documentID"])[0].text
        # patent.title = root.findall(dtdStructure["inventionTitle"])[0].text
        # patent.date = root.findall(dtdStructure["date"])[0].text
        # patent.abstract = self.node_to_text(inputfile, root, dtdStructure, "abstract")
        # patent.description = self.node_to_text(inputfile, root, dtdStructure, "description")
        # patent.claims = self.node_to_text(inputfile, root, dtdStructure, "claims")


    def parsePatent(self, patent):
        try:
            vec = self.getVec(patent.title)
            vec = self.getVec(patent.description, vec)
            vec = self.getVec(patent.claims, vec)
            return vec
        except:
            print "Problem with parsing " + patent.documentID

    def validWord(self, word):
        if len(word) < 3:
            return False
        return True

    def bisection(self, looking, start, end ):
        index = (start + end) / 2;
        # print start, end, index
        if start >= end:
            # print "Nie znalazlem slowa " + looking
            return None
        word = self.list_of_words[index]
        if word == looking:
            # print looking + " ma index " + str(index)
            return index
        elif looking < word :
            return self.bisection(looking, start, index)
        else:
            return self.bisection(looking, index + 1, end)

if __name__ == '__main__':


    if len(sys.argv) == 3:
        src = sys.argv[1]
        dest = sys.argv[2]
        dict = open("dictionary/../dictionary/myDict.txt", "r").read()
        bag = BagOfWords(dict)

        # print bag.bisection('aaron', 0, bag.dictSize)

        for fn in os.listdir(src):
            patent = cPickle.load(open(src + os.sep + fn, "rb"))
            vec = bag.parsePatent(patent)
            if vec is not None:
                vec.tofile(dest + os.sep + fn)
    else:
        print "python bag_of_words.py [working_directory] [destination]"