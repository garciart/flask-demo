"""Administration forms manager
"""

import re
from flask_wtf import FlaskForm
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from tracker_99 import db
from tracker_99.models.models import Member


INVALID_PASSWORD_MSG = (
    'Password must be between 8-15 characters long, '
    + 'contain at least one uppercase letter, one lowercase letter, and one number.'
)
PASSWORD_FIELD_LABEL = 'Repeat Password'
INVALID_EMAIL_MSG = 'Email address already exists.'


class AddMemberForm(FlaskForm):
    """Parameters for the Add Member form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """

    member_name = StringField('Username', validators=[DataRequired()])
    member_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        PASSWORD_FIELD_LABEL, validators=[DataRequired(), EqualTo('password')]
    )
    member_is_admin = BooleanField('This member an administrator')
    submit = SubmitField('Add Member')

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_member_name(self, member_name: StringField) -> None:
        """Check if a member already exists in the database.

        :param StringField member_name: The name to check

        :raises ValidationError: If the submitted name already exists

        :returns: None
        :rtype: None
        """
        if member_name_exists(db.session, member_name.data):
            raise ValidationError('Name already exists.')

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_member_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        if member_email_exists(db.session, member_email.data):
            raise ValidationError(INVALID_EMAIL_MSG)

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_password(self, password: PasswordField) -> None:
        """Ensure the password meets validation criteria.

        :param PasswordField password: The plain text password to check

        :raises ValidationError: If the submitted password does not meet the complexity requirements

        :returns: None
        :rtype: None
        """
        if not password_is_valid(password.data):
            raise ValidationError(INVALID_PASSWORD_MSG)


class EditMemberForm(FlaskForm):
    """Parameters for the Edit Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_name = StringField('Username', validators=[DataRequired()])
    member_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField(PASSWORD_FIELD_LABEL, validators=[EqualTo('password')])
    member_is_admin = BooleanField('This member is an administrator')
    submit = SubmitField('Update Member')

    def __init__(
        self, current_member_name: str, current_member_email: str, *args, **kwargs
    ) -> None:
        """Get the name and email of the member being edited.

        :param str current_member_name: The member's name
        :param str current_member_email: The member's current email

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.current_member_name = current_member_name
        self.current_member_email = current_member_email

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_member_name(self, member_name: StringField) -> None:
        """Check if a member already exists in the database.

        :param StringField member_name: The name to check

        :raises ValidationError: If the submitted name already exists

        :returns: None
        :rtype: None
        """
        if member_name.data != self.current_member_name and member_name_exists(
            db.session, member_name.data
        ):
            raise ValidationError('Name already exists.')

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_member_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        if member_email.data != self.current_member_email and member_email_exists(
            db.session, member_email.data
        ):
            raise ValidationError(INVALID_EMAIL_MSG)

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_password(self, password: PasswordField) -> None:
        """Ensure the password meets validation criteria.

        :param PasswordField password: The plain text password to check

        :raises ValidationError: If the submitted password does not meet the complexity requirements

        :returns: None
        :rtype: None
        """
        if password.data.strip() != '' and not password_is_valid(password.data):
            raise ValidationError(INVALID_PASSWORD_MSG)


class UpdateProfileForm(FlaskForm):
    """Parameters for the Update Profile form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField(PASSWORD_FIELD_LABEL, validators=[EqualTo('password')])
    submit = SubmitField('Update Member')

    def __init__(self, current_member_email: str, *args, **kwargs) -> None:
        """Get the email of the member being edited.

        :param str current_member_email: The member's current email

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.current_member_email = current_member_email

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_member_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        if member_email.data != self.current_member_email and member_email_exists(
            db.session, member_email.data
        ):
            raise ValidationError(INVALID_EMAIL_MSG)

    # MUST USE validate_{field_name} PATTERN WITH Flask-WTF!
    def validate_password(self, password: PasswordField) -> None:
        """Ensure the password meets validation criteria.

        :param PasswordField password: The plain text password to check

        :raises ValidationError: If the submitted password does not meet the complexity requirements

        :returns: None
        :rtype: None
        """

        if password.data.strip() != '' and not password_is_valid(password.data):
            raise ValidationError(INVALID_PASSWORD_MSG)


class DeleteMemberForm(FlaskForm):
    """Parameters for the Delete Member form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """

    submit = SubmitField('Delete Member')


def member_name_exists(session: Session, member_name: str) -> bool:
    """Check if the member name already exists in the database.

    :param Session session: The current database session
    :param str member_name: The name to check

    :returns: If the name exists
    :rtype: bool
    """
    return (
        session.scalar(
            select(Member).where(func.lower(Member.member_name) == func.lower(member_name))
        )
        is not None
    )


def member_email_exists(session: Session, member_email: str) -> bool:
    """Check if the email address already exists in the database.

    :param Session session: The current database session
    :param str member_name: The email address to check

    :returns: If the email address exists
    :rtype: bool
    """
    return (
        session.scalar(
            select(Member).where(func.lower(Member.member_email) == func.lower(member_email))
        )
        is not None
    )


def password_is_valid(submitted_password: str) -> bool:
    """Ensure the password meets validation criteria.

    - A minimum of eight characters
    - A maximum of fifteen characters
    - At least one uppercase letter, one lowercase letter and one number

    :param str password: The plain text password to check

    :returns: If the submitted password does not meet the complexity requirements
    :rtype: bool
    """
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,15}$'
    return False if not re.fullmatch(password_regex, submitted_password) else True
