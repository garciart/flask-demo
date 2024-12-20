"""Runtime configuration variables for Flask.

**WARNING** - This file is not for configuration variables that need to in
place before Flask starts, like FLASK_RUN_PORT. Place those variables in .flaskenv or .env.

Usage:
- app.config.from_object(Config)
- app.config['CONFIG_MSG']
"""

import logging

__all__ = ['CONFIGS']


class Config:
    """Default configuration variables and settings."""

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


CONFIGS = {
    'default': Config,
    'development': DevelopmentConfig,
    'profile': ProfilingConfig,
    'testing': TestingConfig,
}
