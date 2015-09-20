import unittest
import doctest
import patent_parsing_tools.dictionary.dictionary_maker as dictionary_maker

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(dictionary_maker))
    return tests
