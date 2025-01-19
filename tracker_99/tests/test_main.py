"""Test methods and functions in blueprints/main

Run with -s option to allow tests to use the 'print' command within the tests
to display messages along with pylint output (i.e., `pytest tracker_99/tests -s` or
`coverage run -m pytest tracker_99/tests -s`)
"""
from flask import Flask
from flask.testing import FlaskClient
from flask_login import current_user

from tracker_99.tests import app, client


def test_index_page_code_pass(client: FlaskClient, app: Flask) -> None:
    """Test the HTTP response code to a request for the Index page.

    :param FlaskClient client: The fixture that sends requests (GET, POST, etc.) to app
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    # Act as an authenticated administrator for testing
    with app.test_request_context():
        current_user.is_admin = True

        response = client.get('/index')
        assert response.status_code == 200


def test_index_page_content_pass(client: FlaskClient, app: Flask) -> None:
    """Test the HTTP response code to a request for the Index page.

    :param FlaskClient client: The fixture that sends requests (GET, POST, etc.) to app
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    # Act as an authenticated administrator for testing
    with app.test_request_context():
        current_user.is_admin = True

        response = client.get('/index')
        assert b"Welcome" in response.data


def test_about_page_code_pass(client: FlaskClient, app: Flask) -> None:
    """Test the HTTP response code to a request for the About page.

    :param FlaskClient client: The fixture that sends requests (GET, POST, etc.) to app
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    response = client.get('/about')
    assert response.status_code == 200


def test_about_page_content_pass(client: FlaskClient, app: Flask) -> None:
    """Test the HTTP response code to a request for the About page.

    :param FlaskClient client: The fixture that sends requests (GET, POST, etc.) to app
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    response = client.get('/about')
    assert b"About" in response.data
