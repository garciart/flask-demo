"""The `__init__.py` file makes the `app` directory a package. You can
then import its files as modules (e.g., `from app.foo import bar`).
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import flask
from blue_app.config import Config


__author__ = "Rob Garcia"

DEBUG_FLAG = True


def create_app(alt_config=None):
    # type: (str) -> flask.Flask
    """Application Factory.

    :param str alt_config: An alternate configuration file path for
    testing, etc. Uses blue_app/config.py by default if None

    :return: An application instance
    :rtype: flask.Flask
    """
    # Ensure the Python version supports Flask 3
    _python_version = _get_python_version()

    if _python_version < 3.08:
        print(
            f"Python version is {_python_version}. Flask 3 requires Python 3.8 or above."
        )
        sys.exit(0)

    # Create and configure the app
    app = flask.Flask(__name__)

    # Start logging events
    _start_log(app)

    # Display version info if debugging
    if DEBUG_FLAG == True:
        # Use lazy % formatting in logging functions
        app.logger.info("Python version: %s", _python_version)
        app.logger.info("Flask version: %s", flask.__version__)

    # Load blue_app/config.py if no alternate configuration filename was provided
    if alt_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(alt_config)

    # Test page for http://127.0.0.1:5000/
    @app.route("/")
    def hello():
        return "<h1>Hello, World!</h1>"

    @app.route("/demo")
    def demo():
        return flask.render_template("demo/demo_child.html")

    return app


def _start_log(app):
    # type: (flask.Flask) -> None
    """Setup and start logging into the 'logs' directory.

    NOTE - Do not log if using `flask --debug run`

    :param flask.Flask app: The application instance

    :return: None
    """
    # Do not log if using 'python flask --debug run'
    if not app.debug:
        # Attempt to read LOGGING_LEVEL environment variable
        # Leave at logging.DEBUG (10) if variable does not exist
        _logging_level = 10

        try:
            _logging_level = getattr(logging, app.config["LOGGING_LEVEL"])
        except (AttributeError, KeyError):
            pass

        # Example entry: 2024-07-09 22:08:25,132-blue_app-INFO: Starting Flask application
        # [at repos\blue\blue_app\__init__.py:102]
        _msg_format = (
            "%(asctime)s-%(name)s-%(levelname)s: %(message)s "
            "[at %(pathname)s:%(lineno)d]"
        )

        if not os.path.exists("logs"):
            os.mkdir("logs")

        # Use multiple small logs for easy reading
        file_handler = RotatingFileHandler(
            "logs/blue_app.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(_msg_format))
        file_handler.setLevel(_logging_level)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(_logging_level)
        app.logger.info("Starting Flask application")


def _get_python_version():
    # type: () -> float
    """Get the Python version used by the server.

    :return: The Python version used by the server
    :rtype: float
    """
    # Get Python version and convert to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    return _python_version
