"""A basic Flask application that uses an application factory and a configuration file.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage:
- python -B -m flask --app tracker_03 run
- python -B -m flask --app "tracker_03:create_app(config_name='development')" run
- python -B -m flask --app "tracker_03:create_app('development')" run

> **NOTE** - Enclose options in quotation marks when using special characters.
"""

import logging
import sys

import flask

# Import the runtime configuration file
# The leading dot tells Python that this is a relative import from within the package
from .config import Config, DevConfig, TestConfig

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default') -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
    development, testing, etc. Uses the base `Config` class by default if None

    :return: An application instance
    :rtype: flask.Flask
    """
    # Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    # Ensure the Python version supports Flask 3
    print(f"Your Python version is {_python_version}.")
    if _python_version < 3.08:
        print('Flask 3 requires Python 3.8 or above. Exiting now...')
        sys.exit(1)

    # Create the Flask application instance and get the version number
    app = flask.Flask(__name__)
    _flask_version = flask.__version__

    # Ensure you are using Flask 3
    print(f"Your Flask version is {_flask_version}.")
    if int(_flask_version.split('.')[0]) < 3:
        print('This application requires Flask 3 or above. Exiting now...')
        sys.exit(1)

    # Load the configuration class from config.py based on the environment
    if config_name == 'development':
        app.config.from_object(DevConfig())
    elif config_name == 'testing':
        app.config.from_object(TestConfig())
    else:
        app.config.from_object(Config())

    # Create a route and page
    @app.route('/')
    @app.route('/index')
    def index() -> str:
        """Render the default landing page.

        :return: The HTML code for the page
        :rtype: str
        """
        logging_level = (int)(app.config['LOGGING_LEVEL'])
        logging_level_name = logging.getLevelName(logging_level)

        # DOCTYPE prevents Quirks mode
        greeting = f"""<!DOCTYPE html>
            <h1>Hello, World!</h1>
            <p>Your are using the <b>{config_name}</b> configuration and your logging level is
            <b>{logging_level_name} ({logging_level})</b>.</p>
            """
        return greeting

    # Return the application instance to the code that invoked 'create_app()'
    return app
