"""Unit tests for the Flask demo.

**NOTES:**

- Remember to activate your Python virtual environment first:

    - `source .venv/bin/activate` (Linux)
    - `.venv/Scripts/activate` (Windows)

- Test from the project directory (e.g., `flask-demo`, not `tracker_XX`)
- Do not log events when unit testing or each test will create a log file.
- Using `--buffer` and `--verbose` together provides a good balance of output,
  since `--buffer` hides console output from the application
  and `--verbose` displays the test's docstring
  (ex., `Test that check_system() fails because min_python_version is not type float ... ok`)

**Usage:**

```
python -B -m unittest discover tracker_XX/tests -b -v
```
"""
import unittest  # pylint: disable=unused-import

import flask

from tracker_08.app_utils import log_page_request
from tracker_08.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestAppUtils2(BaseTestCase):
    """Unit tests for application utilities.

    :param unittest.TestCase BaseTestCase: Inherited from __init__.py
    """

    def test_log_page_request_pass(self):
        """Test that log_page_request() passes when requirements met"""
        test_app = flask.Flask(__name__)
        # Required environ keys. If you receive a KeyError, append the key-value pair to the dict
        environ = {
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET',
            'wsgi.url_scheme': 'http',
        }
        test_response = flask.Response('foo', status=201, mimetype='text/plain')
        # Create a mock request
        with self.app.request_context(environ):
            test_request = flask.Request(environ)
            try:
                log_page_request(app=test_app, request=test_request, response=test_response)
            except (TypeError, ValueError):
                self.fail('Method raised an exception unexpectedly.')

    def test_log_page_request_fail_arg1_type(self):
        """Test that log_page_request() fails when arg1 is the wrong type"""
        test_app = 'foo'
        # Required environ keys. If you receive a KeyError, append the key-value pair to the dict
        environ = {
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET',
            'wsgi.url_scheme': 'http',
        }
        test_response = flask.Response('foo', status=201, mimetype='text/plain')
        # Create a mock request
        with self.app.request_context(environ):
            test_request = flask.Request(environ)
            with self.assertRaises(TypeError):
                log_page_request(app=test_app, request=test_request, response=test_response)

    def test_log_page_request_fail_arg2_type(self):
        """Test that log_page_request() fails when arg2 is the wrong type"""
        test_app = flask.Flask(__name__)
        test_response = flask.Response('foo', status=201, mimetype='text/plain')
        test_request = 'foo'
        with self.assertRaises(TypeError):
            log_page_request(app=test_app, request=test_request, response=test_response)

    def test_log_page_request_fail_arg3_type(self):
        """Test that log_page_request() fails when arg3 is the wrong type"""
        test_app = flask.Flask(__name__)
        # Required environ keys. If you receive a KeyError, append the key-value pair to the dict
        environ = {
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET',
            'wsgi.url_scheme': 'http',
        }
        test_response = 'foo'
        # Create a mock request
        with self.app.request_context(environ):
            test_request = flask.Request(environ)
            with self.assertRaises(TypeError):
                log_page_request(app=test_app, request=test_request, response=test_response)
