"""Unit tests for app.py

Run from the project;s root directory (e.g., ../flask-template)

Ensure you have an empty __init__.py in the 'tests' directory

Usage: python3 -m unittest --verbose --buffer tests.test_app
"""
import unittest
from app import app

__author__ = 'Rob Garcia'


class TestApp(unittest.TestCase):
    """Unit tests for app.py

    :param class unittest.TestCase: Class to test single test cases

    :returns: None
    """

    def setUp(self):
        """Create the application instance"""
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clear out the application instance"""
        self.app_context.pop()
        self.app = None
        self.app_context = None
        self.client = None

    def test_app(self):
        """Ensure you created the application instance"""
        assert self.app is not None
        assert app == self.app

    def test_index_response_code(self):
        """Test landing page response"""
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        """Check landing page contents"""
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'<h1>Welcome!</h1>', response.data)


if __name__ == '__main__':
    unittest.main()
