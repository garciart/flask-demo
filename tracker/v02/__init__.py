"""The `__init__.py` serves double duty: it will contain the application factory,
and it tells Python that the current directory should be treated as a package.
You can then import its files as modules (e.g., `from app.foo import bar`).

Usage: python -B -m flask --app "v02" run
"""

import sys

import flask

__author__ = 'Rob Garcia'


def create_app() -> flask.Flask:
    """Application Factory.

    :returns: An application instance
    :rtype: flask.Flask
    """
    _flask_version = flask.__version__
    # Get the Python version and convert it to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    # Ensure the Python version supports Flask 3
    print(f"Your Python version is {_python_version}.")
    if _python_version < 3.08:
        print('Flask 3 requires Python 3.8 or above. Exiting now...')
        sys.exit(1)

    # Ensure you are using Flask 3
    print(f"Your Flask version is {_flask_version}.")
    if int(_flask_version.split('.')[0]) < 3:
        print('This application requires Flask 3 or above. Exiting now...')
        sys.exit(1)

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
            <p>I am Version 2.</p>
            """

    # Return the application instance to the code that invoked 'create_app()'
    return app
