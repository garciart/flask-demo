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

from tracker_12.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestPages(BaseTestCase):
    """Unit tests for functions and methods in the application's blueprints directory.

    Covers web and error pages (e.g., /index, /about, etc)

    :param unittest.TestCase BaseTestCase: Inherited from tests/__init__.py
    """

    def test_index_response_code(self):
        """Test that the index page was created by looking at the response code"""
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        """Test that the index page contains the correct contents"""
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Hello, World!', response.data)

    def test_about_response_code(self):
        """Test that the about page was created by looking at the response code"""
        response = self.client.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_content(self):
        """Test that the about page contains the correct contents"""
        response = self.client.get('/about', follow_redirects=True)
        self.assertIn(b'About', response.data)

    def test_not_found_response_code(self):
        """Test that the Not Found page was created by looking at the response code"""
        response = self.client.get('/oops', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_not_found_content(self):
        """Test that the Not Found page contains the correct contents"""
        response = self.client.get('/oops', follow_redirects=True)
        self.assertIn(b'Not Found', response.data)

    def test_error_response_code(self):
        """Test that the Error page was created by looking at the response code"""
        response = self.client.get('/doh', follow_redirects=True)
        self.assertEqual(response.status_code, 500)

    def test_error_content(self):
        """Test that the Error page contains the correct contents"""
        response = self.client.get('/doh', follow_redirects=True)
        self.assertIn(b'Internal Server Error', response.data)