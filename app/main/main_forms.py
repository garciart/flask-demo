"""Main forms manager.

updateStudentAttendanceForm = CourseAccessForm
attendanceCode = access_code
"Attendance Code" = 'Access Code'
updateClassAttendanceForm = UserAccessForm
classMembers = access_fields
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField

class SimpleForm(FlaskForm):
    submit = SubmitField()
