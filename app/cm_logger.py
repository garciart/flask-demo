"""Logging handler for Class Manager

Usage:
from app import cm_logger
logger = cm_logger.create_logger('cm_logger', logging.DEBUG)
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from app.cm_utils import validate_input

FORMATTER = logging.Formatter(
    '%(asctime)s-%(name)s-%(levelname)s-%(message)s')
LOG_FILE = 'cm.log'


def _create_console_handler():
    # type: () -> logging.StreamHandler
    """Configure displaying log messages to the screen.

    :returns: The configured console handler
    :rtype: StreamHandler
    """
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(FORMATTER)
    return _console_handler


def _create_file_handler():
    # type: () -> RotatingFileHandler
    """Configure saving log messages to a file.

    :returns: The configured file handler
    :rtype: RotatingFileHandler
    """
    _file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2048,
                                        backupCount=5)
    _file_handler.setFormatter(FORMATTER)
    return _file_handler


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
    validate_input('logger_name', logger_name, str)
    validate_input('logging_level', logging_level, int)

    _logger = logging.getLogger(logger_name)
    _logger.setLevel(logging_level)
    _logger.addHandler(_create_console_handler())
    _logger.addHandler(_create_file_handler())
    # Set to true if you want messsages to appear in system log as well
    _logger.propagate = False
    return _logger
