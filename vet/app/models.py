"""Database models
"""
from typing import Optional, List

from flask_login import UserMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .app_utils import validate_input
from . import db, login


# - 'python -B -m flask db init' to create the migration repository
# - 'python -B -m flask db migrate -m '<message>'' to generate a migration script
#       after making changes to the schema
# - 'python -B -m flask db upgrade' to apply changes
# - 'python -B -m flask db downgrade' to undo migration


class Course(db.Model):
    """Course database model
    """
    __tablename__ = 'courses'

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(
        String(64), index=True, unique=True)
    course_code: Mapped[str] = mapped_column(
        String(64), unique=True)
    course_group: Mapped[Optional[str]] = mapped_column(
        String(64))
    course_desc: Mapped[Optional[str]] = mapped_column(
        String(256))

    associations: Mapped[List['Association']] = relationship(
        back_populates='course', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'course_desc': self.course_desc
        }


class Role(db.Model):
    """Role database model
    """
    __tablename__ = 'roles'

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(
        String(64), index=True, unique=True)
    role_privilege: Mapped[int] = mapped_column(unique=True)

    associations: Mapped[List['Association']] = relationship(
        back_populates='role', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_privilege': self.role_privilege
        }


class User(UserMixin, db.Model):
    """User database model
    """
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    user_email: Mapped[Optional[str]] = mapped_column(String(128), unique=True)
    is_admin: Mapped[bool] = mapped_column(default=True)
    password_hash: Mapped[str] = mapped_column(String(256))

    associations: Mapped[List['Association']] = relationship(
        back_populates='user', cascade='all, delete-orphan')

    def to_dict(self) -> dict:
        """Return the object as a dictionary for conversion to JSON

        :return: The keys and values of the object
        :rtype: dict
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'user_email': self.user_email,
            'is_admin': self.is_admin
        }

    def get_id(self):
        # type: () -> int
        """Overrides UserMixin get_id, so you can use user_id instead of id.

        :returns: The user id
        :rtype: int
        """
        return self.user_id

    def set_password(self, password):
        # type: (str) -> None
        """Hashes a password using scrypt

        :param str password: A password in plain text

        :returns: None
        :rtype: None
        """
        # Validate inputs
        validate_input('password', password, str)

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # type: (str) -> bool
        """Converts input to a hash and compares it against an existing hash

        :param str password: A password in plain text

        :returns: True if the password hashes match
        :rtype: bool
        """
        # Validate inputs
        validate_input('password', password, str)

        return check_password_hash(self.password_hash, password)


class Association(db.Model):
    """Association database model
    Note: This is a three-way relationship
    """
    __tablename__ = 'associations'

    course_id: Mapped[int] = mapped_column(
        ForeignKey(Course.course_id), primary_key=True, nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey(Role.role_id), primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.user_id), primary_key=True, nullable=False)

    course: Mapped['Course'] = relationship(
        back_populates='associations')
    role: Mapped['Role'] = relationship(back_populates='associations')
    user: Mapped['User'] = relationship(back_populates='associations')

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'role_id': self.role_id,
            'user_id': self.user_id
        }


@login.user_loader
def load_user(user_id):
    # type: (int) -> User
    """Get user information from the database.

    :param int user_id: The user ID to search for

    :returns: A user object
    :rtype: app.models.User
    """
    # Validate inputs
    validate_input('user_id', user_id, int)

    return db.session.get(User, user_id)
