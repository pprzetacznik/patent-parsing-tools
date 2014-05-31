# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
from logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger().getLogger("testLogger")
        self.logger.info("setup")

    def tearDown(self):
        pass

    def test_logger(self):
        self.logger = Logger().getLogger("test_loggerMethod()")
        self.logger.debug("debug")
        self.logger.info("informacja")


if __name__ == '__main__':
    unittest.main()
