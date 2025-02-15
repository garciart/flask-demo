"""Authorization Forms Manager
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField)
from wtforms.validators import DataRequired

from tracker_99 import db, constants as c

class LoginForm(FlaskForm):
    """Parameters for the login form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """
    member_name = StringField('Member Name', validators=[DataRequired()])
    password = PasswordField(c.PASSWORD_FIELD_LABEL, validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
