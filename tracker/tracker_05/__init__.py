"""A Flask application that incorporates logging.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage:
- python -B -m flask --app "tracker_05:create_app(config_name='development', log_events=True)" run
- python -B -m flask --app "tracker_05:create_app('development', True)" run

> **NOTE** - Enclose options in quotation marks when using special characters.

Changes:
- Replaced `import config`. Importing occurs on demand in the `_configure_app` method
- Replaced configuration if-elif-else with mapping for readability and maintainability
- Consolidated input validation in the `validate_input` method
- Added logging
"""

import importlib
import logging
from logging.handlers import RotatingFileHandler
import os
import socket
import sys
import time

import flask

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default', log_events: bool = False) -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
        development, testing, etc. Uses the base `Config` class if None or 'default'

    :returns: The Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('config_name', config_name, str)
    validate_input('config_name', log_events, bool)

    if config_name not in ['default', 'development']:
        raise ValueError(
            'Invalid configuration name. Exiting now...')

    # Ensure the system meets the prerequisites for the application
    _check_system()

    # Create the Flask application instance with the selected configuration
    _app = _configure_app(config_name)

    try:
        _logging_level = int(_app.config.get('LOGGING_LEVEL', logging.WARNING))
    except ValueError:
        _logging_level = logging.WARNING

    _logging_level_name = logging.getLevelName(_logging_level)


    # This may sound counter-intuitive, but I recommend you do not save log events
    # to a file when running the application in debug mode,
    # like if you run `python -m flask --app "app" run --debug`
    # If you run the app in debug mode so you can make hot fixes,
    # you may end up with a huge log file.
    if _app.debug:
        log_events = False

    # Start to log events
    if log_events:
        _start_log_file(_app, log_dir='tracker_logs', logging_level=_logging_level)

        # Log events will still appear in the console
        # Use lazy % formatting in logging functions
        _app.logger.info('Starting %s application at logging level %s.',
                         __package__, _logging_level_name)

        @_app.after_request
        def log_response_code(response):
            # Capture the request and the response
            log_page_request(_app, flask.request, response)

            # Do not forget to return the response to the client, or the app will crash
            return response

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
    if int(_flask_version) < min_flask_version:
        raise ValueError(
            f"This application requires Flask {min_flask_version:.2f} or above. Exiting now..."
        )


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
        'development': f'{__package__}.config.DevConfig',
        'default': f'{__package__}.config.Config'
    }

    _app.config.from_object(config_mapping.get(config_name, config_mapping['default']))

    return _app


def validate_input(obj_name: str, obj_to_check: object, expected_type: type) -> None:
    """Validate an input's type and ensure it is not empty.

    Use this function to reduce code complexity in calling functions and methods.

    :param str obj_name: The name of the input to validate
    :param object obj_to_check: The input to validate
    :param type expected_type: The expected type for the input

    :returns: None
    :rtype: None
    """
    if not isinstance(obj_to_check, expected_type):
        raise TypeError(f"'{obj_name}' is not type {expected_type}. Exiting now...")

    if isinstance(obj_to_check, (str, list, dict)) and len(obj_to_check) == 0:
        raise ValueError(f"'{obj_name}' is empty. Exiting now...")


def _start_log_file(
    app: flask.Flask, log_dir: str = 'tracker_logs', logging_level: int = logging.DEBUG
) -> None:
    """Setup and start logging.

    Each instance of this class to have a separate log file in the 'logs' directory.

    **NOTE** - This may sound counter-intuitive, but if you run the app in debug mode so you can \
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
    # plus the time the instance was instantiated (tracker_05_1234567890.1234567.log).
    _log_name = f"{app.name}_{time.time()}"
    _log_path = f"{log_dir}/{_log_name}.log"

    # Use multiple small logs for easy reading
    _file_handler = RotatingFileHandler(
        _log_path, mode='a', maxBytes=10240, backupCount=10, encoding='utf-8'
    )

    # Use CSV format for log entries, with columns for Time, Server IP, Process ID, Message Level,
    # and Message
    _file_handler.stream.write('"date_time", "server_ip", "process_id", "msg_level", "message"\n')

    _server_hostname = socket.gethostname()
    _server_ip_address = socket.gethostbyname(_server_hostname)

    # Example entry: "2024-07-09 22:08:25,132", "192.168.56.1", "9132", "INFO",
    # "Starting Flask application."
    _msg_format = (
        f"\"%(asctime)s\", \"{_server_ip_address}\", \"%(process)d\", \"%(levelname)s\", "
        f"\"%(message)s\""
    )
    _formatter = logging.Formatter(_msg_format)
    _file_handler.setFormatter(_formatter)

    app.logger.addHandler(_file_handler)
    app.logger.setLevel(logging_level)

    # IMPORTANT! Since the timestamp is part of the log file name,
    # pause for a tenth of a second before leaving to prevent logs from having the same name.
    time.sleep(0.1)


def log_page_request(app: flask.Flask, request: flask.Request, response: flask.Response) -> None:
    """Log information about the client when a page is requested.

    :param flask.Flask app: The application instance
    :param flask.Request request: The client's request object
    :param flask.Request request: The server's response object

    :returns: None
    :rtype: None
    """
    # Validate inputs
    validate_input('app', app, flask.Flask)
    validate_input('request', request, flask.Request)
    validate_input('response', response, flask.Response)

    _client_address = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ['REMOTE_ADDR']

    # Log the requested page and client address
    app.logger.info(
        f"{request.path} requested by {_client_address} using {request.method}; "
        f"{response.status}."
    )
