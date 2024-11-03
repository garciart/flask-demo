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
    # DOCTYPE prevents Quirks mode
    return """<!DOCTYPE html>
        <h1>Hello, World!</h1>
        <p>This is a demo of a basic Flask application that uses a package pattern.</p>
        """
