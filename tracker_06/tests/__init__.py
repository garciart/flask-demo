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
import importlib
import sys
import unittest

from tracker_06 import create_app


class BaseTestCase(unittest.TestCase):
    """Base test case for Flask applications.

    This class sets up the application context and provides methods
    to be shared across different test modules.
    """
    CONFIG_NAME = 'default'

    def setUp(self):
        """Create the application instance"""
        # Get the Python version number and convert it to float (e.g., 3.9 -> 3.09)
        self.sys_python_version = float(f"{sys.version_info.major}.{sys.version_info.minor:02d}")

        # Get the Flask major and minor version numbers and convert them to a float
        raw_flask_version = importlib.metadata.version("flask")
        flask_version_major, flask_version_minor = map(int, raw_flask_version.split('.')[:2])
        self.sys_flask_version = float(f"{flask_version_major}.{flask_version_minor:02d}")

        self.app = create_app(self.CONFIG_NAME)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clear out the application instance variables"""
        self.app_context.pop()
        self.app = None
        self.app_context = None
        self.client = None
