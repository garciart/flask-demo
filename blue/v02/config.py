"""Python class to store configuration variables.

Usage:
- app.config.from_object(Config)
- app.config['LOGGING_LEVEL']
"""

import os
import logging
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Default configuration variables and settings."""

    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or "A default CRSF protection key if none is set in the OS environment."
    )
    UNDEFINED_KEY = (
        os.environ.get("EXTRA_KEY")
        or "This is an example of a config.py variable Flask will use if a variable by the same name is not set in the OS environment, .env, or .flaskenv."
    )
    # WARNING is the default logging level
    LOGGING_LEVEL = logging.WARNING


class DevConfig(Config):
    """Development configuration variables and settings."""

    LOGGING_LEVEL = logging.DEBUG


class TestConfig(Config):
    """Test configuration variables and settings."""

    LOGGING_LEVEL = logging.INFO
