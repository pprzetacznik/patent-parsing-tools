import logging
from datetime import datetime
import os

class Logger:
    __shared_state = {}
    __register = False

    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.__register:
            self._init_default_register()

    def _init_default_register(self):
        if not os.path.isdir('logs'):
            os.makedirs('logs')
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=datetime.now().strftime('logs/logs_%Y_%m_%d_%H_%M.log'),
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.info("initialized logger")
        Logger.__register = True

    def getLogger(self, filename):
        return logging.getLogger(filename)