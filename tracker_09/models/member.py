"""Class for the Member database model using SQLAlchemy ORM Declarative Mapping.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from werkzeug.security import (generate_password_hash, check_password_hash)

from tracker_09.app_utils import validate_input
from tracker_09.models import db


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
