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


class DevelopmentConfig(Config):
    """Configuration variables and settings for development."""

    CONFIG_MSG = 'You are using the development configuration.'


CONFIGS = {
    'default': Config,
    'development': DevelopmentConfig,
}
