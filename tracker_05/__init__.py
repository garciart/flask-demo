"""A Flask application that incorporates unit testing.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

Usage:
# Run the unit tests found in `tests/test_app.py`
# Use Interactive mode
python -B -m unittest --buffer --verbose tracker_05/tests/test_app.py
# Use Automatic mode
echo 'default' | python -B -m unittest --buffer --verbose tracker_05/tests/test_app.py

Changes:
- Added unit tests.
"""

import flask

# Import the helper functions
from tracker_05.app_utils import check_system, validate_input
# Import the runtime configuration classes
from tracker_05.config import CONFIGS

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
            <p>{_app.config['CONFIG_MSG']}</p>
            <p>You are using Python {_python_version} and Flask {_flask_version}.</p>
            """
        return _greeting

    # Return the application instance to the code that invoked 'create_app()'
    return _app
