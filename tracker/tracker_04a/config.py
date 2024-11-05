"""Runtime configuration variables for Flask.

> **WARNING** - This file is not for configuration variables that need to in
place before Flask starts, like FLASK_RUN_PORT. Place those variables in .flaskenv or .env.

Usage:
- app.config.from_object(Config)
- app.config['LOGGING_LEVEL']
"""

import logging

__all__ = ['Config', 'DevConfig']


class Config:
    """Default configuration variables and settings."""

    # WARNING is the default level for the logging module
    LOGGING_LEVEL = logging.WARNING


class DevConfig(Config):
    """Development configuration variables and settings."""

    LOGGING_LEVEL = logging.DEBUG
