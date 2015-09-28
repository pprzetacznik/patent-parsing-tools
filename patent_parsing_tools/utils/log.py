# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
from datetime import datetime
import os
import time
from functools import wraps


class Logger:
    __register = False

    def __init__(self):
        if not self.__register:
            self._init_default_register()

    def _init_default_register(self):
        if not os.path.isdir('logs'):
            os.makedirs('logs')
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=datetime.now().strftime('logs/logs_%Y_%m_%d_%H_%M.log'),
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.info("Logger initialized")
        Logger.__register = True

    def get_logger(self, filename):
        return logging.getLogger(filename)

def log(cls):
    cls.logger = Logger().get_logger(cls.__name__)
    return cls

def log_timer(fn):
    @wraps(fn)
    def helper(*args, **kw):
        start = time.time()
        result = fn(*args, **kw)
        args[0].logger.info("Invoking method %s() took %fs" % (fn.__name__, (time.time() - start)))
        return result
    return helper
