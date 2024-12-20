"""Runtime configuration variables for Flask.

**WARNING** - This file is not for configuration variables that need to in
place before Flask starts, like FLASK_RUN_PORT. Place those variables in .flaskenv or .env.

Usage:
- app.config.from_object(Config)
- app.config['CONFIG_MSG']
"""

__all__ = ['CONFIGS']


class Config:
    """Default configuration variables and settings."""

    CONFIG_MSG = 'You are using the default configuration.'

    # Return error pages, instead of the stack trace, when not testing
    TESTING = False

    # Set profiling to false by default
    PROFILING_ENABLED = False


class DevelopmentConfig(Config):
    """Configuration variables and settings for development."""

    CONFIG_MSG = 'You are using the development configuration.'


class ProfilingConfig(Config):
    """Configuration variables and settings for profiling."""

    CONFIG_MSG = 'You are using the profiling configuration.'

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
