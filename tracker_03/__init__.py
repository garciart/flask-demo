"""A Flask application that uses an application factory and a configuration file.

**NOTE** - Remember to activate your Python virtual environment first:

- source .venv/bin/activate (Linux)
- .venv/Scripts/activate (Windows)

**Usage**:

```
# Run the Flask application using the configuration variables found in `config.py`
python -B -m flask --app "tracker_03:create_app(config_name='development')" run
python -B -m flask --app "tracker_03:create_app('development')" run
# Run the application using the 'default' configuration
python -B -m flask --app tracker_03 run
# Use the 'foo' command-line argument
python -B -m flask --app "tracker_03:create_app(foo_var='42')" run
```

**NOTE** - Enclose options in quotation marks when using special characters.
"""

import importlib
import sys

import flask

# Import the runtime configuration classes
from tracker_03.config import CONFIGS

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
    _python_version, _flask_version = check_system(min_python_version=3.08, min_flask_version=3.0)

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
            <h1>Welcome to Tracker!</h1>
            <p>{_app.config['CONFIG_MSG']}</p>
            <p>You are using Python {_python_version} and Flask {_flask_version}.</p>
            <p>The value of <code>foo</code> is "{foo_var}".</p>
            """
        return _greeting

    # Return the application instance to the code that invoked 'create_app()'
    return _app


def check_system(min_python_version: float = 3.08, min_flask_version: float = 3.0) -> tuple:
    """Check if the installed Python and Flask versions can run the application.

    **NOTE** - Use `3.01` for version `3.1` and `3.10` for version `3.10`.

    :param float min_python_version: The minimum Python version in float format, defaults to 3.08
    :param float min_flask_version: The minimum Flask version in float format, defaults to 3.0

    :returns: The Python and Flask versions in float format (`3.01` for version `3.1`, etc.)
    :rtype: tuple
    """
    # Validate inputs
    if not isinstance(min_python_version, float) or not isinstance(min_flask_version, float):
        raise TypeError(
            'The minimum Python and Flask version numbers must be type float. Exiting now...'
        )

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

    return _python_version, _flask_version
