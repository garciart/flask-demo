"""A Flask application that uses a utility file.

**NOTE** - Remember to activate your Python virtual environment before running:

- `source venv/bin/activate` (Linux)
- `venv/Scripts/activate` (Windows)

**Usage**:

```
# Run the Flask application using the configuration variables found in `config.py`
python -B -m flask --app "tracker_03a:create_app(config_name='development')" run
python -B -m flask --app "tracker_03a:create_app('development')" run
# Run the application using the 'default' configuration
python -B -m flask --app tracker_03a run
# Use the 'foo' command-line argument
python -B -m flask --app "tracker_03a:create_app(foo_var='42')" run
```

**NOTE** - Enclose options in quotation marks when using special characters.
"""

import logging

import flask

# Import the helper functions
from tracker_03a.app_utils import (check_system, validate_input)
# Import the runtime configuration classes
from tracker_03a.config import Config, DevConfig

__author__ = 'Rob Garcia'


def create_app(config_name: str = 'default', foo_var: str = 'bar') -> flask.Flask:
    """Application Factory.

    :param str config_name: An alternate configuration from `config.py` for \
    development, testing, etc. Uses the base `Config` class if None or 'default'
    :param str foo_var: Demonstrates using command-line inputs. Remove after testing.

    :returns: The Flask application instance
    :rtype: flask.Flask
    """
    # Ensure the system meets the prerequisites for the application
    check_system(min_python_version=3.08, min_flask_version=3.0)

    # Create the Flask application instance
    _app = flask.Flask(__name__)

    # Create the Flask application instance with the selected configuration
    _app = _configure_app(config_name)

    try:
        _logging_level = int(_app.config.get('LOGGING_LEVEL', logging.WARNING))
    except ValueError:
        _logging_level = logging.WARNING

    _logging_level_name = logging.getLevelName(_logging_level)

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
            <p>The value of <code>foo</code> is "{foo_var}".</p>
            """
        return _greeting

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
        'default': Config,
    }

    _app.config.from_object(config_mapping.get(config_name, Config))

    return _app
