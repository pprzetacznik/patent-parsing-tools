import unittest
import doctest
import patent_parsing_tools.patent as patent
import os

def setUp(_arg):
    pass

def tearDown(_arg):
    if os.path.isfile("serialized_patent"):
        os.remove("serialized_patent")

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(patent, setUp=setUp, tearDown=tearDown))
    return tests
