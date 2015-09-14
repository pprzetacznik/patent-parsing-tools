# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
from patent_parsing_tools.utils.log import log

@log
class SimpleClass(object):
    def do_sth(self):
        self.logger.info("sample info")

@log
class AnotherClass(object):
    def do_sth(self):
        self.logger.info("another info")

class TestLogger(unittest.TestCase):
    def test_logger(self):
        SimpleClass().do_sth()
        AnotherClass().do_sth()

if __name__ == '__main__':
    unittest.main()

