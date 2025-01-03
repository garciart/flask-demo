"""Authorization Forms Manager
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Parameters for the login form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """
    member_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
