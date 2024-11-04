"""A basic Flask application that uses a package pattern.

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Usage: python -B -m flask --app tracker_01 run
"""

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
flask_version = flask.__version__
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
    # DOCTYPE prevents Quirks mode
    return """<!DOCTYPE html>
        <h1>Hello, World!</h1>
        <p>This is a demo of a basic Flask application that uses a package pattern.</p>
        """
