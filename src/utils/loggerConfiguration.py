from threading import Lock
import logging
import sys


class LoggerMeta(type):
    """
    Logger with thread safer implementation
    """

    _instance = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instance:
                instance = super().__call__(*args, **kwargs)
                cls._instance[cls] = instance

        return cls._instance[cls]


class Logger(metaclass=LoggerMeta):
    logger = None

    def __init__(self):
        self.logger = logging.getLogger('GENERAL')
        logger_handler = logging.StreamHandler(stream=sys.stdout)
        logger_handler.setLevel(logging.DEBUG)
        logger_format = logging.Formatter('[%(levelname)s] %(asctime)s | Method: %(funcName)s - %(name)s | %(message)s')
        logger_handler.setFormatter(logger_format)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logger_handler)


def configure_logger_format(logger_name):
    logger = logging.getLogger(logger_name)
    logger_format = logging.Formatter('[%(levelname)s] %(asctime)s | Method: %(funcName)s - %(name)s | %(message)s')
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    logger_handler.setFormatter(logger_format)
    logger.addHandler(logger_handler)