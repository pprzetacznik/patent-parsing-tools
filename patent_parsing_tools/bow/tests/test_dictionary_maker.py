import unittest
import doctest
import patent_parsing_tools.bow.dictionary_maker as dictionary_maker

def setUp(_arg):
    pass

def tearDown(_arg):
    pass

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(dictionary_maker, setUp=setUp, tearDown=tearDown))
    return tests
