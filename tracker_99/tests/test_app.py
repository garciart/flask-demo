"""Test methods and functions in root files (e.g., __init)__.py, app_utils.py, etc.)

Use with -s option to allow tests to print to STDOUT
(i.e., `pytest tracker_99/tests/test_app.py -s`)
"""

import click
import pytest
from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient

from tracker_99.tests import app, client, runner


# Tests using indirect parametrization
@pytest.mark.parametrize('app', ['no_log'], indirect=True)
def test_about_page_pass(client: FlaskClient, app: Flask) -> None:
    """Test the HTTP response code to a request for the About page.

    :param FlaskClient client: The fixture that sends requests \
        (GET, POST, etc.) to the application
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    response = client.get('/about')
    assert response.status_code == 200


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


@pytest.mark.parametrize('app', ['no_log'], indirect=True)
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
