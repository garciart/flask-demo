"""Class for the Member database model using SQLAlchemy ORM Declarative Mapping.
"""
import re
from typing import Union

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from werkzeug.security import (generate_password_hash, check_password_hash)

from tracker_11.app_utils import validate_input
from tracker_11.models import db


class Member(db.Model):
    """Member database model
    """
    __tablename__ = 'member'

    member_id: Mapped[int] = mapped_column(primary_key=True)
    # Using RFC 5321, 5322, and 3696 for member name and email lengths
    member_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    member_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    def __repr__(self):
        """Return a representation of the data in JSON format

        :return: The data in JSON format
        :rtype: str
        """
        return (
            f'{{"member_id": "{self.member_id}",'
            f'"member_name": "{self.member_name}",'
            f'"member_email": "{self.member_email}"}}'
        )

    def __init__(self, member_name: str,
                 member_email: str, password: Union[str, None] = None) -> None:
        """Initialization with validation to ensure valid types and values.

        :param str member_name: The username of the member
        :param str member_email: The email address of the member
        :param str password: A password for the member, defaults to None,
            which prevents the database from accepting the member
            unless the password is set using `set_password()`
        """
        # Validate inputs
        validate_input('member_name', member_name, str)
        validate_input('member_email', member_email, str)
        validate_input('password', password, Union[str, None])

        # Validate that member_name:
        # - Starts with a letter
        # - Contains only letters, numbers, underscores, and periods
        # - Must Be at least 3 characters long
        name_regex = r'^[A-Za-z][A-Za-z0-9\.\_\-]{2,}$'
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

    def set_password(self, password: str) -> None:
        """Hashes a password using scrypt

        :param str password: A password in plain text

        :returns None: None
        """
        # Validate inputs
        validate_input('password', password, str)
        self.validate_password(password)

        self.password_hash = generate_password_hash(password)

    @staticmethod
    def validate_password(password: str) -> None:
        """Validate password requirements:

        - A minimum of eight characters
        - At least one uppercase letter, one lowercase letter and one number

        :param str password: The password to validate

        :returns None: None
        """
        validate_input('password', password, str)

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
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
