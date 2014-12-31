__author__ = 'vreal'

import re
from nltk.corpus import stopwords


def edit():
     wikipedia = open('dictionary.txt', 'r')
     myfile = open("myDict.txt", 'w')
     dict = []
     line = wikipedia.readline()
     while line != '':


         writeLine = re.sub(r'\d', '', line)
         writeLine = re.sub(r'\s', '', writeLine)
         dict.append(writeLine)
         line = wikipedia.readline()

     print dict[1]
     dict_words = []
     dict.sort()
     stop = stopwords.words('english')
     for x in xrange(0, 10000):
         word = dict[x].replace('.', '')
         # word = stem(word.lower())
         if len(word) > 2 and  word not in dict_words and word not in stop:
             myfile.write(word + "\n")
             dict_words.append(word)




edit()
