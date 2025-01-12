"""Administration Forms Manager.
"""
from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, PasswordField, SubmitField,
                     IntegerField)
from wtforms.widgets import TextArea
from wtforms.validators import (ValidationError, DataRequired, Email, EqualTo,
                                NumberRange, Length)
from sqlalchemy import select
from app import db
from app.models import (User, Role, Course)


class SimpleForm(FlaskForm):
    """Basic form to capture data on submit.
    """
    submit = SubmitField()


class AddCourseForm(FlaskForm):
    """Parameters for the Add Course form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    # CUSTOM VALIDATORS THAT DO NOT USE A FIELD NAME MUST BE DEFINED BEFORE USE!
    def validate_unique_course(form, field):
        """A custom validator to check if the course name and code combination is unique
        """
        course_name = form.course_name.data
        course_code = form.course_code.data

        # Query the database to check if a course with the same name and code exists
        existing_course = Course.query.filter_by(course_name=course_name, course_code=course_code).first()

        if existing_course:
            raise ValidationError(f"A course with name '{course_name}' and code '{course_code}' already exists.")

    course_name = StringField('Course', validators=[DataRequired(), Length(max=64)])
    course_code = StringField('Code', validators=[DataRequired(), Length(max=64), validate_unique_course])
    course_group = StringField('Group', validators=[Length(max=64)])
    course_desc = StringField('Description', widget=TextArea(), validators=[Length(max=256)])
    submit = SubmitField('Add Course')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_course_name(self, course_name: StringField) -> None:
        """Check if a course already exists in the database.

        :param StringField course_name: The course to check

        :raises ValidationError: If the submitted course already exists

        :returns: None
        :rtype: None
        """
        _course = db.session.scalar(select(Course).where(Course.course_name == course_name.data))
        if _course is not None:
            raise ValidationError('Course already exists.')


class EditCourseForm(FlaskForm):
    """Parameters for the Edit Course form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    course_name = StringField('Course', validators=[DataRequired(), Length(max=64)])
    course_code = StringField('Code', validators=[DataRequired(), Length(max=64)])
    course_group = StringField('Group', validators=[Length(max=64)])
    course_desc = StringField('Description', widget=TextArea(), validators=[Length(max=256)])
    submit = SubmitField('Update Course')

    def __init__(self, original_course_name: str, *args, **kwargs) -> None:
        """Get the name of the course being edited.

        :param str original_course_name: The edited course's name

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.original_course_name = original_course_name

    def validate_course_name(self, course_name: StringField) -> None:
        """Check if a course already exists in the database.

        :param StringField course_name: The course to check

        :raises ValidationError: If the submitted course already exists

        :returns: None
        :rtype: None
        """
        if course_name.data != self.original_course_name:
            _course = db.session.scalar(select(Course).where(Course.course_name == self.course_name.data))
            if _course is not None:
                raise ValidationError('Course already exists.')


class DeleteCourseForm(FlaskForm):
    """Parameters for the Delete Course form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    submit = SubmitField('Delete Course')


class AddRoleForm(FlaskForm):
    """Parameters for the Add Role form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    role_name = StringField('Role', validators=[DataRequired(),
                                                Length(max=64)])
    role_privilege = IntegerField(
        'Privilege Level', validators=[DataRequired(),
                                       NumberRange(min=0, max=15)])
    submit = SubmitField('Add Role')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_role_name(self, role_name: StringField) -> None:
        """Check if a role name already exists in the database.

        :param StringField role_name: The role name to check

        :raises ValidationError: If the submitted role name already exists

        :returns: None
        :rtype: None
        """
        _role = db.session.scalar(select(Role).where(Role.role_name == role_name.data))
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
        _role = db.session.scalar(select(Role).where(Role.role_privilege == role_privilege.data))
        if _role is not None:
            raise ValidationError('Privilege level already assigned.')


class EditRoleForm(FlaskForm):
    """Parameters for the Edit Role form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    role_name = StringField('Role name', validators=[DataRequired()])
    role_privilege = IntegerField(
        'Privilege Level', validators=[DataRequired(),
                                       NumberRange(min=0, max=15)])
    submit = SubmitField('Update Role')

    def __init__(self, original_role_name: str,
                 original_role_privilege: str,
                 *args: any, **kwargs: any) -> None:
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
            _role = db.session.scalar(select(Role).where(Role.role_name == self.role_name.data))
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
            _role = db.session.scalar(select(Role).where(Role.role_privilege == self.role_privilege.data))
            if _role is not None:
                raise ValidationError('Privilege level already assigned.')


