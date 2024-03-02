"""Database models
"""
from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.app_utils import validate_input
from app import db, login

# - 'flask db init' to create migration repository
# - 'flask db migrate -m "<message>"' to generate a migration script
#       after making changes to the schema
# - 'flask db upgrade' to apply changes
# - 'flask db downgrade' to undo migration


class Course(db.Model):
    """Course database model
    """
    __tablename__ = 'courses'

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(
        String(64), index=True, )
    course_code: Mapped[str] = mapped_column(
        String(64), index=True)
    course_group: Mapped[Optional[str]] = mapped_column(
        String(64), index=True)
    course_desc: Mapped[Optional[str]] = mapped_column(
        String(256), index=True)

    associations: Mapped[List['Association']] = relationship(
        back_populates='course')

    def __repr__(self):
        return (f'{{"course_id": "{self.course_id}",'
                f'"course_name": "{self.course_name}",'
                f'"course_code": "{self.course_code}",'
                f'"course_desc": "{self.course_desc}"}}')


class Role(db.Model):
    """Role database model
    """
    __tablename__ = 'roles'

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(
        String(64), index=True, unique=True)

    associations: Mapped[List['Association']] = relationship(
        back_populates='role')

    def __repr__(self):
        return (f'{{"role_id": "{self.role_id}",'
                f'"role_name": "{self.role_name}"}}')


class User(UserMixin, db.Model):
    """User database model
    """
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(64), index=True, unique=True)
    user_email: Mapped[Optional[str]] = mapped_column(
        String(128), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(
        String(256))

    associations: Mapped[List['Association']] = relationship(
        back_populates='user')

    def __repr__(self):
        return (f'{{"user_id": "{self.user_id}",'
                f'"username": "{self.username}",'
                f'"user_group": "{self.user_group}",'
                f'"user_email": "{self.user_email}",'
                f'"password_hash": "{self.password_hash}"}}')

    def get_id(self):
        # type: () -> int
        """Overrides UserMixin get_id so you can use user_id instead of id.

        :returns: The user id
        :rtype: int
        """
        return self.user_id

    def set_password(self, password):
        # type: (str) -> None
        """Hashes a password using scrypt

        :param str password: A password in plain text

        :returns: None
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
        ForeignKey(Course.course_id), primary_key=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey(Role.role_id), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.user_id), primary_key=True)

    course: Mapped['Course'] = relationship(
        back_populates='associations')
    role: Mapped['Role'] = relationship(back_populates='associations')
    user: Mapped['User'] = relationship(back_populates='associations')

    def __repr__(self):
        return (f'{{"course_id": "{self.course_id}",'
                f'"role_id": "{self.role_id}",'
                f'"user_id": "{self.user_id}"}}')


@login.user_loader
def load_user(user_id):
    # type: (int) -> User
    """_summary_

    :param int user_id: The user ID to search for

    :returns: A user object
    :rtype: app.models.User
    """
    # Validate inputs
    validate_input('user_id', user_id, int)

    return db.session.get(User, user_id)
