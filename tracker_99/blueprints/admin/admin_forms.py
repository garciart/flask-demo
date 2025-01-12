"""Administration forms manager
"""

import re

from flask_wtf import FlaskForm
from sqlalchemy import func, select
from wtforms import BooleanField, IntegerField, StringField, PasswordField, SubmitField, Form, Field
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Regexp, Optional,
)
from wtforms.widgets import TextArea

from tracker_99 import db
from tracker_99.models.models import Course, Member, Role

# Ensure the password meets validation criteria.
# - A minimum of eight characters
# - A maximum of fifteen characters
# - At least one uppercase letter, one lowercase letter and one number
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,15}$'
INVALID_PASSWORD_MSG = (
    'Password must be between 8-15 characters long, '
    + 'contain at least one uppercase letter, one lowercase letter, and one number.'
)
PASSWORD_FIELD_LABEL = 'Repeat Password'
INVALID_EMAIL_MSG = 'Email address already exists.'


# CUSTOM VALIDATORS WITHOUT A FIELD NAME IN THE FUNCTION NAME MUST BE DEFINED BEFORE USE!
def validate_unique_course(form: Form, field: Field) -> None:
    """A custom validator to check if the course name and code combination is unique.

    :param Form form: The form to validate (normally the name of the class)
    :param Field field: The field being validated
    """
    course_name = form.course_name.data
    course_code = field.data

    # Query the database to check if a course with the same name and code exists
    # but exclude the current course when editing
    # SELECT * FROM courses WHERE courses.course_name='Building Secure Python Applications' AND course_code='SDEV 300' LIMIT 1;
    existing_course = (
        Course.query.filter(Course.course_name == course_name, Course.course_code == course_code)
        .first()
    )

    if existing_course:
        raise ValidationError(
            f"A course with name '{course_name}' and code '{course_code}' already exists."
        )


class AddCourseForm(FlaskForm):
    """Parameters for the Add Course form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    course_name = StringField('Course', validators=[DataRequired(), Length(max=64)])
    course_code = StringField(
        'Code', validators=[DataRequired(), Length(max=64), validate_unique_course]
    )
    course_group = StringField('Group', validators=[Length(max=64)])
    course_desc = StringField('Description', widget=TextArea(), validators=[Length(max=256)])
    submit = SubmitField('Add Course')


class EditCourseForm(FlaskForm):
    """Parameters for the Edit Course form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    course_name = StringField('Course', validators=[DataRequired(), Length(max=64)])
    course_code = StringField(
        'Code', validators=[DataRequired(), Length(max=64), validate_unique_course]
    )
    course_group = StringField('Group', validators=[Length(max=64)])
    course_desc = StringField('Description', widget=TextArea(), validators=[Length(max=256)])
    submit = SubmitField('Update Course')


class DeleteCourseForm(FlaskForm):
    """Parameters for the Delete Course form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    submit = SubmitField('Delete Course')


class AddMemberForm(FlaskForm):
    """Parameters for the Add Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_name = StringField('Username', validators=[DataRequired(), Length(max=64)])
    member_email = StringField('Email', validators=[DataRequired(), Email(), Length(max=320)])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(max=15),
            Regexp(PASSWORD_REGEX, message=INVALID_PASSWORD_MSG),
        ],
    )
    password2 = PasswordField(
        PASSWORD_FIELD_LABEL, validators=[DataRequired(), EqualTo('password')]
    )
    is_admin = BooleanField('This member an administrator')
    submit = SubmitField('Add Member')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    @staticmethod
    def validate_member_name(member_name: StringField) -> None:
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
    @staticmethod
    def validate_member_email(member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM members WHERE LOWER(members.member_email) = LOWER("LeTo.ATREIDES@atreides.com");
        if db.session.scalar(
            select(Member).where(func.lower(Member.member_email) == func.lower(member_email.data))
        ):
            raise ValidationError(INVALID_EMAIL_MSG)


class EditMemberForm(FlaskForm):
    """Parameters for the Edit Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_name = StringField('Username', validators=[DataRequired(), Length(max=64)])
    member_email = StringField('Email', validators=[DataRequired(), Email(), Length(max=320)])
    password = PasswordField(
        'Password',
        validators=[Length(max=15), Regexp(PASSWORD_REGEX, message=INVALID_PASSWORD_MSG)],
    )
    password2 = PasswordField(PASSWORD_FIELD_LABEL, validators=[EqualTo('password')])
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
        # SELECT * FROM members WHERE LOWER(members.member_email) = LOWER("LeTo.ATREIDES@atreides.com");
        if member_email.data != self.current_member_email and db.session.scalar(
            select(Member).where(func.lower(Member.member_email) == func.lower(member_email.data))
        ):
            raise ValidationError(INVALID_EMAIL_MSG)


class UpdateProfileForm(FlaskForm):
    """Parameters for the Update Profile form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    member_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[Optional(), Length(max=15), Regexp(PASSWORD_REGEX, message=INVALID_PASSWORD_MSG)],
    )
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

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_member_email(self, member_email: StringField) -> None:
        """Check if an email address already exists in the database.

        :param StringField member_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM members WHERE LOWER(members.member_email) = LOWER("LeTo.ATREIDES@atreides.com");
        if member_email.data != self.current_member_email and db.session.scalar(
            select(Member).where(func.lower(Member.member_email) == func.lower(member_email.data))
        ):
            raise ValidationError(INVALID_EMAIL_MSG)


class DeleteMemberForm(FlaskForm):
    """Parameters for the Delete Member form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    submit = SubmitField('Delete Member')


