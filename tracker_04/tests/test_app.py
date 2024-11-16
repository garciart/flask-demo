"""Unit tests for the Flask demo.

Run from the project directory (e.g., tracker, not tracker_XX)

Ensure you have an empty __init__.py in the 'tests' directory

> **NOTE** - Do not log events when unit testing or each test will create a log file.

Usage:
- (Interactive) python -B -m unittest --buffer --verbose tracker_XX/tests/test_app.py
- (Auto) echo 'default' | python -B -m unittest --buffer --verbose tracker_XX/tests/test_app.py

> **NOTE** - The reason I added user interaction to `test_app.py` is because you cannot pass
> arguments, like `--config development`, to `test_app.py` using `sys.argv` or the
>`argparse` module; the `unittest` module will read them instead.

> **NOTE** - Using --buffer and --verbose together provides a good balance of output,
> since --buffer hides console output from the application
> and --verbose displays the test's docstring
> (ex., "Ensure you created the application instance ... ok")
"""

import importlib
import sys
import unittest

from tracker_04 import create_app, check_system

__author__ = 'Rob Garcia'


class TestApp(unittest.TestCase):
    """Unit tests for the Flask demo.

    :param class unittest.TestCase: Class to test single test cases
    """
    config_name = (
            input('Enter a configuration to use (press [Enter] to use \'default\'): ') or 'default'
    )
    if config_name not in ['default', 'development', 'profiler']:
        config_name = 'default'
    print(f'\nUsing the {config_name} configuration...')

    def setUp(self):
        """Create the application instance"""
        # Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
        self.sys_python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

        # Get the Flask major and minor version numbers and convert them to a float
        raw_flask_version = importlib.metadata.version("flask")
        flask_version_major, flask_version_minor = map(int, raw_flask_version.split('.')[:2])
        self.sys_flask_version = float(f"{flask_version_major}.{flask_version_minor:02d}")

        self.app = create_app(self.config_name)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_app(self):
        """Ensure you created the application instance"""
        self.assertIsNotNone(self.app)

    def test_index_response_code(self):
        """Test that the index page was created by looking at the response code"""
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        """Test that the index page contains the correct contents"""
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Hello, World!', response.data)

    def tearDown(self):
        """Clear out the application instance variables"""
        self.app_context.pop()
        self.app = None
        self.app_context = None
        self.client = None

    def test_config_name_is_string(self):
        """Test that create_app() passes when config_name is a string."""
        try:
            create_app('default')
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_config_name_is_not_string(self):
        """Test that create_app() fails when config_name is not a string."""
        with self.assertRaises(TypeError):
            create_app(1)

    def test_config_name_accepts_valid_value(self):
        """Test that create_app() passes when config_name is a valid selection."""
        try:
            create_app('development')
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_config_name_rejects_invalid_value(self):
        """Test that create_app() fails when config_name is not a valid selection."""
        with self.assertRaises(ValueError):
            create_app('foo')

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


if __name__ == '__main__':
    unittest.main()
