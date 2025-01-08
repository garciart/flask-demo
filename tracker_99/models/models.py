"""Classes for the database models using SQLAlchemy ORM Declarative Mapping.
"""

import re
from typing import List, Union, Optional

from flask_login import UserMixin
from sqlalchemy import String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from tracker_99 import login_manager
from tracker_99.app_utils import validate_input
from tracker_99.models import db

CASCADE_ARG = 'all, delete-orphan'


class Member(UserMixin, db.Model):
    """Member database model"""

    __tablename__ = 'member'

    member_id: Mapped[int] = mapped_column(primary_key=True)
    # Using RFC 5321, 5322, and 3696 for member name and email lengths
    member_name: Mapped[str] = mapped_column(String(64), nullable=False)
    member_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    member_is_admin: Mapped[bool] = mapped_column(nullable=False)

    associations: Mapped[List['Association']] = relationship(
        'Association', back_populates='member', cascade=CASCADE_ARG
    )

    def __init__(
        self,
        member_name: str,
        member_email: str,
        password: Union[str, None] = None,
        member_is_admin: bool = False,
    ) -> None:
        """Initialization with validation to ensure valid types and values.

        :param str member_name: The username of the member
        :param str member_email: The email address of the member
        :param str password: A password for the member in plain text, defaults to None,
            which prevents the database from accepting the member
            unless the password is set using `set_password()`
        :param bool member_is_admin: The email address of the member
        """
        # Validate inputs
        validate_input('member_name', member_name, str)
        validate_input('member_email', member_email, str)
        validate_input('password', password, Union[str, None])
        validate_input('member_is_admin', member_is_admin, Union[bool, None])

        # Validate that member_name:
        # - Starts with a letter
        # - Contains only letters, numbers, underscores, and periods
        # - Must be at least 4 characters long
        name_regex = r'^[A-Za-z][A-Za-z0-9._-]{3,}$'
        if not re.fullmatch(name_regex, member_name):
            raise ValueError("Invalid member name.")

        # Validate that member_email matches the email pattern
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$'
        if not re.fullmatch(email_regex, member_email):
            raise ValueError("Invalid member email.")

        # Set the member_name and member_email
        self.member_name = member_name
        self.member_email = member_email

        if password is not None:
            self.validate_password(password)
            # Initialize password hash
            self.set_password(password)

        self.member_is_admin = member_is_admin

    def get_id(self) -> int:
        """Overrides UserMixin get_id so you can use member_id instead of id.

        :returns: The member ID
        :rtype: int
        """
        return self.member_id

    def set_password(self, password: str) -> None:
        """Hashes a password using scrypt

        :param str password: A password in plain text

        :returns: None
        :rtype: None
        """
        # Validate inputs
        validate_input('password', password, str)
        self.validate_password(password)

        self.password_hash = generate_password_hash(password)

    @staticmethod
    def validate_password(password: str) -> None:
        """Validate password requirements:

        - A minimum of eight characters
        - A maximum of fifteen characters
        - At least one uppercase letter, one lowercase letter and one number

        :param str password: The password to validate

        :returns: None
        :rtype: None
        """
        validate_input('password', password, str)

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,15}$'
        if not re.fullmatch(password_regex, password):
            raise ValueError("Invalid password.")

    def verify_password(self, password_to_verify: str) -> bool:
        """Converts input to a hash and compares it against an existing hash

        :param str password_to_verify: A provided password in plain text

        :returns: True if the password hashes match
        :rtype: bool
        """
        # Validate inputs
        validate_input('password_to_verify', password_to_verify, str)

        return check_password_hash(self.password_hash, password_to_verify)

    def to_dict(self) -> dict:
        """Return the object as a dictionary for conversion to JSON

        :return: The keys and values of the object
        :rtype: dict
        """
        return {
            'member_id': self.member_id,
            'member_name': self.member_name,
            'member_email': self.member_email,
            'member_is_admin': self.member_is_admin,
        }


@login_manager.user_loader
def load_user(member_id: int) -> Member:
    """Get user information from the database.

    :param int member_id: The member ID to search for

    :returns: A user object
    :rtype: app.models.User
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    return db.session.get(Member, member_id)


class Course(db.Model):
    """Course database model"""

    __tablename__ = 'courses'

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(String(64), nullable=False)
    course_code: Mapped[str] = mapped_column(String(64), nullable=False)
    course_group: Mapped[Optional[str]] = mapped_column(String(64))
    course_desc: Mapped[Optional[str]] = mapped_column(String(256))

    # Courses can have the same name or code, but not both
    __table_args__ = (
        UniqueConstraint('course_name', 'course_code', name='uq_course_name_code'),
    )

    associations: Mapped[List['Association']] = relationship(
        'Association', back_populates='course', cascade=CASCADE_ARG
    )

    def to_dict(self):
        """Return the object as a dictionary for conversion to JSON

        :return: The keys and values of the object
        :rtype: dict
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'course_desc': self.course_desc,
        }


class Role(db.Model):
    """Role database model"""

    __tablename__ = 'roles'

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(64), unique=True)
    role_privilege: Mapped[int] = mapped_column(unique=True)

    associations: Mapped[List['Association']] = relationship(
        'Association', back_populates='role', cascade=CASCADE_ARG
    )

    def to_dict(self):
        """Return the object as a dictionary for conversion to JSON

        :return: The keys and values of the object
        :rtype: dict
        """
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_privilege': self.role_privilege,
        }


class Association(db.Model):
    """Association database model
    Note: This is a three-way relationship
    """

    __tablename__ = 'associations'

    course_id: Mapped[int] = mapped_column(
        ForeignKey(Course.course_id), primary_key=True, nullable=False
    )
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.role_id), primary_key=True, nullable=False)
    member_id: Mapped[int] = mapped_column(
        ForeignKey(Member.member_id), primary_key=True, nullable=False
    )

    course: Mapped['Course'] = relationship(back_populates='associations')
    role: Mapped['Role'] = relationship(back_populates='associations')
    member: Mapped['Member'] = relationship(back_populates='associations')

    def has_access_to_course(self, course: 'Course', role_name: str) -> bool:
        """Check if the member has access to the course with a specific role."""
        for association in self.associations:
            if association.course == course and association.role.role_name == role_name:
                return True
        return False

    def to_dict(self):
        """Return the object as a dictionary for conversion to JSON

        :return: The keys and values of the object
        :rtype: dict
        """
        return {'course_id': self.course_id, 'role_id': self.role_id, 'member_id': self.member_id}
