import unittest
import doctest
import patent_parsing_tools.patent as patent
import os
from pkg_resources import resource_filename

def setUp():
    print "setup"
    print "setup"
    print "setup"
    print "setup"
    print "setup"
    if os.path.isfile("./serialized_patent"):
        print "istnieje"
    else:
        print "nie ma"
    print os.path.dirname(__file__)
    # print resource_filename("patent_parsing_tools.tests", "US08613112-20131224.XML")
    # print resource_filename("patent_parsing_tools")

def tearDown():
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print "teardown"
    print os.curdir
    if os.path.isfile("./serialized_patent"):
        print "istnieje"
    else:
        print "nie ma"

    # os.remove("serialized_patent")


def load_tests(loader, tests, ignore):
    # tests.addTests(doctest.DocTestSuite(patent, setUp=setUp(), tearDown=tearDown()))
    tests.addTests(doctest.DocTestSuite(patent))
    return tests
