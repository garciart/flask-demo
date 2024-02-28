"""Database models
"""
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from app.cm_utils import validate_input

# - 'flask db init' to create migration repository
# - 'flask db migrate -m "<message>"' to generate a migration script
#       after making changes to the schema
# - 'flask db upgrade' to apply changes
# - 'flask db downgrade' to undo migration


@login.user_loader
def load_user(user_id):
    """_summary_

    :param int user_id: The user ID to search for

    :return: A user object
    :rtype: app.models.User
    """
    # Validate inputs
    validate_input('user_id', user_id, int)

    return db.session.get(User, user_id)


class User(UserMixin, db.Model):
    """User database model
    """
    __tablename__ = 'users'

    user_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True)
    user_group: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(64), index=True)
    user_email: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256))

    associations: so.Mapped[List['Association']] = so.relationship(
        back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        """Overrides UserMixin get_id so you can use user_id instead of id.

        :return: The user id
        :rtype: int
        """
        return self.user_id

    def set_password(self, password):
        """Hashes a password using scrypt

        :param str password: A password in plain text
        """
        # Validate inputs
        validate_input('password', password, str)

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Converts input to a hash and compares it against an existing hash

        :param str password: A password in plain text
        """
        # Validate inputs
        validate_input('password', password, str)

        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    """Course database model
    """
    __tablename__ = 'courses'

    course_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    course_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True)
    course_code: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True)
    course_desc: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256), index=True)

    associations: so.Mapped[List['Association']] = so.relationship(
        back_populates='course')

    def __repr__(self):
        return f'<Course {self.course_name}>'


class Role(db.Model):
    """Role database model
    """
    __tablename__ = 'roles'

    role_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    role_name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True)

    associations: so.Mapped[List['Association']] = so.relationship(
        back_populates='role')

    def __repr__(self):
        return f'<Role {self.role_name}>'


class Association(db.Model):
    """Association database mode
    Note - This is a ternary association table
    """
    __tablename__ = 'associations'

    course_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Course.course_id), primary_key=True)
    role_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Role.role_id), primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.user_id), primary_key=True)

    course: so.Mapped['Course'] = so.relationship(
        back_populates='associations')
    role: so.Mapped['Role'] = so.relationship(back_populates='associations')
    user: so.Mapped['User'] = so.relationship(back_populates='associations')

    def __repr__(self):
        return f'{self.course_id} {self.role_id} {self.user_id}'
