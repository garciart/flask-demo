"""Member forms manager
"""

from flask_wtf import FlaskForm
from sqlalchemy import func, select
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp,
    Optional,
)

from tracker_99 import db, constants as c
from tracker_99.models.models import Member


class AddMemberForm(FlaskForm):
    """Parameters for the Add Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_name = StringField(
        'Member Name',
        validators=[
            DataRequired(),
            Length(max=64),
            Regexp(c.NAME_REGEX, message=c.INVALID_NAME_MSG),
        ],
    )
    member_email = StringField('Email', validators=[DataRequired(), Email(), Length(max=320)])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(max=15),
            Regexp(c.PASSWORD_REGEX, message=c.INVALID_PASSWORD_MSG),
        ],
    )
    password2 = PasswordField(
        c.PASSWORD_FIELD_LABEL, validators=[DataRequired(), EqualTo('password')]
    )
    is_admin = BooleanField('This member an administrator')
    submit = SubmitField('Add Member')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_member_name(self, member_name: StringField) -> None:
        """Check if a member already exists in the database.

        :param StringField member_name: The name to check

        :raises ValidationError: If the submitted name already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM members WHERE LOWER(members.member_name) = LOWER("LeTo.ATREIDES");
        if db.session.scalar(
                select(Member).where(func.lower(Member.member_name) == func.lower(member_name.data))
        ):
            raise ValidationError('Name already exists.')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_member_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM members
        # WHERE LOWER(members.member_email) = LOWER("LeTo.ATREIDES@atreides.com");
        if db.session.scalar(
                select(Member).where(
                    func.lower(Member.member_email) == func.lower(member_email.data))
        ):
            raise ValidationError(c.INVALID_EMAIL_MSG)


class EditMemberForm(FlaskForm):
    """Parameters for the Edit Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_name = StringField(
        'Member Name',
        validators=[
            DataRequired(),
            Length(max=64),
            Regexp(c.NAME_REGEX, message=c.INVALID_NAME_MSG),
        ],
    )
    member_email = StringField('Email', validators=[DataRequired(), Email(), Length(max=320)])
    password = PasswordField(
        'Password',
        validators=[
            Optional(),
            Length(max=15),
            Regexp(c.PASSWORD_REGEX, message=c.INVALID_PASSWORD_MSG),
        ],
    )
    password2 = PasswordField(c.PASSWORD_FIELD_LABEL, validators=[EqualTo('password')])
    is_admin = BooleanField('This member is an administrator')
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

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_member_name(self, member_name: StringField) -> None:
        """Check if a member already exists in the database.

        :param StringField member_name: The name to check

        :raises ValidationError: If the submitted name already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM members WHERE LOWER(members.member_name) = LOWER("LeTo.ATREIDES");
        if member_name.data != self.current_member_name and db.session.scalar(
                select(Member).where(func.lower(Member.member_name) == func.lower(member_name.data))
        ):
            raise ValidationError('Name already exists.')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_member_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM members
        # WHERE LOWER(members.member_email) = LOWER("LeTo.ATREIDES@atreides.com");
        if member_email.data != self.current_member_email and db.session.scalar(
                select(Member).where(
                    func.lower(Member.member_email) == func.lower(member_email.data))
        ):
            raise ValidationError(c.INVALID_EMAIL_MSG)


class UpdateProfileForm(FlaskForm):
    """Parameters for the Update Profile form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[
            Optional(),
            Length(max=15),
            Regexp(c.PASSWORD_REGEX, message=c.INVALID_PASSWORD_MSG),
        ],
    )
    password2 = PasswordField(c.PASSWORD_FIELD_LABEL, validators=[EqualTo('password')])
    submit = SubmitField('Update Member')

    def __init__(self, current_member_email: str, *args, **kwargs) -> None:
        """Get the email of the member being edited.

        :param str current_member_email: The member's current email

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.current_member_email = current_member_email

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_member_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM members WHERE
        # LOWER(members.member_email) = LOWER("LeTo.ATREIDES@atreides.com");
        if member_email.data != self.current_member_email and db.session.scalar(
                select(Member).where(
                    func.lower(Member.member_email) == func.lower(member_email.data))
        ):
            raise ValidationError(c.INVALID_EMAIL_MSG)


class DeleteMemberForm(FlaskForm):
    """Parameters for the Delete Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    submit = SubmitField('Delete Member')
