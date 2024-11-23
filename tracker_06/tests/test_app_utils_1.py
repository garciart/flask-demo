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
import logging
import os
import shutil
import unittest  # pylint: disable=unused-import

import flask

from tracker_06.app_utils import check_system, validate_input, start_log_file
from tracker_06.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestAppUtils1(BaseTestCase):
    """Unit tests for application utilities.

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
        # NOTE - Do not run this all the time, since it will create a log file
        # that you must manually remove

        # test_app = flask.Flask(__name__)  # NOSONAR
        # try:
        #     start_log_file(app=test_app, log_dir='tracker_logs/test', logging_level=10)
        # except (TypeError, ValueError):
        #     self.fail('Method raised an exception unexpectedly.')
        
        pass

    def test_start_log_file_fail_arg1_type(self):
        """Test that start_log_file() fails when arg1 is the wrong type"""
        test_app = 'foo'
        with self.assertRaises(TypeError):
            start_log_file(app=test_app, log_dir='tracker_logs/test', logging_level=10)

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
            start_log_file(app=test_app, log_dir='tracker_logs/test', logging_level='foo')

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
        logging.shutdown()
        shutil.rmtree(f'{cwd}/foo')
