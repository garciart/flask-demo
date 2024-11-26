"""Administration forms manager
"""

from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import (BooleanField, StringField, PasswordField, SubmitField)
from wtforms.validators import (ValidationError, DataRequired, Email, EqualTo)

from tracker_14 import db
from tracker_14.models.member import Member


class EditMemberForm(FlaskForm):
    """Parameters for the Edit Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """
    member_name = StringField('Username', validators=[DataRequired()])
    member_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password')])
    member_is_admin = BooleanField('This member an administrator')
    submit = SubmitField('Update Member')

    def __init__(self, current_member_name: str,
                 current_member_email: str,
                 *args, **kwargs) -> None:
        """Get the username and email of the user being edited.

        :param str current_member_name: The member's current username
        :param str current_member_email: The member's current email

        :returns None: None
        """
        super().__init__(*args, **kwargs)
        self.current_member_name = current_member_name
        self.current_member_email = current_member_email

    def check_member_name(self, member_name: StringField) -> None:
        """Check if a member already exists in the database.

        :param StringField member_name: The member name to check

        :raises ValidationError: If the submitted member name already exists

        :returns None: None
        """
        if member_name.data != self.current_member_name:
            _member = db.session.scalar(select(Member).where(
                Member.member_name == member_name.data))
            if _member is not None:
                raise ValidationError('Member already exists.')

    def check_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns None: None
        """
        if member_email.data != self.current_member_email:
            _member = db.session.scalar(select(Member).where(
                Member.member_email == member_email.data))
            if _member is not None:
                raise ValidationError('Email address already exists.')
