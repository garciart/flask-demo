"""The `__init__.py` serves double duty: it will contain the application factory,
and it tells Python that the current directory should be treated as a package.
You can then import its files as modules (e.g., `from app.foo import bar`).

Usage:
- python -B -m flask --app "v03" run
- python -B -m flask --app "v03:create_app(config_class='v03.config.DevConfig')" run
"""

import os
import sys

import flask

# Ignore 'imported but unused' messages
from v03.config import Config, DevConfig, TestConfig  # noqa

__author__ = 'Rob Garcia'


def create_app(config_class: object = Config) -> flask.Flask:
    """Application Factory.

    :param str config_class: An alternate configuration from `config.py` for \
    development, testing, etc. Uses the base `Config` class by default if None

    :return: An application instance
    :rtype: flask.Flask
    """
    _flask_version = flask.__version__
    # Get the Python version and convert it to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    # Ensure the Python version supports Flask 3
    print(f"Your Python version is {_python_version}.")
    if _python_version < 3.08:
        print('Flask 3 requires Python 3.8 or above. Exiting now...')
        sys.exit(1)

    # Ensure you are using Flask 3
    print(f"Your Flask version is {_flask_version}.")
    if int(_flask_version.split('.')[0]) < 3:
        print('This application requires Flask 3 or above. Exiting now...')
        sys.exit(1)

    # Create the Flask application instance and use the project's .flaskenv and .env
    app = flask.Flask(__name__, instance_relative_config=True)

    # Load the selected configuration class from config.py
    try:
        app.config.from_object(config_class)
    except ImportError:
        print(f'{config_class} is not a valid configuration class. Exiting now...')
        sys.exit(1)

    # Create a route and page
    @app.route('/')
    @app.route('/index')
    def index() -> str:
        """Render the default landing page.

        :return: The HTML code for the page
        :rtype: str
        """
        # DOCTYPE prevents Quirks mode
        greeting = f"""<!DOCTYPE html>
            <h1>Hello, World!</h1>
            <h2>I am Version 3.</h2>
            <p>From <code>__init__.py</code>: You are using Python {_python_version}.</p>
            <p>From <code>config.py</code>: Your logging level is {app.config['LOGGING_LEVEL']}.</p>
            <p>From <code>.flaskenv</code>: Your port number is {os.environ.get('FLASK_RUN_PORT')}.</p>
            <p>From <code>.env</code>: <samp>EXAMPLE_ENV_VARIABLE</samp>: {os.environ.get('EXAMPLE_ENV_VARIABLE')}</p>
            <p>From <code>config.py</code>: <code>UNDEFINED_KEY</code>: {app.config['UNDEFINED_KEY']}</p>
            """
        return greeting

    # Return the application instance to the code that invoked 'create_app()'
    return app
