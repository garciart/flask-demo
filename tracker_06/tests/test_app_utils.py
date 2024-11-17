"""Unit tests for the Flask demo.

**NOTES:**

- Remember to activate your Python virtual environment before running:

    - `source venv/bin/activate` (Linux)
    - `venv/Scripts/activate` (Windows)

- Run from the project directory (e.g., flask-demo, not tracker_XX)
- Ensure you have an empty __init__.py in the 'tests' directory
- Do not log events when unit testing or each test will create a log file.
- Using --buffer and --verbose together provides a good balance of output,
  since --buffer hides console output from the application
  and --verbose displays the test's docstring
  (ex., "Ensure you created the application instance ... ok")

**Usage:**

```
python -B -m unittest --buffer --verbose tracker_XX/tests/test_app.py
```
"""
import os
import shutil
import unittest

import flask

from tracker_06.app_utils import check_system, validate_input, start_log_file, log_page_request
from tracker_06.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestAppUtils(BaseTestCase):
    """"Unit tests for application utilities.

    :param unittest.TestCase BaseTestCase: Inherited from __init__.py
    """

    def test_check_system_pass_meets_req(self):
        """Test that check_system() passes when requirements met"""
        try:
            check_system(
                min_python_version=self.sys_python_version, min_flask_version=self.sys_flask_version
            )
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_check_system_pass_exceeds_req(self):
        """Test that check_system() passes when requirements exceeded"""
        try:
            check_system(
                min_python_version=self.sys_python_version - 0.1,
                min_flask_version=self.sys_flask_version - 0.1,
            )
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_check_system_fail_arg1_wrong_type(self):
        """Test that check_system() fails because min_python_version is not type float"""
        with self.assertRaises(TypeError):
            check_system(min_python_version='foo', min_flask_version=self.sys_flask_version)

    def test_check_system_fail_arg2_wrong_type(self):
        """Test that check_system() fails because min_flask_version is not type float"""
        with self.assertRaises(TypeError):
            check_system(min_python_version=self.sys_python_version, min_flask_version='foo')

    def test_check_system_fail_arg1_zero_or_below(self):
        """Test that check_system() fails because min_python_version is zero or below"""
        with self.assertRaises(ValueError):
            check_system(min_python_version=-0.1, min_flask_version=self.sys_flask_version)

    def test_check_system_fail_arg2_zero_or_below(self):
        """Test that check_system() fails because min_flask_version is zero or below"""
        with self.assertRaises(ValueError):
            check_system(min_python_version=self.sys_python_version, min_flask_version=-0.1)

    def test_check_system_fail_python_version_below_req(self):
        """Test that check_system() fails because the installed Python version is too old"""
        with self.assertRaises(ValueError):
            check_system(
                min_python_version=self.sys_python_version + 0.1,
                min_flask_version=self.sys_flask_version,
            )

    def test_check_system_fail_flask_version_below_req(self):
        """Test that check_system() fails because the installed Flask version is too old"""
        with self.assertRaises(ValueError):
            check_system(
                min_python_version=self.sys_python_version,
                min_flask_version=self.sys_flask_version + 0.1,
            )

    def test_validate_input_pass_single_type(self):
        """Test that validate_input() passes when requirements met"""
        test_var = 3.14
        try:
            validate_input(obj_name='test_var', obj_to_check=test_var, expected_type=float)
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_validate_input_pass_multi_type(self):
        """Test that validate_inputs() passes when a type in a tuple matches the input type"""
        test_var = 3.14
        try:
            validate_input(obj_name='test_var', obj_to_check=test_var, expected_type=float | str)
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_validate_input_fail_type(self):
        """Test that validate_input() fails if the input type is incorrect"""
        test_var = 3.14
        with self.assertRaises(TypeError):
            validate_input(obj_name='test_var', obj_to_check=test_var, expected_type=str)

    def test_validate_input_fail_empty(self):
        """Test that validate_input() fails if the input is empty"""
        test_var = ''
        with self.assertRaises(ValueError):
            validate_input(obj_name='test_var', obj_to_check=test_var, expected_type=str)

    def test_start_log_file_pass(self):
        """Test that start_log_file() passes when requirements met"""
        test_app = flask.Flask(__name__)
        try:
            start_log_file(app=test_app, log_dir='tracker_logs', logging_level=10)
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_start_log_file_fail_arg1_type(self):
        """Test that start_log_file() fails when arg1 is the wrong type"""
        test_app = 'foo'
        with self.assertRaises(TypeError):
            start_log_file(app=test_app, log_dir='tracker_logs', logging_level=10)

    def test_start_log_file_fail_arg2_type(self):
        """Test that start_log_file() fails when arg2 is the wrong type"""
        test_app = flask.Flask(__name__)
        with self.assertRaises(TypeError):
            start_log_file(app=test_app, log_dir=1, logging_level=10)

    def test_start_log_file_fail_arg2_empty(self):
        """Test that start_log_file() fails when arg2 is empty"""
        test_app = flask.Flask(__name__)
        with self.assertRaises(ValueError):
            start_log_file(app=test_app, log_dir='', logging_level=10)

    def test_start_log_file_fail_arg3_type(self):
        """Test that start_log_file() fails when arg3 is the wrong type"""
        test_app = flask.Flask(__name__)
        with self.assertRaises(TypeError):
            start_log_file(app=test_app, log_dir='tracker_logs', logging_level='foo')

    def test_start_log_file_mkdir_log_dir_pass(self):
        """Test that start_log_file() can make a log directory"""
        test_app = flask.Flask(__name__)
        cwd = os.getcwd()
        # Delete the directory and its contents if it exists
        try:
            shutil.rmtree(f'{cwd}/foo')
        except FileNotFoundError:
            pass
        try:
            start_log_file(app=test_app, log_dir='foo', logging_level=10)
        except OSError:
            self.fail('Method raised an exception unexpectedly.')
        shutil.rmtree(f'{cwd}/foo')

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


if __name__ == '__main__':
    unittest.main()
