import logging
import os


class LoggerUtility:
    @staticmethod
    def get_logger(name=None):
        # Create a logger object
        logger = logging.getLogger(name)

        return logger
