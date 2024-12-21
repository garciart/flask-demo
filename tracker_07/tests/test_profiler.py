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

import flask

from tracker_07.profiler import add_profiler_middleware
from tracker_07.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestProfiler(BaseTestCase):
    """Unit tests for profiler utilities.

    :param unittest.TestCase.BaseTestCase: Inherited from __init__.py
    """

    def test_add_profiler_middleware_pass(self):
        """Test that add_profiler_middleware() passes when requirements met"""
        test_app = flask.Flask(__name__)
        try:
            add_profiler_middleware(app=test_app)
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_add_profiler_middleware_fail_type(self):
        """Test that add_profiler_middleware() fails when app is the wrong type"""
        test_var = 3.14
        with self.assertRaises(TypeError):
            add_profiler_middleware(app=test_var)
