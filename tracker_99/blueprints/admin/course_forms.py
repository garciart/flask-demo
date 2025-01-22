"""Course forms manager
"""

from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import StringField, PasswordField, SubmitField, Form, Field
from wtforms.validators import (
    ValidationError,
    DataRequired,
    EqualTo,
    Length,
    Regexp,
    Optional,
)
from wtforms.widgets import TextArea

from tracker_99 import db, constants as c
from tracker_99.models.models import Course


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
    # SELECT * FROM courses
    # WHERE courses.course_name='Building Secure Python Applications' AND
    #     course_code='SDEV 300' LIMIT 1;
    existing_course = Course.query.filter(
        Course.course_name == course_name, Course.course_code == course_code
    ).first()

    if existing_course:
        raise ValidationError(f"A course named '{course_name}' ({course_code}) already exists.")


class AddCourseForm(FlaskForm):
    """Parameters for the Add Course form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    course_name = StringField(
        'Course',
        validators=[
            DataRequired(),
            Length(max=64),
            Regexp(c.TEXT_REGEX, message=c.INVALID_TEXT_MSG),
        ],
    )
    course_code = StringField(
        'Code',
        validators=[
            DataRequired(),
            Length(max=64),
            validate_unique_course,
            Regexp(c.TEXT_REGEX, message=c.INVALID_TEXT_MSG),
        ],
    )
    course_group = StringField('Group', validators=[Length(max=64)])
    course_key = PasswordField(
        'Course Key',
        validators=[
            DataRequired(),
            Length(max=15),
            Regexp(c.PASSWORD_REGEX, message=c.INVALID_PASSWORD_MSG),
        ],
    )
    course_key2 = PasswordField(
        'Repeat Course Key', validators=[DataRequired(), EqualTo('course_key')]
    )
    course_desc = StringField('Description', widget=TextArea(), validators=[Length(max=256)])
    submit = SubmitField('Add Course')


class EditCourseForm(FlaskForm):
    """Parameters for the Edit Course form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    course_name = StringField(
        'Course',
        validators=[
            DataRequired(),
            Length(max=64),
            Regexp(c.TEXT_REGEX, message=c.INVALID_TEXT_MSG),
        ],
    )
    course_code = StringField(
        'Code',
        validators=[
            DataRequired(),
            Length(max=64),
            Regexp(c.TEXT_REGEX, message=c.INVALID_TEXT_MSG),
        ],
    )
    course_group = StringField('Group', validators=[Length(max=64)])
    course_key = PasswordField(
        'Course Key',
        validators=[
            Optional(),
            Length(max=15),
            Regexp(c.PASSWORD_REGEX, message=c.INVALID_PASSWORD_MSG),
        ],
    )
    course_key2 = PasswordField('Repeat Course Key', validators=[EqualTo('course_key')])
    course_desc = StringField('Description', widget=TextArea(), validators=[Length(max=256)])
    submit = SubmitField('Update Course')

    def __init__(self, current_course_name: str, current_course_code: str, *args, **kwargs) -> None:
        """Get the name and code of the course being edited.

        :param str current_course_name: The course's current name
        :param str current_course_email: The course's current code

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.current_course_name = current_course_name
        self.current_course_code = current_course_code

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_course_name(self, course_name: StringField) -> None:
        """Check if a course and its code already exist in the database.

        :param StringField course_name: The course's long name

        :raises ValidationError: If the submitted name and code already exist

        :returns: None
        :rtype: None
        """
        # SELECT course_name, course_code FROM courses
        # WHERE LOWER(course_name) = LOWER("database security")
        # AND LOWER(course_code) = LOWER("sdev 350");
        if (
                course_name.data != self.current_course_name
                or self.course_code.data != self.current_course_code
        ):
            _result = db.session.query(Course.course_name, Course.course_code).filter(
                func.lower(Course.course_name) == func.lower(course_name.data),
                func.lower(Course.course_code) == func.lower(self.course_code.data),
            ).all()

            if _result:
                raise ValidationError(
                    f"A course named '{course_name.data}' ({self.course_code.data}) already exists."
                )


class DeleteCourseForm(FlaskForm):
    """Parameters for the Delete Course form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    submit = SubmitField('Delete Course')
