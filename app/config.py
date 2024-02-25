import os


class Config:
    """Gets environment variables
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'crsf_protection_key'
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'DEBUG'
