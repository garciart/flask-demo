"""A Flask application that incorporates templates.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage:
- python -B -m flask --app tracker_11 run
- python -B -m flask --app "tracker_11:create_app('development', True)" run
> **NOTE** - Enclose options in quotation marks when using special characters.

> **NOTE** - Do not log events when unit testing or each test will create a log file.

Changes:
- Moved pages into templates
- Added a "master" layout page
- Added static Cascading Style Sheets (CSS) and JavaScript files
"""

import logging
import os

import flask
from flask_sqlalchemy import SQLAlchemy

from tracker.tracker_11.app_utils import validate_input, check_system, start_log_file, log_page_request
# Import the runtime configuration classes
from tracker.tracker_11.config import Config, DevConfig, ProfilerConfig
# Import the profiling middleware
from tracker.tracker_11.profiler import add_profiler_middleware

__author__ = 'Rob Garcia'

# Create an instance of the SQLAlchemy class
db = SQLAlchemy()


def create_app(config_name: str = 'default', log_events: bool = False) -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
        development, testing, etc. Uses the base `Config` class if None or 'default'
    :param bool log_events: Flag to start the logger, defaults to False

    :returns: The Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('config_name', config_name, str)
    validate_input('config_name', log_events, bool)

    if config_name not in ['default', 'development', 'profiler']:
        raise ValueError(
            'Invalid configuration name. Exiting now...')

    # Ensure the system meets the prerequisites for the application
    check_system()

    # Create the Flask application instance with the selected configuration
    _app = _configure_app(config_name)

    # Ensure a logging level is set
    try:
        _logging_level = int(_app.config.get('LOGGING_LEVEL', logging.WARNING))
    except ValueError:
        _logging_level = logging.WARNING

    # This may sound counter-intuitive, but I recommend you do not save log events
    # to a file when running the application in debug mode,
    # like if you run `python -m flask --app "app" run --debug`
    # If you run the app in debug mode, so you can make hot fixes,
    # you may end up with a huge log file.
    if _app.debug:
        log_events = False

    # Start to log events
    if log_events:
        # Start the log at logging.INFO to enter application starting messages
        start_log_file(_app, log_dir='tracker_logs', logging_level=_logging_level)

        @_app.after_request
        def log_response_code(response):
            # Capture the request and the response
            log_page_request(_app, flask.request, response)

            # Do not forget to return the response to the client, or the app will crash
            return response

    # Get the name of the logging level from config.py
    _logging_level_name = logging.getLevelName(_logging_level)

    # Optionally add the profiler middleware based on configuration
    if _app.config.get("PROFILING_ENABLED", False):
        _app = add_profiler_middleware(_app)

    # Initialize the database with the app
    db.init_app(_app)

    # Create the database if it does not exist
    with _app.app_context():
        # Lazy import to avoid circular imports
        from tracker.tracker_11.models.create_db import create_db

        # Extract database file path from the URI
        uri = db.engine.url
        db_path = uri.database if uri.database else uri.host

        if not os.path.exists(db_path):
            create_db()

    # Start routing using blueprints
    # Import modules after instantiating 'app' to avoid known circular import problems with Flask
    from tracker.tracker_11.blueprints import main, api, error

    main.get_vars_from_create_app(config_name, _logging_level, _logging_level_name)
    api.get_vars_from_create_app(config_name, _logging_level, _logging_level_name)

    _app.register_blueprint(main.main_bp)
    _app.register_blueprint(api.api_bp)
    _app.register_blueprint(error.error_bp)

    # Remove after testing
    @_app.route('/doh')
    def doh():
        # Raise an exception to trigger a 500 error
        raise RuntimeError("This is an intentional 500 error.")

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
