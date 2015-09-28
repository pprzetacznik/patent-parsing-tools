import unittest
import doctest
import patent_parsing_tools.bow.bag_of_words as bag_of_words
from patent_parsing_tools.bow.bag_of_words import BagOfWords
from pkg_resources import resource_filename
import os

def setUp(arg):
    dictionary = resource_filename("patent_parsing_tools.bow.tests", "dictionary.txt")
    arg.globs['bag_of_words'] = BagOfWords(dictionary)

def tearDown(_arg):
    if os.path.isfile("./final_serialized_patent"):
        os.remove("./final_serialized_patent")

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(bag_of_words, setUp=setUp, tearDown=tearDown))
    return tests
