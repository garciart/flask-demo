"""Contains pytest fixtures and code used or shared by multiple test modules.

Run with -s option to allow tests to use the 'print' command within the tests
to display messages along with pylint output (i.e., `pytest tracker_99/tests -s` or
`coverage run -m pytest tracker_99/tests -s`)
"""

import pytest
from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient
from pytest import FixtureRequest

from tracker_99 import create_app


@pytest.fixture()
def app(request: FixtureRequest):
    """Fixture to create the Flask application instance.

    :param FixtureRequest request: A request from a test or fixture function

    :yields: The Flask application instance to test
    :yield type: Flask
    """
    # Set the default run configuration to...'default'! :)
    _config_name = 'default'

    # By default, logging requests and responses is enabled in the Tracker app.
    # Since each test creates a Tracker instance, each test will generate a small log file.
    # which is usually not necessary for the test.
    # To avoid this, set the default log_events value to False for testing
    _log_events = False

    # If the test needs to use a different configuration file or needs to log events,
    # you can pass the values to `create_app(...)` directly in the test,
    # or you can use indirect parametrization to pass arguments from the test to this fixture
    # before creating the instance:
    #
    # @pytest.mark.parametrize(
    #     'app', [{'config_name': 'foo', 'log_events': True}], indirect=True)
    # def test_app(client: FlaskClient, app: Flask) -> None:
    #     """Ensure you created the application instance.
    #
    # The following code will retrieve the parameters:
    if hasattr(request, 'param'):
        _config_name = request.param.get('config_name', 'default')
        _log_events = request.param.get('log_events', False)

    _app = create_app(config_name=_config_name, log_events=_log_events)

    _app.config.update({"TESTING": True, "LOGIN_DISABLED": True})

    ###
    # Add additional setup code here
    ###

    yield _app

    ###
    # Add clean-up and resource reset here
    ###


# W0621: Redefining name 'app' from outer scope is a false positive
# In pytest, functions require 'app' as an argument
# pylint: disable=redefined-outer-name


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
