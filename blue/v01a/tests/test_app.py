"""Unit tests for the Flask demo.

Run from the project directory (e.g., ../flask-demo)

Ensure you have an empty __init__.py in the 'tests' directory

Usage: python -B -m unittest --verbose --buffer v01a/tests/test_app.py
"""
import unittest
from v01a import create_app

__author__ = 'Rob Garcia'


class TestApp(unittest.TestCase):
    """Unit tests for the Flask demo.

    :param class unittest.TestCase: Class to test single test cases
    """

    def setUp(self):
        """Create the application instance"""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_app(self):
        """Ensure you created the application instance"""
        assert self.app is not None

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


if __name__ == '__main__':
    unittest.main()
