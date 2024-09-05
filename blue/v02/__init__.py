"""The `__init__.py` serves double duty: it will contain the application factory,
and it tells Python that the current directory should be treated as a package.
You can then import its files as modules (e.g., `from app.foo import bar`).

Usage:
- python -B -m flask --app "v02" run
- python -B -m flask --app "v02:create_app(config_class='v02.config.DevConfig')" run
"""

import os
import sys
import flask
from v02.config import Config, DevConfig, TestConfig

__author__ = "Rob Garcia"


def create_app(config_class: object | str = Config) -> flask.Flask:
    """Application Factory.

    :param str config_class: An alternate configuration from `config.py` for \
    development, testing, etc. Uses the base `Config` class by default if None

    :return: An application instance
    :rtype: flask.Flask
    """
    # Ensure the Python version supports Flask 3
    _python_version = _get_python_version()
    print(f"Your Python version is {_python_version}.")
    if _python_version < 3.08:
        print("Flask 3 requires Python 3.8 or above. Exiting now...")
        sys.exit(0)

    # Create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    @app.route("/")
    @app.route("/index")
    def index():
        """Render the default landing page.

        :return: The HTML code for the page
        :rtype: str
        """
        greeting = f"""<h1>Hello, World!</h1>
        <h2>I am Version 2.</h2>
        <p>From <code>__init__.py</code>: You are using Python {_python_version}.</p>
        <p>From <code>config.py</code>: Your logging level is {app.config['LOGGING_LEVEL']}.</p>
        <p>From <code>.flaskenv</code>: Your port number is {os.environ.get('FLASK_RUN_PORT')}.</p>
        <p>From <code>.env</code>: <samp>EXAMPLE_ENV_VARIABLE</samp>: "{os.environ.get('EXAMPLE_ENV_VARIABLE')}"</p>
        <p><code>UNDEFINED_KEY</code>: {app.config['UNDEFINED_KEY']}</p>
        """
        return greeting

    return app


def _get_python_version() -> float:
    """Get the Python version used by the server.

    :return: The Python version used by the server
    :rtype: float
    """
    # Get Python version and convert to float (e.g., 3.9 -> 3.09)
    _python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

    return _python_version
