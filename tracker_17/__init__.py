"""A Flask application that incorporates API authentication.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - source .venv/bin/activate (Linux)
> - .venv/Scripts/activate (Windows)

Usage: python -B -m flask --app tracker_17 run
"""

import logging
import os
from typing import Union

import flask
from flask import Response

# Import the helper functions
from tracker_17.app_utils import validate_input, check_system, start_log_file, log_page_request
# Import the runtime configuration classes
from tracker_17.config import CONFIGS
# Import a SQLAlchemy object
from tracker_17.models import db, migrate, login_manager
# Import profiler middleware
from tracker_17.profiler import add_profiler_middleware

# Flask application factories require lazy loading to prevent circular imports,
# so disable the warning
# pylint: disable=import-outside-toplevel

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default', log_events: Union[bool, None] = None) -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
        development, testing, etc. Uses the base `Config` class if None or 'default'
    :param bool or None log_events: Allows you to override LOGGING_ENABLED configuration setting

    :returns: The Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('config_name', config_name, str)
    validate_input('log_events', log_events, Union[bool, None])

    if config_name not in CONFIGS:
        raise ValueError('Invalid configuration name. Exiting now...')

    # Ensure the system meets the prerequisites for the application
    _python_version, _flask_version = check_system()

    # Create the Flask application instance
    _app = flask.Flask(__name__)

    # Load the configuration class from config.py based on the environment
    _app.config.from_object(CONFIGS[config_name])

    # Optionally add the profiler middleware based on configuration
    if _app.config.get('PROFILING_ENABLED', False):
        _app = add_profiler_middleware(_app)

    # Configure logging
    _app, _logging_enabled, _logging_level = _configure_logging(_app, log_events)

    if _logging_enabled:
        # Start the log at logging.INFO to enter application starting messages
        start_log_file(_app, log_dir='tracker_logs', logging_level=_logging_level)

        @_app.after_request
        def log_response_code(response: Response) -> Response:
            """Intercept the response, log it, and send it back to the app.

            **NOTE** - This will not change the response.

            :param Response response: The response to log

            :returns: The response without changes
            :rtype: Response
            """
            # Capture the request and the response
            log_page_request(_app, flask.request, response)

            # Do not forget to return the response to the client, or the app will crash
            return response

    # Configure database
    _app = _configure_database(_app)

    # Enable authentication
    login_manager.init_app(_app)
    login_manager.login_view = 'auth_bp.login'

    # Start routing using blueprints
    # Import modules after instantiating 'app' to avoid known circular import problems with Flask
    from tracker_17.blueprints import main, error, admin, api, auth

    main.get_vars_from_create_app(
        config_name, _logging_level, logging.getLevelName(_logging_level))

    _app.register_blueprint(main.main_bp)
    _app.register_blueprint(error.error_bp)
    _app.register_blueprint(admin.admin_bp)
    _app.register_blueprint(api.api_bp)
    _app.register_blueprint(auth.auth_bp)

    @_app.route('/doh')
    def doh() -> None:
        """Use to raise an exception to trigger a 500 error for testing.
        Remove before deploying to production.

        :returns None: None
        """
        raise RuntimeError('This is an intentional 500 error.')

    # Return the application instance to the code that invoked 'create_app()'
    return _app


def _configure_logging(app: flask.Flask, log_events: Union[bool, None] = None) -> tuple:
    """Configure the database

    :param flask.Flask app: The original Flask application instance
    :param bool or None log_events: Allows you to override LOGGING_ENABLED configuration setting

    :returns: The revised Flask application instance, the logging-enabled flag, \
        and the logging level
    :rtype: tuple
    """
    # Validate inputs
    validate_input('app', app, flask.Flask)
    validate_input('log_events', log_events, Union[bool, None])

    # Configure logging
    try:
        # This may sound counter-intuitive, but I recommend you do not save log events
        # to a file when running the application in debug mode,
        # like if you run `python -m flask --app "app" run --debug`
        # If you run the app in debug mode, so you can make hot fixes,
        # you may end up with a huge log file.
        if app.debug:
            _logging_enabled = False
        elif log_events is not None:
            # If log_events is explicitly passed, use it
            _logging_enabled = log_events
        else:
            _logging_enabled = bool(app.config.get('LOGGING_ENABLED', True))

        # Get the logging level from the config, and default to WARNING if not specified
        _logging_level = int(app.config.get('LOGGING_LEVEL', logging.WARNING))

    # Exempt from coverage because the exception cannot be unit tested easily
    except (ValueError, TypeError) as e:  # pragma: no cover
        # If there is a configuration error, use default settings
        print(f'Configuration error: {e}\nUsing default settings...')
        _logging_enabled = True
        _logging_level = logging.WARNING

    return app, _logging_enabled, _logging_level


def _configure_database(app: flask.Flask) -> flask.Flask:
    """Configure the database

    :param flask.Flask app: The original Flask application instance
    :returns: The revised Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('app', app, flask.Flask)

    # Bind the database instance to the app
    db.init_app(app)

    # Link the Migrate object to the app and the database to allow migrations,
    # like schema updates, etc.
    migrate.init_app(app, db)

    # Lazy import to avoid circular imports
    # and to ensure models are loaded before performing any migrations
    # pylint: disable-next=unused-import
    from tracker_17.models.member import Member

    # Create the database if it does not exist
    with app.app_context():
        # Extract database file path from the URI
        uri = db.engine.url
        db_path = uri.database if uri.database else uri.host

        if not os.path.exists(db_path):
            from tracker_17.models.create_db import create_db

            create_db()

    return app
