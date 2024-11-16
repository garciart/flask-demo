"""Add profiling support to the Flask application using Werkzeug's ProfilerMiddleware.
"""

import flask
from werkzeug.middleware.profiler import ProfilerMiddleware

from tracker_07.app_utils import (validate_input)

__all__ = ['add_profiler_middleware']


def add_profiler_middleware(app: flask.Flask) -> flask.Flask:
    """Wraps the application instance in middleware that profiles each request using the cProfile module.

    :param flask.Flask app: The application instance

    :returns: The wrapped application instance
    :rtype: flask.Flask
    """
    # Validate inputs
    validate_input('app', app, flask.Flask)

    # Add ProfilerMiddleware to your Flask app.
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    return app
