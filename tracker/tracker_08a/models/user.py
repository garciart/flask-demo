"""Class for the User database model using SQLAlchemy ORM Declarative Mapping.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from werkzeug.security import (generate_password_hash, check_password_hash)
from . import db
from .. import validate_input


class User(db.Model):
    """User database model
    """
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    # Using RFC 5321, 5322, and 3696 for username and email lengths
    user_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    user_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    def __repr__(self):
        """Return a representation of the data in JSON format

        :return: The data in JSON format
        :rtype: str
        """
        return (
            f'{{"user_id": "{self.user_id}",'
            f'"user_name": "{self.user_name}",'
            f'"user_email": "{self.user_email}"}}'
        )

    def set_password(self, password: str) -> None:
        """Hashes a password using scrypt

        :param str password: A password in plain text

        :returns: None
        :rtype: None
        """
        # Validate inputs
        validate_input('password', password, str)

        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Converts input to a hash and compares it against an existing hash

        :param str password: A password in plain text

        :returns: True if the password hashes match
        :rtype: bool
        """
        # Validate inputs
        validate_input('password', password, str)

        return check_password_hash(self.password_hash, password)
