"""Contains pytest fixtures and code used or shared by multiple test modules.
"""

import pytest
from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient
from pytest import FixtureRequest

from tracker_99 import create_app


@pytest.fixture()
def app(request: FixtureRequest) -> Flask:
    """Fixture to create the Flask application instance.

    :param FixtureRequest request: A request from a test or fixture function

    :yields: The Flask application instance to test
    :yield type: Flask
    """
    # Logging is enabled by default in the Tracker app.
    # However, since each test creates a Tracker instance,
    # each test will generate a small log file, which is usually not needed.
    # To only create log files when testing logging functions and methods,
    # use indirect parameterization to pass a 'log/no_log' argument from the test.
    # 'log' means enable logging, and 'no_log' means disable logging.
    # Passing no argument also disables logging.
    log_events = (request.param == 'log')

    if log_events:
        app = create_app()
    else:
        app = create_app(log_events=False)

    app.config.update(
        {
            "TESTING": True,
        }
    )

    """
    Additional setup code goes here
    """

    yield app

    """
    Clean-up and resource reset goes here
    """


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """Send a request (GET, POST, etc.) to the application without running a live server.

    :param Flask app: The Flask application instance to test

    :returns: The response to the request as an object
    :rtype: FlaskClient
    """
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    """Run a CLI command using Click

    :param Flask app: The Flask application instance to test

    :returns: The result of a Click command as an object
    :rtype: FlaskCliRunner
    """
    return app.test_cli_runner()
