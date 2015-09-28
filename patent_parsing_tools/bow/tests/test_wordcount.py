import unittest
import doctest
import patent_parsing_tools.bow.wordcount as wordcount

def setUp(_arg):
    pass

def tearDown(_arg):
    pass

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(wordcount, setUp=setUp, tearDown=tearDown))
    return tests
