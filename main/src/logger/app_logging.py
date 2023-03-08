import logging
import sys
import tempfile
import os

global IS_SETUP
IS_SETUP = False


def init_logger():
    print("Initializing logger basic configuration")
    global IS_SETUP

    fd, fname = tempfile.mkstemp()
    directory = os.path.dirname(fname)
    logfilepath = directory + '/' + 'app.log'

    logging_params = {
        'level': logging.DEBUG,
        'format': '%(asctime)s [%(process)d] [%(threadName)s] [%(levelname)s] [%(module)s.%(funcName)s](%(name)s)[L%(lineno)d] %(message)s',
        'handlers': [
            logging.FileHandler(logfilepath),
            logging.StreamHandler(sys.stdout)
        ]
    }

    logging.root.handlers = []
    logging.basicConfig(**logging_params)

    IS_SETUP = True

    logging.debug("successfully initialized configuration of logging")


def getlogger(loggername, level=logging.DEBUG):
    if IS_SETUP == False:
        init_logger()

    logger = logging.getLogger(loggername)
    logger.setLevel(level)

    return logger


if __name__ == '__main__':
    log = getlogger('test')
    log.debug('working?')
