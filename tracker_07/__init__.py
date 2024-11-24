"""A Flask application that incorporates performance profiling.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Usage:
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_07:create_app('profiler')" run --without-threads

Changes:
- Added performance profiling.
"""

import logging

import flask

# Import the helper functions
from tracker_07.app_utils import (check_system, validate_input)
# Import the runtime configuration classes
from tracker_07.config import Config, DevConfig, ProfilerConfig
# Import profiler middleware
from tracker_07.profiler import add_profiler_middleware

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default') -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
        development, testing, etc. Uses the base `Config` class if None or 'default'

    :returns: The Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    if not isinstance(config_name, str):
        raise TypeError(
            'The configuration name must be type str. Exiting now...')

    if config_name not in ['default', 'development', 'profiler']:
        raise ValueError(
            'Invalid configuration name. Exiting now...')

    # Ensure the system meets the prerequisites for the application
    check_system(min_python_version=3.08, min_flask_version=3.0)

    # Create the Flask application instance
    _app = flask.Flask(__name__)

    # Create the Flask application instance with the selected configuration
    _app = _configure_app(config_name)

    # Exempt from coverage because the exception cannot be unit tested easily
    try:
        _logging_level = int(_app.config.get('LOGGING_LEVEL', logging.WARNING))
    except ValueError:  # pragma: no cover
        _logging_level = logging.WARNING

    # Get the name of the logging level from config.py
    _logging_level_name = logging.getLevelName(_logging_level)

    # Optionally add the profiler middleware based on configuration
    if _app.config.get('PROFILING_ENABLED', False):
        _app = add_profiler_middleware(_app)

    # Create a route and page
    @_app.route('/')
    @_app.route('/index')
    def index() -> str:
        """Render the default landing page.

        :returns: The HTML code for the page
        :rtype: str
        """
        # DOCTYPE prevents Quirks mode
        _greeting = f"""<!DOCTYPE html>
            <h1>Hello, World!</h1>
            <p>Your are using the <b>{config_name}</b> configuration and your logging level is
            <b>{_logging_level_name} ({_logging_level})</b>.</p>
            """
        return _greeting

    # Return the application instance to the code that invoked 'create_app()'
    return _app


def _configure_app(config_name: str = 'default') -> flask.Flask:
    """Create the Flask application instance with the selected configuration

    :param str config_name: The name of the configuration to use, defaults to 'default'

    :returns: The configured Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('config_name', config_name, str)

    # Create the Flask application instance
    _app = flask.Flask(__name__)

    # Load the configuration class from config.py based on the environment
    # NOTE - Switched from if-elif-else to mapping for readability and maintainability
    config_mapping = {
        'development': DevConfig,
        'profiler': ProfilerConfig,
        'default': Config,
    }

    _app.config.from_object(config_mapping.get(config_name, Config))

    return _app
