"""Python class to store configuration variables.

Usage:
- app.config.from_object(Config)
- app.config['LOGGING_LEVEL']
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:  # pylint: disable=too-few-public-methods
    """Gets environment variables
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'crsf_protection_key'
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'DEBUG'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
