"""Runtime configuration variables for Flask.

> **WARNING** - This file is not for configuration variables that need to in
place before Flask starts, like FLASK_RUN_PORT. Place those variables in .flaskenv or .env.

Usage:
- app.config.from_object(Config)
- app.config['LOGGING_LEVEL']
"""

import logging
import os

__all__ = ['CONFIGS']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Default configuration variables and settings."""

    # Explicitly default to False to prevent enabling debug mode when deploying to production
    DEBUG = False

    CONFIG_MSG = 'You are using the default configuration.'

    # Explicitly default to True to ensure rotating logs on production servers
    LOGGING_ENABLED = True

    # Explicitly default to WARNING,
    # even though WARNING is the default level for the logging module
    LOGGING_LEVEL = logging.WARNING

    # Return error pages, instead of the stack trace, when not testing
    TESTING = False

    # Set profiling to false by default
    PROFILING_ENABLED = False

    # Get the database location from the environment or, if undefined,
    # use the test database
    # Same as:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
    #         'sqlite:///' + os.path.join(basedir, 'tracker.db')
    # )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'tracker.db')
    )

    # Disable Flask-SQLAlchemy event notification system to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Get the secret key from the environment or, if undefined,
    # use a default value to protect against Cross-site request forgery (CRSF) attacks
    # Always include a default value, since unittest cannot get values from .env and .flaskenv
    # Same as: os.environ.get('SECRET_KEY') or 'default_secret_key'
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Ensure CSRF protection is enabled
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Configuration variables and settings for development."""

    CONFIG_MSG = 'You are using the development configuration.'

    # Override default logging level during development
    LOGGING_LEVEL = logging.DEBUG


class ProfilingConfig(Config):
    """Configuration variables and settings for profiling."""

    CONFIG_MSG = 'You are using the profiling configuration.'

    # Do not log events when profiling,
    # unless you want to see if logging causes bottlenecks
    # Override the setting using `create_app(log_events=True)`
    LOGGING_ENABLED = False

    # Profile the application
    PROFILING_ENABLED = True


class TestingConfig(Config):
    """Configuration variables and settings for testing."""

    CONFIG_MSG = 'You are using the testing configuration.'

    # Do not log events when unit testing
    # The tests will create multiple instances of the application,
    # resulting in empty log files
    LOGGING_ENABLED = False

    # Return the stack trace, instead of error pages, when testing
    TESTING = True

    # Disable CSRF protection when testing to avoid:
    # `RuntimeError: Working outside of request context` errors
    WTF_CSRF_ENABLED = False

    SERVER_NAME = '127.0.0.1:5000'
    PREFERRED_URL_SCHEME = 'https'


CONFIGS = {
    'default': Config,
    'development': DevelopmentConfig,
    'profile': ProfilingConfig,
    'testing': TestingConfig,
}
