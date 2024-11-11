"""A Flask application that uses environment variables.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage: python -B -m flask --app tracker_02 run

Changes:
- Added ability to read environment variables
"""

import importlib
import os
import sys
import flask

__author__ = 'Rob Garcia'

# Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

# Ensure you are using the correct version of Python
print(f"Your Python version is {python_version}.")
if python_version < 3.08:
    raise ValueError('Flask 3 requires Python 3.8 or above. Exiting now...')

# Ensure you are using the correct version of Flask
flask_version = importlib.metadata.version("flask")
print(f"Your Flask version is {flask_version}.")
if int(flask_version.split('.')[0]) < 3:
    raise ValueError('This application requires Flask 3 or above. Exiting now...')

# Create the Flask application instance
app = flask.Flask(__name__)


# Create a route and page
@app.route('/')
@app.route('/index')
def index() -> str:
    """Render the default landing page.

    :returns: The HTML code for the page
    :rtype: str
    """
    # This system environment variable is common to Linux and Windows systems
    default_encoding = os.environ.get('LANG')

    # This system environment variable is defined in the .env file
    env_user_defined_var = os.environ.get('ENV_USER_DEFINED_VAR')

    # This Flask environment variable is defined in the .flaskenv file
    flaskenv_user_defined_var = os.environ.get('FLASKENV_USER_DEFINED_VAR')

    # This Flask environment variable is not defined anywhere but has a default value
    foo = os.environ.get('FOO', 'bar')

    # DOCTYPE prevents Quirks mode
    return f"""<!DOCTYPE html>
        <h1>Hello, World!</h1>
        <p>This is a demo of A Flask application that uses environment variables.</p>
        <p>Your encoding is <code>{default_encoding}</code>.</p>
        <p>This is <code>ENV_USER_DEFINED_VAR</code>, a user-defined variable from the
        <code>.env</code> file: <code>{env_user_defined_var}</code></p>
        <p>This is <code>FLASKENV_USER_DEFINED_VAR</code>, a user-defined variable from the
        <code>.flaskenv</code> file: <code>{flaskenv_user_defined_var}</code></p>
        <p>The value of <code>foo</code> is "{foo}".</p>
        """
