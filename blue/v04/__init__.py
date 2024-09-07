"""The `__init__.py` serves double duty: it will contain the application factory,
and it tells Python that the current directory should be treated as a package.
You can then import its files as modules (e.g., `from app.foo import bar`).

Usage:
- python -B -m flask --app "v04" run
- python -B -m flask --app "v04:create_app(config_class='v04.config.DevConfig')" run
"""

import logging
import os
import socket
import sys
import time
from logging.handlers import RotatingFileHandler

import flask
from v04.config import DevConfig

__author__ = 'Rob Garcia'


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
        print('Flask 3 requires Python 3.8 or above. Exiting now...')
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
            _logging_level = app.config['LOGGING_LEVEL']
        except (AttributeError, KeyError):
            pass

        # Start to log events
        _start_log(app, log_dir='blue_logs', logging_level=_logging_level)

    app.logger.info('Starting Flask application.')

    # Display version info if debugging
    if _logging_level == logging.DEBUG:
        # Use lazy % formatting in logging functions
        app.logger.info("Python version: %s", _python_version)
        app.logger.info("Flask version: %s", flask.__version__)

    @app.route('/')
    @app.route('/index')
    def index():
        """Render the default landing page.

        :return: The HTML code for the page
        :rtype: str
        """
        _log_request(app, flask.request)

        return flask.render_template(
            'main/index.html',
            _python_version=_python_version,
            _logging_level=_logging_level,
        )

    return app


def _get_python_version() -> float:
    """Get the Python version used by the server.

    :return: The Python version used by the server
    :rtype: float
    """
    # Get Python version and convert to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    return _python_version


def _start_log(app: flask.Flask, log_dir: str = 'blue_logs', logging_level: int = logging.DEBUG) -> None:
    """Setup and start logging.

    Each instance of this class to have a separate log file in the 'logs' directory.

    NOTE - This may sound counter-intuitive, but if you run the app in debug mode so you can make \
    hot fixes, you may end up with a huge log file. Therefore, I recommend you do not log events \
    when in debug mode (`python3 flask --debug run`)

    :param flask.Flask app: The application instance
    :param str log_dir: The directory that will hold the log files
    :param int logging_level: The level of messages to log. The default is to log DEBUG \
        messages (level 10) or greater

    :return: None
    """
    # Create the log directory if it does not exist
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    _log_name = f"{app.name}_{time.time()}"
    _log_path = f"{log_dir}/{_log_name}.log"
    # Use multiple small logs for easy reading
    _file_handler = RotatingFileHandler(
        _log_path, mode='a', maxBytes=10240, backupCount=10, encoding='utf-8')

    _file_handler.stream.write('"date_time", "server_ip", "process_id", "msg_level", "message"\n')

    server_hostname = socket.gethostname()
    server_ip_address = socket.gethostbyname(server_hostname)

    # Use CSV format for log entries, with columns for Time, Server IP, Process ID, Message Level, and Message
    # Example entry: "2024-07-09 22:08:25,132", "192.168.56.1", "9132", "INFO", "Starting Flask application."
    _msg_format = f"\"%(asctime)s\", \"{server_ip_address}\", \"%(process)d\", \"%(levelname)s\", \"%(message)s\""
    _formatter = logging.Formatter(_msg_format)
    _file_handler.setFormatter(_formatter)

    app.logger.addHandler(_file_handler)
    app.logger.setLevel(logging_level)

    # IMPORTANT! The name of the log file is the name of the class,
    # plus the time the class was instantiated (MyClass_1725644384.38276.log).
    # Pause for a tenth of a second before creating a new log file
    # to prevent logs from having the same name.
    time.sleep(0.1)


def _log_request(app: flask.Flask, request: flask.Request) -> None:
    """Log information about the client when a page is requested.

    :param flask.Flask app: The application instance
    :param flask.Request request: The client's request object

    :return: None
    """
    client_address = None
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        client_address = request.environ['REMOTE_ADDR']
    else:
        client_address = request.environ['HTTP_X_FORWARDED_FOR']

    app.logger.info(f"{request.endpoint} requested by {client_address}.")
