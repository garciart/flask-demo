"""Main forms manager.

updateStudentAttendanceForm = CourseAccessForm
attendanceCode = access_code
"Attendance Code" = 'Access Code'
updateClassAttendanceForm = UserAccessForm
classMembers = access_fields
"""
from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, RadioField, StringField, SubmitField


class CourseAccessForm(FlaskForm):
    """Parameters for the sub-form with radio buttons to choose course
    access privileges.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    access_code = RadioField(
        'Access Code',
        choices=[(1, 'Principal'), (2, 'Teacher'), (3, 'Student'),
                 (4, 'No Access')],
    )
    submit = SubmitField('Assign Course(s) to User(s)')


class UserAccessForm(FlaskForm):
    """Parameters for the WTForm that will display the username
    and course access privileges.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """
    title = StringField('title')
    access_fields = FieldList(FormField(CourseAccessForm))
