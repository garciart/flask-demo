"""A basic Flask application that uses a single-file module pattern.

**NOTE** - Remember to activate your Python virtual environment before running:

- `source venv/bin/activate` (Linux)
- `venv/Scripts/activate` (Windows)

**Usage**:

- `python -B -m flask --app hello run`
"""

import flask

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
        <p>This is a demo of a basic Flask application that uses a single-file module pattern.</p>
        """
