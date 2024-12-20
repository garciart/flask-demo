"""A Flask application that incorporates templates.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Usage:
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest --verbose --buffer tracker_10/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_10:create_app('profile')" run --without-threads
# Runs the Flask application using HTML files found in the `templates` directory
# python -B -m flask --app "tracker_10:create_app(config_name='development', log_events=True)" run
python -B -m flask --app "tracker_10:create_app('development', True)" run

> **NOTE** - Enclose options in quotation marks when using special characters.

Changes:
- Moved pages into templates
- Added a "master" layout page
- Added Cascading Style Sheets (CSS), images, and JavaScript files
"""

import logging
from typing import Union

import flask
from flask import Response

# Import the helper functions
from tracker_10.app_utils import validate_input, check_system, start_log_file, log_page_request
# Import the runtime configuration classes
from tracker_10.config import CONFIGS
# Import profiler middleware
from tracker_10.profiler import add_profiler_middleware

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

        :returns: The HTML code to display with {{ placeholders }} populated
        :rtype: str
        """
        return flask.render_template(
            'main/index.html',
            config_msg_text=_app.config['CONFIG_MSG'],
            python_version_text=_python_version,
            flask_version_text=_flask_version,
            logging_level_text=_logging_level,
            logging_level_name_text=logging.getLevelName(_logging_level),
        )

    @_app.errorhandler(404)
    def page_not_found(e) -> tuple:
        """Render an error page if the requested page or resource was not found on the server.

        :returns: The HTML code to render and the response code
        :rtype: tuple
        """
        return flask.render_template('error/404.html', e=e), 404

    @_app.errorhandler(500)
    def server_error(e) -> tuple:
        """Render an error page if there is a server error.

        :returns: The HTML code to render and the response code
        :rtype: tuple
        """
        return flask.render_template('error/500.html', e=e), 500

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
