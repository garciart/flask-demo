"""Course administration forms manager.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from sqlalchemy import select
from app import db
from app.models import Course


class AddCourseForm(FlaskForm):
    """Parameters for the Add Course form template.
    """
    course_name = StringField('Course', validators=[DataRequired()])
    course_code = StringField('Code', validators=[DataRequired()])
    course_group = StringField('Group')
    course_desc = StringField('Description')
    submit = SubmitField('Add Course')

    def validate_course_name(self, course_name):
        # type: (StringField) -> None
        """Check if a course already exists in the database.

        :param StringField course_name: The course to check
        :return: None
        :raises ValidationError: If the submitted course already exists
        """
        _course = db.session.scalar(select(Course).where(
            Course.course_name == course_name.data))
        if _course is not None:
            raise ValidationError('Course already exists.')


class EditCourseForm(FlaskForm):
    """Parameters for the Edit Course form template.
    """
    course_name = StringField('Course name', validators=[DataRequired()])
    submit = SubmitField('Update Course')

    def __init__(self, original_course_name, *args, **kwargs):
        # type: (str, any, any) -> None
        """Get the name of the course being edited.

        :params str original_course_name: The edited course's name
        :return: None
        """
        super().__init__(*args, **kwargs)
        self.original_course_name = original_course_name

    def validate_course_name(self, course_name):
        # type: (StringField) -> None
        """Check if a course already exists in the database.

        :param StringField course_name: The course to check
        :return: None
        :raises ValidationError: If the submitted course already exists
        """
        if course_name.data != self.original_course_name:
            _course = db.session.scalar(select(Course).where(
                Course.course_name == self.course_name.data))
            if _course is not None:
                raise ValidationError('Course already exists.')


class DeleteCourseForm(FlaskForm):
    """Parameters for the Delete Course form template.
    """
    submit = SubmitField('Delete Course')
