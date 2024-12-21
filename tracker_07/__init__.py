"""A Flask application that incorporates performance profiling.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - source .venv/bin/activate (Linux)
> - .venv/Scripts/activate (Windows)

Usage:
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_07:create_app('profile')" run --without-threads
"""

import flask

# Import the helper functions
from tracker_07.app_utils import check_system, validate_input
# Import the runtime configuration classes
from tracker_07.config import CONFIGS
# Import profiler middleware
from tracker_07.profiler import add_profiler_middleware

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default') -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
        development, testing, etc. Uses the base `Config` class if None or 'default'

    :returns: The Flask application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('config_name', config_name, str)

    if config_name not in CONFIGS:
        raise ValueError(
            'Invalid configuration name. Exiting now...')

    # Ensure the system meets the prerequisites for the application
    _python_version, _flask_version = check_system()

    # Create the Flask application instance
    _app = flask.Flask(__name__)

    # Load the configuration class from config.py based on the environment
    _app.config.from_object(CONFIGS[config_name])

    # Optionally add the profiler middleware based on configuration
    if _app.config.get('PROFILING_ENABLED', False):
        _app = add_profiler_middleware(_app)

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
            <h1>Welcome to Tracker!</h1>
            <p>{_app.config['CONFIG_MSG']}</p>
            <p>You are using Python {_python_version} and Flask {_flask_version}.</p>
            """
        return _greeting

    # Return the application instance to the code that invoked 'create_app()'
    return _app
