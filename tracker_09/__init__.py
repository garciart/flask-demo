"""A Flask application that incorporates error handling.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Usage:
# Redirect the user to a custom error page and logs the error
# python -B -m flask --app "tracker_09:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_09:create_app('development', True)" run

> **NOTE**
>
> - Enclose options in quotation marks when using special characters.
> - Use the `development` configuration so the application will log `logging.INFO`-level messages.

Changes:
- Added custom 404 and 500 error pages
"""

import logging

import flask
from flask import Response

# Import the helper functions
from tracker_09.app_utils import validate_input, check_system, start_log_file, log_page_request

# Import the runtime configuration classes
from tracker_09.config import CONFIGS

# Import profiler middleware
from tracker_09.profiler import add_profiler_middleware

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default', log_events: bool | None = None) -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
        development, testing, etc. Uses the base `Config` class if None or 'default'
    :param bool log_events: Allows you to override LOGGING_ENABLED configuration setting

    :returns: The Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('config_name', config_name, str)
    validate_input('config_name', log_events, bool | None)

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
    try:
        # This may sound counter-intuitive, but I recommend you do not save log events
        # to a file when running the application in debug mode,
        # like if you run `python -m flask --app "app" run --debug`
        # If you run the app in debug mode, so you can make hot fixes,
        # you may end up with a huge log file.
        if _app.debug:
            _logging_enabled = False
        elif log_events is not None:
            # If log_events is explicitly passed, use it
            _logging_enabled = log_events
        else:
            _logging_enabled = bool(_app.config.get('LOGGING_ENABLED', True))

        _logging_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]

        # Ensure that _logging_level is one of the valid logging levels
        if _app.config.get('LOGGING_LEVEL', logging.WARNING) not in _logging_levels:
            raise ValueError('Invalid logging level.')

        # Get the logging level from the config, and default to WARNING if not specified
        _logging_level = int(_app.config.get('LOGGING_LEVEL', logging.WARNING))

    # Exempt from coverage because the exception cannot be unit tested easily
    except (ValueError, TypeError) as e:  # pragma: no cover
        # If there is any configuration error, log it and fall back to default settings
        _logging_enabled = True
        _logging_level = logging.WARNING
        _app.logger.error('Error configuring logging: %s', e)

    if _logging_enabled:
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
            <b>{logging.getLevelName(_logging_level)} ({_logging_level})</b>.</p>
            """
        return _greeting

    @_app.errorhandler(404)
    def page_not_found(e) -> tuple:
        """Render an error page if the requested page or resource was not found on the server.

        :returns: The HTML code to render and the response code
        :rtype: tuple
        """
        # DOCTYPE prevents Quirks mode
        _error_msg = f"""<!DOCTYPE html>
            <h1>Going somewhere, Solo?</h1>
            <p><i>({e.code}: {e.name})</i></p>
            <p>These aren't the pages you're looking for.</p>
            <p>You can go about your business.</p>
            <p>Move along to the <a href='/index' rel='nofollow' target='_self'
            title='Home'>home page</a>.</p>
            """
        return _error_msg, 404

    @_app.errorhandler(500)
    def server_error(e) -> tuple:
        """Render an error page if there is a server error.

        :returns: The HTML code to render and the response code
        :rtype: tuple
        """
        # DOCTYPE prevents Quirks mode
        _error_msg = f"""<!DOCTYPE html>
            <h1>What a piece of junk!</h1>
            <p><i>({e.code}: {e.name})</i></p>
            <p>Looks like those special modifications I made aren't working.</p>
            <p>But we're a little rushed, so if you'll just
            <a href='/index' rel='nofollow' target='_self' title='Home'>click this link</a>, we'll
            get outta here.</p>
            """
        return _error_msg, 500

    @_app.route('/doh')
    def doh() -> None:
        """Use to raise an exception to trigger a 500 error for testing.
        Remove before deploying to production.

        :returns None: None
        """
        raise RuntimeError('This is an intentional 500 error.')

    # Return the application instance to the code that invoked 'create_app()'
    return _app
