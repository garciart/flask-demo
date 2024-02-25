"""Python class to store configuration variables.

Usage:
- app.config.from_object(Config)
- app.config['LOGGING_LEVEL']
"""
import os


class Config:  # pylint: disable=too-few-public-methods
    """Gets environment variables
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'crsf_protection_key'
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'DEBUG'
