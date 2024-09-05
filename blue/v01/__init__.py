"""The `__init__.py` serves double duty: it will contain the application factory,
and it tells Python that the current directory should be treated as a package.
You can then import its files as modules (e.g., `from app.foo import bar`).

Usage: python -B -m flask --app "v01" run
"""

import sys
import flask

__author__ = "Rob Garcia"


def create_app() -> flask.Flask:
    """Application Factory.

    :return: An application instance
    :rtype: flask.Flask
    """
    # Ensure the Python version supports Flask 3
    _python_version = _get_python_version()
    print(f"Your Python version is {_python_version}.")
    if _python_version < 3.08:
        print('Flask 3 requires Python 3.8 or above. Exiting now...')
        sys.exit(0)

    # Create and configure the app
    app = flask.Flask(__name__)

    @app.route("/")
    @app.route("/index")
    def index():
        """Render the default landing page.

        :return: The HTML code for the page
        :rtype: str
        """
        return "<h1>Hello, World!</h1><p>I am Version 1.</p>"

    return app


def _get_python_version() -> float:
    """Get the Python version used by the server.

    :return: The Python version used by the server
    :rtype: float
    """
    # Get Python version and convert to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    return _python_version
