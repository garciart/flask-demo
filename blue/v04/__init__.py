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
from v04.config import *

__author__ = 'Rob Garcia'


def create_app(config_class: object = DevConfig) -> flask.Flask:
    """Application Factory.

    :param str config_class: An alternate configuration from `config.py` for \
    development, testing, etc. Uses the base `Config` class by default if None

    :return: An application instance
    :rtype: flask.Flask
    """
    _flask_version = flask.__version__
    # Get the Python version and convert it to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")
    # Set logging to DEBUG (10) just in case the LOGGING_LEVEL environment variable is not set
    _logging_level = logging.DEBUG

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

    # Create the Flask application instance
    app = flask.Flask(__name__, instance_relative_config=True)

    # Load the selected configuration class from config.py
    try:
        app.config.from_object(config_class)
    except ImportError:
        print(f'{config_class} is not a valid configuration class. Exiting now...')
        sys.exit(1)

    # Attempt to read LOGGING_LEVEL environment variable
    # Use the default value if environment value does not exist
    try:
        _logging_level = app.config['LOGGING_LEVEL']
    except (AttributeError, KeyError):
        app.config['LOGGING_LEVEL'] = _logging_level

    # Start to log events
    # This may sound counter-intuitive, but I recommend you do not save log events
    # to a file when running the application in debug mode,
    # like if you run `python -m flask --app "app" run --debug`
    # If you run the app in debug mode so you can make hot fixes,
    # you may end up with a huge log file.
    if not app.debug:
        _start_log_file(app, log_dir='blue_logs', logging_level=app.config['LOGGING_LEVEL'])

    # Log events will still appear in the console
    app.logger.info('Starting Flask application.')
    # Use lazy % formatting in logging functions
    app.logger.info("Python version: %s", _python_version)
    app.logger.info("Flask version: %s", _logging_level)

    @app.route('/')
    @app.route('/index')
    def index() -> str:
        """Render the default landing page.

        :return: The HTML code for the page
        :rtype: str
        """
        log_page_request(app, flask.request)

        return flask.render_template(
            'main/index.html',
            _python_version=_python_version,
            _logging_level=_logging_level,
        )

    # Return the application instance to the code that invoked 'create_app()'
    return app


def _start_log_file(app: flask.Flask, log_dir: str = 'blue_logs', logging_level: int = logging.DEBUG) -> None:
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
    # Validate inputs
    validate_input('app', app, flask.Flask)
    validate_input('log_dir', log_dir, str)
    validate_input('logging_level', logging_level, int)

    # Create the log directory if it does not exist
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # The name of the log file is the name of the class,
    # plus the time the class was instantiated (MyClass_1725644384.38276.log).
    _log_name = f"{app.name}_{time.time()}"
    _log_path = f"{log_dir}/{_log_name}.log"

    # Use multiple small logs for easy reading
    _file_handler = RotatingFileHandler(
        _log_path, mode='a', maxBytes=10240, backupCount=10, encoding='utf-8')

    # Use CSV format for log entries, with columns for Time, Server IP, Process ID, Message Level, and Message
    _file_handler.stream.write('"date_time", "server_ip", "process_id", "msg_level", "message"\n')

    server_hostname = socket.gethostname()
    server_ip_address = socket.gethostbyname(server_hostname)

    # Example entry: "2024-07-09 22:08:25,132", "192.168.56.1", "9132", "INFO", "Starting Flask application."
    _msg_format = f"\"%(asctime)s\", \"{server_ip_address}\", \"%(process)d\", \"%(levelname)s\", \"%(message)s\""
    _formatter = logging.Formatter(_msg_format)
    _file_handler.setFormatter(_formatter)

    app.logger.addHandler(_file_handler)
    app.logger.setLevel(logging_level)

    # IMPORTANT! Since the timestamp is part of the log file name,
    # pause for a tenth of a second before leaving to prevent logs from having the same name.
    time.sleep(0.1)


def validate_input(obj_name: str, obj_to_check: object, expected_type: type) -> None:
    """Validate an input's type and ensure it is not empty.

    Use this function to reduce code complexity in calling functions and methods.

    :param str obj_name: The name of the input to validate
    :param object obj_to_check: The input to validate
    :param type expected_type: The expected type for the input

    :return: None
    """
    # Validate inputs for this function
    if not isinstance(obj_name, str):
        print('obj_name must be type <str>. Exiting now...')
        sys.exit(2)

    if not isinstance(expected_type, type | tuple):
        print('expected_type must be type <type> or a tuple of types. Exiting now...')
        sys.exit(2)

    # Validate inputs for the calling function
    if not isinstance(obj_to_check, expected_type):
        print(f"'{obj_name}' is not type {expected_type}. Exiting now...")
        sys.exit(2)

    if isinstance(obj_to_check, str) and obj_to_check == '':
        print(f"'{obj_name}' is empty. Exiting now...")
        sys.exit(2)

    if isinstance(obj_to_check, (str, list, dict)) and len(obj_to_check) == 0:
        print(f"'{obj_name}' is empty. Exiting now...")
        sys.exit(2)


def log_page_request(app: flask.Flask, request: flask.Request) -> None:
    """Log information about the client when a page is requested.

    :param flask.Flask app: The application instance
    :param flask.Request request: The client's request object

    :return: None
    """
    # Validate inputs
    validate_input('app', app, flask.Flask)
    validate_input('request', request, flask.Request)

    client_address = None
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        client_address = request.environ['REMOTE_ADDR']
    else:
        client_address = request.environ['HTTP_X_FORWARDED_FOR']

    # Log the requested page and client address
    app.logger.info(f"{request.endpoint} requested by {client_address}.")
