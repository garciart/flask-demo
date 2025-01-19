"""Test methods and functions in root files (e.g., __init)__.py, app_utils.py, etc.)

Run with -s option to allow tests to use the 'print' command within the tests
to display messages along with pylint output (i.e., `pytest tracker_99/tests -s` or
`coverage run -m pytest tracker_99/tests -s`)
"""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from tracker_99.tests import app, client


# Test using indirect parametrization
@pytest.mark.parametrize('app', ['no_log'], indirect=True)
def test_index_page_code_pass(client: FlaskClient, app: Flask) -> None:
    """Ensure you created the application instance.

    :param FlaskClient client: The fixture that sends requests \
        (GET, POST, etc.) to the application
    :param Flask app: The Flask application instance used for test

    :returns: None
    :rtype: None
    """
    with app.test_request_context():
        assert app is not None
