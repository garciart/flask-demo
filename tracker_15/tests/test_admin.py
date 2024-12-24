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
- Ensure CRSF protection is disabled in config.py when testing!

Usage:

```
python -B -m unittest discover tracker_XX/tests -b -v
```
"""

from unittest.mock import MagicMock, patch

from flask import url_for
from wtforms import ValidationError

from tracker_15.blueprints.admin.admin_forms import EditMemberForm
from tracker_15.tests import BaseTestCase

__author__ = 'Rob Garcia'


class TestAdmin(BaseTestCase):
    """Unit tests for functions and methods in the application's blueprints directory.

    Covers web and error pages (e.g., /index, /about, etc.)

    :param unittest.TestCase.BaseTestCase: Inherited from tests/__init__.py
    """

    def test_view_member_response_code(self):
        """Test that the view_member page was created by looking at the response code"""
        response = self.client.get('/admin/view_member/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_member_content(self):
        """Test that the view_member page contains the correct contents"""
        response = self.client.get('/admin/view_member/1', follow_redirects=True)
        self.assertIn(b'View Member', response.data)

    def test_edit_member_response_code(self):
        """Test that the edit_member page was created by looking at the response code"""
        response = self.client.get('/admin/edit_member/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_member_content(self):
        """Test that the index page contains the correct contents"""
        response = self.client.get('/admin/edit_member/1', follow_redirects=True)
        self.assertIn(b'Edit Member', response.data)

    # Mock the db.session.scalar
    @patch('tracker_15.blueprints.admin.admin_forms.db.session.scalar')
    def test_validate_member_name_exists(self, mock_scalar):
        """Test that the form raises a ValidationError if the member name already exists."""
        # Create a mock member object
        existing_member = MagicMock()
        existing_member.member_name = 'Admin'

        # Configure the mock to return the existing member
        mock_scalar.return_value = existing_member

        # Initialize the form with some test data
        form_data = {'member_name': 'Admin', 'member_email': 'admin@tracker.com'}
        form = EditMemberForm(
            current_member_name="different_member_name",
            current_member_email="different_member_email@example.com",
            data=form_data,
        )

        # Ensure the app and request contexts are pushed before form validation
        with self.app.app_context(), self.app.test_request_context():
            # Check that the ValidationError is raised because member name already exists
            with self.assertRaises(ValidationError) as context:
                form.validate_member_name(form.member_name)

            self.assertEqual(str(context.exception), 'Name already exists.')

    # Mock the db.session.scalar
    @patch('tracker_15.blueprints.admin.admin_forms.db.session.scalar')
    def test_validate_member_email_exists(self, mock_scalar):
        """Test that the form raises a ValidationError if the member email already exists."""
        # Create a mock member object
        existing_member = MagicMock()
        existing_member.member_name = 'Admin'
        existing_member.member_email = 'admin@tracker.com'

        # Configure the mock to return the existing member
        mock_scalar.return_value = existing_member

        # Initialize the form with some test data
        form_data = {'member_name': 'Admin', 'member_email': 'admin@tracker.com'}
        form = EditMemberForm(
            current_member_name="different_member_name",
            current_member_email="different_member_email@example.com",
            data=form_data,
        )

        # Ensure the app and request contexts are pushed before form validation
        with self.app.app_context(), self.app.test_request_context():
            # Check that the ValidationError is raised because member email already exists
            with self.assertRaises(ValidationError) as context:
                form.validate_member_email(form.member_email)

            self.assertEqual(str(context.exception), 'Email address already exists.')

    @patch('tracker_15.blueprints.admin.admin_routes.EditMemberForm')
    @patch('tracker_15.models.member.db.session.commit')
    def test_edit_member_valid_form(self, mock_commit, mock_edit_member_form):
        """Test the behavior when the form is valid (successful POST)."""

        # Create a mock member object
        member_id = 1
        mock_member = MagicMock()
        mock_member.id = member_id
        mock_member.member_name = 'Admin'
        mock_member.member_email = 'admin@tracker.com'
        mock_member.member_is_admin = True
        # Mock password hashing method
        mock_member.set_password = MagicMock()

        # Patch the form to simulate successful validation
        mock_form = MagicMock()
        mock_form.validate_on_submit.return_value = True  # Simulate successful form submission
        mock_form.member_name.data = 'Administrator'
        mock_form.member_email.data = 'admin@tracker.com'
        mock_form.member_is_admin.data = True
        mock_form.password.data = 'Change.Me.123'  # Ensure this value is set for the test

        # Mock the EditMemberForm constructor to return the mock form
        mock_edit_member_form.return_value = mock_form

        # Use test client to simulate the POST request with application context
        with self.app.app_context(), patch(
            'tracker_15.models.member.Member.query.get_or_404', return_value=mock_member
        ):
            response = self.client.post(
                url_for('admin_bp.edit_member', member_id=member_id),
                data={
                    'member_name': 'Admin',
                    'member_email': 'admin@tracker.com',
                    'password': 'Change.Me.123',  # Ensure the password is set here
                    'member_is_admin': True,
                },
            )

        # Ensure the member's information is updated
        self.assertEqual(mock_member.member_name, 'Admin')
        self.assertEqual(mock_member.member_email, 'admin@tracker.com')
        self.assertTrue(mock_member.member_is_admin)

        # Ensure the commit was called to save the changes to the database
        mock_commit.assert_called_once()

        # Ensure a redirect occurred (to the members page or a specified route)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('index'))
