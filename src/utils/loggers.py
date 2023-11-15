import logging
import os

import coloredlogs


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerUtility(metaclass=Singleton):
    def __init__(self, name=None):
        # Create a logger object
        self.logger = logging.getLogger(name)

        # Set log level to debug

        # Create console handler with a higher log level
        ch = logging.StreamHandler()

        # Create formatter and add it to the handlers
        formatter = coloredlogs.ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s: %(message)s | %(type)s | %(value)s | %(location)s ",
            level_styles={
                "debug": {"color": "cyan"},
                "info": {"color": "green"},
                "warning": {"color": "yellow"},
                "error": {"color": "red"},
                "critical": {"color": "red", "bold": True},
            },
            field_styles={
                "asctime": {"color": "white"},
                "name": {"color": "blue"},
                "type": {"color": "green"},
                "value": {"color": "magenta"},
                "location": {"color": "white", "bright": True},
                "message": {"color": "white"},
            },
        )
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
