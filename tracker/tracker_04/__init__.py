"""A Flask application that incorporates unit testing.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage:
- python -B -m flask --app tracker_04 run
- python -B -m unittest --verbose --buffer tracker_04/tests/test_app.py

Changes:
- Added unit tests.
"""

import importlib
import logging
import sys

import flask

# The leading dot tells Python that this is a relative import from within the package
# Import the runtime configuration classes
from .config import Config, DevConfig

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default') -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
        development, testing, etc. Uses the base `Config` class if None or 'default'
    :param bool log_events: Flag to start the logger, defaults to False

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
    _check_system(min_python_version=3.08, min_flask_version=3.0)

    # Create the Flask application instance
    _app = flask.Flask(__name__)

    # Load the configuration class from config.py based on the environment
    # NOTE - Will replace if-elif-else with mapping for readability and maintainability
    if config_name == 'development':
        _app.config.from_object(DevConfig())
    else:
        _app.config.from_object(Config())

    try:
        _logging_level = int(_app.config.get('LOGGING_LEVEL', logging.WARNING))
    except ValueError:
        _logging_level = logging.WARNING

    _logging_level_name = logging.getLevelName(_logging_level)

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


def _check_system(min_python_version: float = 3.08, min_flask_version: float = 3.0) -> None:
    """Check if the installed Python and Flask versions can run the application.

    **NOTE** - Use `3.01` for version `3.1` and `3.10` for version `3.10`.

    :param float min_python_version: The minimum Python version in float format, defaults to 3.08
    :param float min_flask_version: The minimum Flask version in float format, defaults to 3.0

    :returns: None
    :rtype: None
    """
    # Validate inputs
    if not isinstance(min_python_version, float) or not isinstance(min_flask_version, float):
        raise TypeError(
            'The minimum Python and Flask version numbers must be type float. Exiting now...')

    if min_python_version <= 0.0 or min_flask_version <= 0.0:
        raise ValueError(
            'The minimum Python and Flask version numbers must be greater than 0. Exiting now...')

    # Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    # Ensure you are using the correct version of Python
    print(f"Your Python version is {_python_version}.")
    if _python_version < min_python_version:
        raise ValueError(
            f"Flask 3 requires Python {min_python_version:.2f} or above. Exiting now...")

    # Get the Flask major and minor version numbers and convert them to a float
    _raw_flask_version = importlib.metadata.version("flask")
    _flask_version_major, _flask_version_minor = map(int, _raw_flask_version.split('.')[:2])
    _flask_version = float(f"{_flask_version_major}.{_flask_version_minor:02d}")

    # Ensure you are using the correct version of Flask
    print(f"Your Flask version is {_raw_flask_version}.")
    if _flask_version < min_flask_version:
        raise ValueError(
            f"This application requires Flask {min_flask_version:.2f} or above. Exiting now...")
