"""Unit tests for app.py

Run from the project;s root directory (e.g., ../flask_demo)

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

    def test_index(self):
        # type: () -> None
        """Unit test placeholder
        """


if __name__ == '__main__':
    unittest.main()