class DeleteRoleForm(FlaskForm):
    """Parameters for the Delete Role form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    submit = SubmitField('Delete Role')


class AddUserForm(FlaskForm):
    """Parameters for the Add User form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    username = StringField('Username', validators=[DataRequired()])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('This user an administrator')
    submit = SubmitField('Add User')

    def validate_username(self, username):
        # type: (StringField) -> None
        """Check if a username already exists in the database.

        :param StringField username: The username to check

        :raises ValidationError: If the submitted username already exists

        :returns: None
        :rtype: None
        """
        _user = db.session.scalar(select(User).where(
            User.username == username.data))
        if _user is not None:
            raise ValidationError('User already exists.')

    def validate_email(self, user_email):
        # type: (StringField) -> None
        """Check if an email address already exists in the database.

        :param StringField user_email: The email address to check

        :raises ValidationError: If the submitted email address already exists

        :returns: None
        :rtype: None
        """
        _user = db.session.scalar(select(User).where(
            User.user_email == user_email.data))
        if _user is not None:
            raise ValidationError('Email address already exists.')


class EditUserForm(FlaskForm):
    """Parameters for the Edit Role form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    username = StringField('Username', validators=[DataRequired()])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField(
        'Repeat Password', validators=[EqualTo('password')])
    is_admin = BooleanField('This user an administrator')
    submit = SubmitField('Update User')

    def __init__(self, original_username, original_user_email,
                 *args, **kwargs):
        # type: (str, str, any, any) -> None
        """Get the username and email of the user being edited.

        :param str original_username: The edited user's username
        :param str original_user_email: The edited user's email

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_user_email = original_user_email

    def validate_username(self, username):
        # type: (StringField) -> None
        """Check if a username already exists in the database.

        :param StringField username: The username to check

        :raises ValidationError: If the submitted username already exists

        :returns: None
        :rtype: None
        """
        if username.data != self.original_username:
            _user = db.session.scalar(select(User).where(
                User.username == self.username.data))
            if _user is not None:
                raise ValidationError('Username already exists.')

    def validate_user_email(self, user_email):
        # type: (StringField) -> None
        """Check if a user's email already exists in the database.

        :param StringField user_email: The user's email to check

        :raises ValidationError: If the submitted user's email already exists

        :returns: None
        :rtype: None
        """
        if user_email.data != self.original_user_email:
            _user = db.session.scalar(select(User).where(
                User.user_email == self.user_email.data))
            if _user is not None:
                raise ValidationError('User email already exists.')

class DeleteUserForm(FlaskForm):
    """Parameters for the Delete User form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    submit = SubmitField('Delete User')


class UpdateProfileForm(FlaskForm):
    """Parameters for the Update Profile form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField(
        'Repeat Password', validators=[EqualTo('password')])
    submit = SubmitField('Update Profile')

    def __init__(self, original_user_email, *args, **kwargs):
        # type: (str, any, any) -> None
        """Get the email of the user being edited.

        :param str original_user_email: The edited user's email

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.original_user_email = original_user_email

    def validate_user_email(self, user_email):
        # type: (StringField) -> None
        """Check if a user's email already exists in the database.

        :param StringField user_email: The user's email to check

        :raises ValidationError: If the submitted user's email already exists

        :returns: None
        :rtype: None
        """
        if user_email.data != self.original_user_email:
            _user = db.session.scalar(select(User).where(
                User.user_email == self.user_email.data))
            if _user is not None:
                raise ValidationError('User email already exists.')
