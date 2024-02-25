"""Logging handler for Class Manager

Usage:
from app import app, cm_logger
logger = cm_logger.create_logger("cm_logger")
"""
import logging
import sys
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter(
    '%(asctime)s-%(name)s-%(levelname)s-%(message)s')
LOG_FILE = "cm.log"


def _create_console_handler():
    # type: () -> logging.StreamHandler
    """Configure displaying log messages to the screen.

    :returns: The configured console handler
    :rtype: StreamHandler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def _create_file_handler():
    # type: () -> RotatingFileHandler
    """Configure saving log messages to a file.

    :returns: The configured file handler
    :rtype: RotatingFileHandler
    """
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2048,
                                       backupCount=5)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def create_logger(logger_name, logging_level):
    # type: (str, int) -> logging.Logger
    """Configure logging (display and file).

    :param str logger_name: The name of the logging handler
    :param int logging_level: The integer representation of the logging level
    (e.g., logging.DEBUG = 10)

    :return: The configured logging handler
    :rtype: logging.Logger
    """
    # Validate inputs
    if not isinstance(logger_name, str):
        raise TypeError('logger_name must be type <str>.')

    if not isinstance(logging_level, int):
        raise TypeError('logging_level must be type <int>.')

    if isinstance(logger_name, str) and (
            logger_name == '' or len(logger_name) == 0):  # noqa E125
        raise ValueError(f"'{logger_name}' is empty.")

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    print(logging_level)
    logger.addHandler(_create_console_handler())
    logger.addHandler(_create_file_handler())
    logger.propagate = False
    return logger
