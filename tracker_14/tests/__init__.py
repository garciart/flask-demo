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

import importlib
import sys
import unittest

from tracker_14 import create_app


class BaseTestCase(unittest.TestCase):
    """Base test case for Flask applications.

    This class sets up the application context and provides methods
    to be shared across different test modules.
    """

    CONFIG_NAME = 'testing'

    def setUp(self):
        """This method runs before each test"""
        # Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
        self.sys_python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

        # Get the Flask major and minor version numbers and convert them to a float
        raw_flask_version = importlib.metadata.version("flask")
        flask_version_major, flask_version_minor = map(int, raw_flask_version.split('.')[:2])
        self.sys_flask_version = float(f"{flask_version_major}.{flask_version_minor:02d}")

        # Create the application instance
        self.app = create_app(self.CONFIG_NAME)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """This method runs after each test"""

        # Clear out the application instance variables
        self.app_context.pop()
        self.app = None
        self.app_context = None
        self.client = None


if __name__ == '__main__':
    unittest.main()
