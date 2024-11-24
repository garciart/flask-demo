"""Runtime configuration variables for Flask.

> **WARNING** - This file is not for configuration variables that need to in
place before Flask starts, like FLASK_RUN_PORT. Place those variables in .flaskenv or .env.

Usage:
- app.config.from_object(Config)
- app.config['LOGGING_LEVEL']
"""

import logging

__all__ = ['Config', 'DevConfig', 'ProfilerConfig']


class Config:
    """Default configuration variables and settings."""

    # WARNING is the default level for the logging module
    LOGGING_LEVEL = logging.WARNING


class DevConfig(Config):
    """Configuration variables and settings for development."""

    LOGGING_LEVEL = logging.DEBUG


class ProfilerConfig(Config):
    """Configuration variables and settings for profiling."""

    LOGGING_LEVEL = logging.DEBUG

    # Set this to True to enable profiling
    PROFILING_ENABLED = True
