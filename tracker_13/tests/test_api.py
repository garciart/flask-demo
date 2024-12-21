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

from tracker_13.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestAPI(BaseTestCase):
    """Unit tests for functions and methods in the application's blueprints directory.

    Covers API requests

    :param unittest.TestCase.BaseTestCase: Inherited from tests/__init__.py
    """

    def test_api_get_favicon_response_code(self):
        """Test that an API call can find the favicon to avoid 404 errors"""
        response = self.client.get('/favicon.ico', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_get_test_data_response_code(self):
        """Test that the API test page was created by looking at the response code"""
        response = self.client.get('/api/test', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_get_test_data_content(self):
        """Test that the API test page contains the correct contents"""
        response = self.client.get('/api/test', follow_redirects=True)
        self.assertIn(b'Python 101', response.data)
        self.assertIn(b'Introduction to Flask', response.data)

    def test_api_get_all_members_response_code(self):
        """Test that the API members page was created by looking at the response code"""
        response = self.client.get('/api/members/all', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_get_all_members_content(self):
        """Test that the API members page contains the correct contents"""
        response = self.client.get('/api/members/all', follow_redirects=True)
        self.assertIn(b'Leto.Atreides', response.data)
        self.assertIn(b'stilgar.tabr@fremen.com', response.data)

    def test_api_single_member_response_code(self):
        """Test that the API member # page was created by looking at the response code"""
        response = self.client.get('/api/members/3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_single_member_content(self):
        """Test that the API member # page contains the correct contents"""
        response = self.client.get('/api/members/3', follow_redirects=True)
        self.assertIn(b'Paul.Atreides', response.data)

    def test_api_single_member_content_fail(self):
        """Test that an incorrect API member # page contains an error message"""
        response = self.client.get('/api/members/0', follow_redirects=True)
        self.assertIn(b'Member not found', response.data)
