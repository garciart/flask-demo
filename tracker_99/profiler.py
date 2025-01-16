"""Add profiling support to the Flask application using the Werkzeug ProfilerMiddleware.
"""

from flask import Flask
from werkzeug.middleware.profiler import ProfilerMiddleware

from tracker_99.app_utils import validate_input

__all__ = ['add_profiler_middleware']


def add_profiler_middleware(app: Flask) -> Flask:
    """Wraps the application instance in middleware that profiles each request
    using the cProfile module.

    :param Flask app: The application instance

    :returns: The wrapped application instance
    :rtype: Flask
    """
    # Validate inputs
    validate_input('app', app, Flask)

    # Add ProfilerMiddleware to your Flask app.
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    return app