class AddRoleForm(FlaskForm):
    """Parameters for the Add Role form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    role_name = StringField('Role', validators=[DataRequired(), Length(max=64)])
    role_privilege = IntegerField(
        'Privilege Level', validators=[DataRequired(), NumberRange(min=1, max=3)]
    )
    submit = SubmitField('Add Role')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    @staticmethod
    def validate_role_name(role_name: StringField) -> None:
        """Check if a role name already exists in the database.

        :param StringField role_name: The role name to check

        :raises ValidationError: If the submitted role name already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM roles WHERE LOWER(roles.role_name) = LOWER("ChAiR");
        _role = db.session.scalar(
            select(Role).where(func.lower(Role.role_name) == func.lower(role_name.data))
        )
        if _role is not None:
            raise ValidationError('Role name already exists.')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    @staticmethod
    def validate_role_privilege(role_privilege: IntegerField) -> None:
        """Check if a privilege level already exists in the database.

        :param IntegerField role_privilege: The privilege level to check

        :raises ValidationError: If the submitted privilege level already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM roles WHERE roles.role_privilege = 3;
        _role = db.session.scalar(select(Role).where(Role.role_privilege == role_privilege.data))
        if _role is not None:
            raise ValidationError('Privilege level already assigned.')


class EditRoleForm(FlaskForm):
    """Parameters for the Edit Role form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """

    role_name = StringField('Role name', validators=[DataRequired()])
    role_privilege = IntegerField(
        'Privilege Level', validators=[DataRequired(), NumberRange(min=1, max=3)]
    )
    submit = SubmitField('Update Role')

    def __init__(
        self, original_role_name: str, original_role_privilege: str, *args: any, **kwargs: any
    ) -> None:
        """Get the name and privilege of the role being edited.

        :param str original_role_name: The edited role's name
        :param int original_role_privilege: The edited role's privilege level

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.original_role_name = original_role_name
        self.original_role_privilege = original_role_privilege

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_role_name(self, role_name: StringField) -> None:
        """Check if a role name or already exists in the database.

        :param StringField role_name: The role name to check

        :raises ValidationError: If the submitted role name already exists

        :returns: None
        :rtype: None
        """
        if role_name.data != self.original_role_name:
            # SELECT * FROM roles WHERE LOWER(roles.role_name) = LOWER("ChAiR");
            _role = db.session.scalar(
                select(Role).where(func.lower(Role.role_name) == func.lower(role_name.data))
            )
            if _role is not None:
                raise ValidationError('Role name already exists.')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_role_privilege(self, role_privilege: IntegerField) -> None:
        """Check if a privilege level already exists in the database.

        :param IntegerField role_privilege: The privilege level to check

        :raises ValidationError: If the submitted privilege level already exists

        :returns: None
        :rtype: None
        """
        if role_privilege.data != self.original_role_privilege:
            # SELECT * FROM roles WHERE roles.role_privilege = 3;
            _role = db.session.scalar(
                select(Role).where(Role.role_privilege == role_privilege.data)
            )
            if _role is not None:
                raise ValidationError('Privilege level already assigned.')


class DeleteRoleForm(FlaskForm):
    """Parameters for the Delete Role form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    submit = SubmitField('Delete Role')


class SimpleForm(FlaskForm):
    """Basic form to capture data on submit."""

    submit = SubmitField()
