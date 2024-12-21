"""Unit tests for the Flask demo.

**NOTES:**

- Remember to activate your Python virtual environment first:

    - source .venv/bin/activate (Linux)
    - .venv/Scripts/activate (Windows)

- Test from the project directory (e.g., `flask-demo`, not `tracker_XX`)
- Do not log events when unit testing or each test will create a log file.
- Using `--buffer` and `--verbose` together provides a good balance of output,
  since `--buffer` hides console output from the application
  and `--verbose` displays the test's docstring
  (ex., `Test that check_system() fails because min_python_version is not type float ... ok`)

Usage:

```
python -B -m unittest discover tracker_XX/tests -b -v
```
"""

from tracker_10 import create_app
from tracker_10.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestApp(BaseTestCase):
    """Unit tests for functions and methods in the application's __init__.py.

    :param unittest.TestCase.BaseTestCase: Inherited from tests/__init__.py
    """

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
        self.assertIn(b'Tracker', response.data)

    def test_not_found_response_code(self):
        """Test that the Not Found page was created by looking at the response code"""
        response = self.client.get('/oops', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_not_found_content(self):
        """Test that the Not Found page contains the correct contents"""
        response = self.client.get('/oops', follow_redirects=True)
        self.assertIn(b'Not Found', response.data)

    def test_error_response(self):
        """Test that the testing config returned a runtime error"""
        with self.assertRaises(RuntimeError):
            self.client.get('/doh', follow_redirects=True)

    def test_error_content_and_code(self):
        """Test that the Error page returns the correct code and contents.

        For this test, you cannot use the 'testing' configuration class.
        """
        # Create an application instance
        app = create_app(config_name='default', log_events=True)
        app_context = app.app_context()
        app_context.push()
        client = app.test_client()
        # Get and test the response
        response = client.get('/doh', follow_redirects=True)
        self.assertIn(b'Internal Server Error', response.data)
        self.assertEqual(response.status_code, 500)
        # Tear down the application instance
        app_context.pop()
        app = None
        app_context = None
        client = None

    def test_config_name_is_string(self):
        """Test that create_app() passes when config_name is a string."""
        try:
            create_app('testing')
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_config_name_is_not_string(self):
        """Test that create_app() fails when config_name is not a string."""
        with self.assertRaises(TypeError):
            create_app(1)

    def test_config_name_accepts_valid_value(self):
        """Test that create_app() passes when config_name is a valid selection."""
        try:
            create_app('testing')
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_config_name_accepts_valid_profiling_value(self):
        """Test that create_app() passes when config_name is a 'profile'."""
        try:
            create_app('profile')
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_config_name_rejects_invalid_value(self):
        """Test that create_app() fails when config_name is not a valid selection."""
        with self.assertRaises(ValueError):
            create_app('foo')

    def test_log_events_is_bool(self):
        """Test that create_app() passes when log_events is a boolean."""
        try:
            create_app(log_events=False)
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_log_events_is_not_bool(self):
        """Test that create_app() fails when config_name is not a string."""
        with self.assertRaises(TypeError):
            create_app(log_events=1)
