"""Helper functions
"""

import importlib
import logging
import os
import socket
import sys
import time
from logging.handlers import RotatingFileHandler
from types import UnionType

import flask

__all__ = ['validate_input', 'check_system', 'start_log_file', 'log_page_request']


def validate_input(obj_name: str, obj_to_check: object,
                   expected_type: type | tuple | UnionType) -> None:
    """Validate an input's type and ensure it is not empty.

    Use this function to reduce code complexity in calling functions and methods.

    :param str obj_name: The name of the input to validate
    :param object obj_to_check: The input to validate
    :param type/tuple/UnionType expected_type: The expected type or list of types for the input

    :returns: None
    :rtype: None
    """
    if not isinstance(obj_to_check, expected_type):
        raise TypeError(f"'{obj_name}' is not type {expected_type}. Exiting now...")

    if isinstance(obj_to_check, (str, list, dict)) and len(obj_to_check) == 0:
        raise ValueError(f"'{obj_name}' is empty. Exiting now...")


def check_system(min_python_version: float = 3.08, min_flask_version: float = 3.0) -> None:
    """Check if the installed Python and Flask versions can run the application.

    **NOTE** - Use `3.01` for version `3.1` and `3.10` for version `3.10`.

    :param float min_python_version: The minimum Python version in float format, defaults to 3.08
    :param float min_flask_version: The minimum Flask version in float format, defaults to 3.0

    :returns: None
    :rtype: None
    """
    # Validate inputs
    validate_input('min_python_version', min_python_version, float)
    validate_input('min_flask_version', min_python_version, float)

    if min_python_version <= 0.0 or min_flask_version <= 0.0:
        raise ValueError(
            'The minimum Python and Flask version numbers must be greater than 0. Exiting now...'
        )

    # Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    # Ensure you are using the correct version of Python
    print(f"Your Python version is {_python_version}.")
    if _python_version < min_python_version:
        raise ValueError(
            f"Flask 3 requires Python {min_python_version:.2f} or above. Exiting now..."
        )

    # Get the Flask major and minor version numbers and convert them to a float
    _raw_flask_version = importlib.metadata.version("flask")
    _flask_version_major, _flask_version_minor = map(int, _raw_flask_version.split('.')[:2])
    _flask_version = float(f"{_flask_version_major}.{_flask_version_minor:02d}")

    # Ensure you are using the correct version of Flask
    print(f"Your Flask version is {_raw_flask_version}.")
    if float(_flask_version) < min_flask_version:
        raise ValueError(
            f"This application requires Flask {min_flask_version:.2f} or above. Exiting now..."
        )


def start_log_file(
        app: flask.Flask, log_dir: str = 'tracker_logs', logging_level: int = logging.DEBUG
) -> None:
    """Setup and start logging.

    Each instance of this class to have a separate log file in the 'logs' directory.

    **NOTE** - This may sound counter-intuitive, but if you run the app in debug mode, so you can \
    make hot fixes, you may end up with a huge log file. Therefore, I recommend you do not log \
    events when in debug mode (`python flask --debug run`)

    :param flask.Flask app: The application instance
    :param str log_dir: The directory that will hold the log files
    :param int logging_level: The level of messages to log. The default is to log DEBUG \
        messages (level 10) or greater

    :returns: None
    :rtype: None
    """
    # Validate inputs
    validate_input('app', app, flask.Flask)
    validate_input('log_dir', log_dir, str)
    validate_input('logging_level', logging_level, int)

    # Create the log directory if it does not exist
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # The name of the log file is the name of the instance,
    # plus the time the instance was instantiated (tracker_10_1234567890.1234567.log).
    _log_name = f"{app.name}_{time.time()}"
    _log_path = f"{log_dir}/{_log_name}.log"

    # Use multiple small logs for easy reading
    _file_handler = RotatingFileHandler(
        _log_path, mode='a', maxBytes=10240, backupCount=10, encoding='utf-8'
    )

    _server_hostname = socket.gethostname()
    _server_ip_address = socket.gethostbyname(_server_hostname)

    # Use CSV format for log entries, with columns for Time, Server IP, Process ID, Message Level,
    # and Message
    # Example entry: "2024-07-09 22:08:25,132", "192.168.56.1", "9132", "INFO",
    # "Starting Flask application."
    _msg_format = (
        f"\"%(asctime)s\", \"{_server_ip_address}\", \"%(process)d\", \"%(levelname)s\", "
        f"\"%(message)s\""
    )
    _formatter = logging.Formatter(_msg_format)
    _file_handler.setFormatter(_formatter)
    app.logger.addHandler(_file_handler)

    # Write CSV column names to the start of the log
    _file_handler.stream.write('"date_time", "server_ip", "process_id", "msg_level", "message"\n')

    # Get the name of the logging level from config.py
    _logging_level_name = logging.getLevelName(logging_level)

    # Record an INFO level message before using the logging level from config.py
    app.logger.setLevel(logging.INFO)

    # Use lazy % formatting in logging functions
    # NOTE - Log events will still appear in the console
    app.logger.info('Starting %s application; setting logging level to %s.',
                    __package__, _logging_level_name)

    # Set logging to the logging level from config.py
    app.logger.setLevel(logging_level)

    # IMPORTANT! Since the timestamp is part of the log file name,
    # pause for a tenth of a second before leaving to prevent logs from having the same name
    time.sleep(0.1)


def log_page_request(app: flask.Flask, request: flask.Request, response: flask.Response) -> None:
    """Log information about the client when a page is requested.

    :param flask.Flask app: The application instance
    :param flask.Request request: The client's request object
    :param flask.Response response: The server's response object

    :returns: None
    :rtype: None
    """
    # Validate inputs
    validate_input('app', app, flask.Flask)
    validate_input('request', request, flask.Request)
    validate_input('response', response, flask.Response)

    # Get the address of the requester
    _client_address = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ['REMOTE_ADDR']

    # Log the requested page and client address
    app.logger.info(
        f"{request.path} requested by {_client_address} using {request.method}; "
        f"{response.status}."
    )
