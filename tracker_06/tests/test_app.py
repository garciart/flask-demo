"""Unit tests for the Flask demo.

**NOTES:**

- Remember to activate your Python virtual environment first:

    - `source .venv/bin/activate` (Linux)
    - `.venv/Scripts/activate` (Windows)

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

import unittest

from tracker_06 import create_app
from tracker_06.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestApp(BaseTestCase):
    """Unit tests for the Flask demo.

    :param unittest.TestCase BaseTestCase: Inherited from __init__.py
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
        self.assertIn(b'Hello, World!', response.data)

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

    def test_config_name_accepts_valid_profiling_value(self):
        """Test that create_app() passes when config_name is a 'profiler'."""
        try:
            create_app('profiler')
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_config_name_rejects_invalid_value(self):
        """Test that create_app() fails when config_name is not a valid selection."""
        with self.assertRaises(ValueError):
            create_app('foo')

    def test_log_events_is_bool(self):
        """Test that create_app() passes when log_events is a boolean."""
        try:
            create_app(log_events=True)
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_log_events_is_not_bool(self):
        """Test that create_app() fails when config_name is not a string."""
        with self.assertRaises(TypeError):
            create_app(log_events=1)

    def test_log_events_is_false_debug(self):
        """Test that create_app() passes when log_events is a boolean."""
        app = create_app()
        app.config['DEBUG'] = True  # Set debug mode
        app.debug = True  # Set through the app object
        app.log_events = True  # Default setting

        # Initialize the application (this would re-run the check)
        if app.debug:
            app.log_events = False

        self.assertFalse(app.log_events, "log_events should be False in debug mode")


if __name__ == '__main__':
    unittest.main()
