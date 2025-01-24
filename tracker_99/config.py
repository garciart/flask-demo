"""Runtime configuration variables for Flask.

> **WARNING** - This file is not for configuration variables that need to in
place before Flask starts, like FLASK_RUN_PORT. Place those variables in .flaskenv or .env.

Usage:
- app.config.from_object(Config)
- app.config['LOGGING_LEVEL']

NOTE - I have included a dictionary of all configuration variables at the bottom of this file
"""

import datetime
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

    # Set default to INFO to capture requests and requesters (for auditing),
    # even though WARNING is the default level for the logging module
    LOGGING_LEVEL = logging.INFO

    # Do not log requests for static content, like images, etc.
    # to reduce the size of the log files
    LOG_STATIC_REQUESTS = False

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
    # Same as: os.environ.get('SECRET_KEY') or 'BACKUP_CSRF_PROTECTION_KEY'
    SECRET_KEY = os.getenv('SECRET_KEY', 'BACKUP_CSRF_PROTECTION_KEY')

    # Ensure CSRF protection is enabled
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Configuration variables and settings for development."""

    CONFIG_MSG = 'You are using the development configuration.'

    # Override default logging level during development
    LOGGING_LEVEL = logging.DEBUG

    # Log requests for everything, including static content, like images, etc.
    # WARNING: This will increase the size of the log files
    LOG_STATIC_REQUESTS = True


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
    PREFERRED_URL_SCHEME = 'http'


CONFIGS = {
    'default': Config,
    'development': DevelopmentConfig,
    'profile': ProfilingConfig,
    'testing': TestingConfig,
}

#################################################
# FOR INFO ONLY: Config variable names and values
#################################################
default_config_vars = {
    'DEBUG': False,
    'TESTING': False,
    'PROPAGATE_EXCEPTIONS': None,
    'SECRET_KEY': None,
    'SECRET_KEY_FALLBACKS': None,
    'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31),
    'USE_X_SENDFILE': False,
    'TRUSTED_HOSTS': None,
    'SERVER_NAME': None,
    'APPLICATION_ROOT': '/',
    'SESSION_COOKIE_NAME': 'session',
    'SESSION_COOKIE_DOMAIN': None,
    'SESSION_COOKIE_PATH': None,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SECURE': False,
    'SESSION_COOKIE_PARTITIONED': False,
    'SESSION_COOKIE_SAMESITE': None,
    'SESSION_REFRESH_EACH_REQUEST': True,
    'MAX_CONTENT_LENGTH': None,
    'MAX_FORM_MEMORY_SIZE': 500000,
    'MAX_FORM_PARTS': 1000,
    'SEND_FILE_MAX_AGE_DEFAULT': None,
    'TRAP_BAD_REQUEST_ERRORS': None,
    'TRAP_HTTP_EXCEPTIONS': False,
    'EXPLAIN_TEMPLATE_LOADING': False,
    'PREFERRED_URL_SCHEME': 'http',
    'TEMPLATES_AUTO_RELOAD': None,
    'MAX_COOKIE_SIZE': 4093,
    'PROVIDE_AUTOMATIC_OPTIONS': True,
}

app_config_vars = {
    'CONFIG_MSG': 'You are using the default configuration.',
    'LOGGING_ENABLED': True,
    'LOGGING_LEVEL': 20,
    'LOG_STATIC_REQUESTS': False,
    'PROFILING_ENABLED': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///tracker.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'WTF_CSRF_ENABLED': True,
}
