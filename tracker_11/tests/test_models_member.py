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

import unittest  # pylint: disable=unused-import

from tracker_11.models.member import Member
from tracker_11.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestModelsMember(BaseTestCase):
    """Unit tests for Member model.

    :param unittest.TestCase.BaseTestCase: Inherited from __init__.py
    """

    def test_member_instantiated_pass(self):
        """Test that the Member model is instantiated args are correct"""
        _member = Member(member_name='John', member_email='john@foo.bar')
        _member.set_password('Change.Me.123')
        self.assertEqual(_member.member_name, 'John')
        self.assertEqual(_member.member_email, 'john@foo.bar')
        self.assertIsNotNone(_member.password_hash)

    def test_member_name_type_fail(self):
        """Test that the Member instantiation fails when member_name is not a string."""
        with self.assertRaises(TypeError):
            _member = Member(member_name=42, member_email='john@foo.bar')

    def test_member_name_invalid_fail(self):
        """Test that the Member instantiation fails when member_name is not valid."""
        with self.assertRaises(ValueError):
            _member = Member(member_name='foo', member_email='john@foo.bar')

    def test_member_email_type_fail(self):
        """Test that the Member instantiation fails when member_email is not a string."""
        with self.assertRaises(TypeError):
            _member = Member(member_name='John', member_email=42)

    def test_member_email_invalid_fail(self):
        """Test that the Member instantiation fails when member_email is not valid."""
        with self.assertRaises(ValueError):
            _member = Member(member_name='John', member_email='john')

    def test_member_password_type_fail(self):
        """Test that the Member instantiation fails when password is not a string."""
        with self.assertRaises(TypeError):
            _member = Member(member_name='John', member_email='john@foo.bar')
            _member.set_password(False)

    def test_member_password_invalid_fail(self):
        """Test that the Member instantiation fails when password is not valid."""
        with self.assertRaises(ValueError):
            _member = Member(member_name='John', member_email='john@foo.bar')
            _member.set_password('foo')

    def test_member_repr_pass(self):
        """Test that the Member model provides an accurate representation"""
        try:
            _member = Member(member_name='John', member_email='john@foo.bar')
            _member.set_password('Change.Me.123')
            _repr = str(_member.__repr__)
            self.assertIn('John', _repr)
        except (TypeError, ValueError):
            self.fail('Method raised an exception unexpectedly.')

    def test_verify_password_pass(self):
        """Test that verify_password() passes when the password is correct."""
        _member = Member(member_name='John', member_email='john@foo.bar', password='Change.Me.123')
        self.assertTrue(_member.verify_password('Change.Me.123',
                                               _member.password_hash))

    def test_verify_password_type_fail(self):
        """Test that verify_password() fails when the password is the wrong type."""
        with self.assertRaises(TypeError):
            _member = Member(member_name='John', member_email='john@foo.bar',
                             password='Change.Me.123')
            _member.set_password(False)

    def test_verify_password_value_fail(self):
        """Test that verify_password() fails when the password is incorrect."""
        _member = Member(member_name='John', member_email='john@foo.bar', password='Change.Me.123')
        self.assertFalse(_member.verify_password('foo', _member.password_hash))
