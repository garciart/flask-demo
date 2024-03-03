"""Administration Forms Manager
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from sqlalchemy import select
from app import db
from app.models import User

class CreateUserForm(FlaskForm):
    """Parameters for the Create User form template.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """_summary_

        :param username: _description_
        :type username: _type_
        :raises ValidationError: If the submitted username already exists
        """
        print('username', username, type(username))
        user = db.session.scalar(select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """_summary_

        :param email: _description_
        :type email: _type_
        :raises ValidationError: If the submitted email already exists
        """
        print('email', email, type(email))
        user = db.session.scalar(select(User).where(
            User.user_email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
