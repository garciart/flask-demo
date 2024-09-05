"""The `__init__.py` serves double duty: it will contain the application factory,
and it tells Python that the current directory should be treated as a package.
You can then import its files as modules (e.g., `from app.foo import bar`).

Usage:
- python -B -m flask --app "v03" run
- python -B -m flask --app "v03:create_app(config_class='v03.config.DevConfig')" run
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import flask
from v03.config import Config, DevConfig, TestConfig

__author__ = "Rob Garcia"


def create_app(config_class: object | str = DevConfig) -> flask.Flask:
    """Application Factory.

    :param str config_class: An alternate configuration from `config.py` for \
    development, testing, etc. Uses the base `Config` class by default if None

    :return: An application instance
    :rtype: flask.Flask
    """
    # Ensure the Python version supports Flask 3
    _python_version = _get_python_version()
    print(f"Your Python version is {_python_version}.")
    if _python_version < 3.08:
        print("Flask 3 requires Python 3.8 or above. Exiting now...")
        sys.exit(0)

    # Create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Set logging to DEBUG (10) just in case the LOGGING_LEVEL variable is not set
    _logging_level = logging.DEBUG

    # This may sound counter-intuitive, but I recommend you do not log events when in debug mode,
    # like if you run `python -m flask --app "app" --debug run`
    # If you run the app in debug mode so you can make hot fixes,
    # you may end up with a huge log file.
    if not app.debug:
        # Attempt to read LOGGING_LEVEL environment variable
        try:
            _logging_level = app.config["LOGGING_LEVEL"]
        except (AttributeError, KeyError):
            pass

        # Start to log events
        _start_log(app, _logging_level)

    app.logger.info("Starting Flask application")

    # Display version info if debugging
    if _logging_level == logging.DEBUG:
        # Use lazy % formatting in logging functions
        app.logger.info("Python version: %s", _python_version)
        app.logger.info("Flask version: %s", flask.__version__)

    @app.route("/")
    @app.route("/index")
    def index():
        """Render the default landing page.

        :return: The HTML code for the page
        :rtype: str
        """
        greeting = f"""<h1>Hello, World!</h1>
        <h2>I am Version 3.</h2>
        <p>From <code>__init__.py</code>: You are using Python {_python_version}.</p>
        <p>From <code>config.py</code>: Your logging level is {app.config['LOGGING_LEVEL']}.</p>
        <p>Check <code>log/blue.log</code> for log entries.</p>
        """
        return greeting

    return app


def _get_python_version() -> float:
    """Get the Python version used by the server.

    :return: The Python version used by the server
    :rtype: float
    """
    # Get Python version and convert to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    return _python_version


def _start_log(app: flask.Flask, logging_level: int = logging.DEBUG) -> None:
    """Setup and start logging in the 'logs' directory.

    NOTE - This may sound counter-intuitive, but if you run the app in debug mode so you can make \
    hot fixes, you may end up with a huge log file. Therefore, I recommend you do not log events \
    when in debug mode (`python3 flask --debug run`)

    :param flask.Flask app: The application instance
    :param int logging_level: The level of messages to log. The default is to log DEBUG \
        messages (level 10) or greater

    :return: None
    """
    # Example entry: 2024-07-09 22:08:25,132-v03-INFO: Starting Flask application
    # [at repos\blue\v03\__init__.py:102]
    _msg_format = (
        "%(asctime)s-%(name)s-%(levelname)s: %(message)s "
        "[at %(pathname)s:%(lineno)d]"
    )

    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Use multiple small logs for easy reading
    file_handler = RotatingFileHandler("logs/blue.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(_msg_format))
    file_handler.setLevel(logging_level)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging_level)
