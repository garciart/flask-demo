"""A basic Flask application that uses environment variables.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage: python -B -m flask --app tracker_02 run
"""

import sys
import flask
import os

__author__ = 'Rob Garcia'

# Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
_python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

# Ensure the Python version supports Flask 3
print(f"Your Python version is {_python_version}.")
if _python_version < 3.08:
    print('Flask 3 requires Python 3.8 or above. Exiting now...')
    sys.exit(1)

# Create the Flask application instance and get the version number
app = flask.Flask(__name__)
_flask_version = flask.__version__

# Ensure you are using Flask 3
print(f"Your Flask version is {_flask_version}.")
if int(_flask_version.split('.')[0]) < 3:
    print('This application requires Flask 3 or above. Exiting now...')
    sys.exit(1)


# Create a route and page
@app.route('/')
@app.route('/index')
def index() -> str:
    """Render the default landing page.

    :return: The HTML code for the page
    :rtype: str
    """
    # This system environment variable is common to Linux and Windows systems
    default_encoding = os.environ.get('LANG')

    # This system environment variable is defined in the .env file
    env_user_defined_var = os.environ.get('ENV_USER_DEFINED_VAR')

    # This Flask environment variable is defined in the .flaskenv file
    flaskenv_user_defined_var = os.environ.get('FLASKENV_USER_DEFINED_VAR')

    # DOCTYPE prevents Quirks mode
    return f"""<!DOCTYPE html>
        <h1>Hello, World!</h1>
        <p>This is a demo of a basic Flask application that uses environment variables.</p>
        <p>Your encoding is {default_encoding}.</p>
        <p>This is <code>ENV_USER_DEFINED_VAR</code>, a user-defined variable from the
        <code>.env</code> file: <code>{env_user_defined_var}</code></p>
        <p>This is <code>ENV_USER_DEFINED_VAR</code>, a user-defined variable from the
        <code>.flaskenv</code> file: <code>{flaskenv_user_defined_var}</code></p>
        """
