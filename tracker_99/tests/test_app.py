"""Test methods and functions in root files (e.g., __init)__.py, app_utils.py, etc.)

Run with -s option to allow tests to use the 'print' command within the tests
to display messages along with pylint output (i.e., `pytest tracker_99/tests -s` or
`coverage run -m pytest tracker_99/tests -s`)
"""
import click
import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from tracker_99 import create_app
from tracker_99.tests import app, client, runner


# Use indirect parametrization to turn logging on or off
@pytest.mark.parametrize('app', [{'log_events': False}], indirect=True)
def test_app(client: FlaskClient, app: Flask) -> None:
    """Ensure you created the application instance.

    :param FlaskClient client: The fixture that sends requests (GET, POST, etc.) to app
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    with app.test_request_context():
        assert app is not None


def test_config_name_is_valid():
    """Test that create_app() passes when config_name exists and is a string."""
    create_app(config_name='testing')


def test_config_name_is_invalid_value():
    """Test that create_app() fails when config_name does not exist."""
    with pytest.raises(ValueError):
        create_app(config_name='doh')


def test_config_name_is_invalid_type():
    """Test that create_app() fails when config_name is not a string."""
    with pytest.raises(TypeError):
        create_app(config_name=1)


def test_log_events_is_valid():
    """Test that create_app() passes when config_name exists and is a string."""
    create_app(log_events=False)


def test_log_events_is_invalid_type():
    """Test that create_app() fails when config_name is not a string."""
    with pytest.raises(TypeError):
        create_app(log_events=1)


"""
The following code demonstrates using and testing Click with Flask.
It is not a necessary part of the application.
"""


@click.command()
@click.option('--name', default='World')
def hello_command(name):
    """A Click command that prints a greeting in the CLI

    :param str name: Who to greet, defaults to 'World'

    :returns: None
    :rtype: None
    """
    click.echo(f'Hello, {name}!')


def test_hello_command(runner: FlaskCliRunner, app: Flask) -> None:
    """Test the contents of the result of a CLI command.

    :param FlaskCliRunner runner: The fixture to invoke the Click command
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    result = runner.invoke(hello_command)
    assert 'World' in result.output

    result = runner.invoke(hello_command, args=['--name', 'Flask'])
    assert 'Flask' in result.output
