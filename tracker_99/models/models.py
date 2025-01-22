"""Classes for the database models using SQLAlchemy ORM Declarative Mapping.
"""

import os
import re
from typing import List, Union, Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flask_login import UserMixin
from sqlalchemy import String, UniqueConstraint, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from werkzeug.security import generate_password_hash, check_password_hash

from tracker_99 import login_manager, constants as c
from tracker_99.app_utils import validate_input
from tracker_99.models import db

CASCADE_ARG = 'all, delete-orphan'


class Member(UserMixin, db.Model):
    """Member database model"""

    __tablename__ = 'members'

    member_id: Mapped[int] = mapped_column(primary_key=True)
    # Using RFC 5321, 5322, and 3696 for member name and email lengths
    member_name: Mapped[str] = mapped_column(String(64), nullable=False)
    member_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False)

    associations: Mapped[List['Association']] = relationship(
        'Association', back_populates='member', cascade=CASCADE_ARG
    )

    def __init__(
        self,
        member_name: str,
        member_email: str,
        password: Union[str, None] = None,
        is_admin: bool = False,
    ) -> None:
        """Initialization with validation to ensure valid types and values.

        :param str member_name: The name of the member
        :param str member_email: The email address of the member
        :param str password: A password for the member in plain text, defaults to None,
            which prevents the database from accepting the member
            unless the password is set using `set_password()`
        :param bool is_admin: True if the user is an administrator
        """
        # Validate inputs
        validate_input('member_name', member_name, str)
        validate_input('member_email', member_email, str)
        validate_input('password', password, Union[str, None])
        validate_input('is_admin', is_admin, bool)

        if not re.fullmatch(c.NAME_REGEX, member_name):
            raise ValueError('Invalid member name.')

        # Validate that member_email matches the email pattern
        if not re.fullmatch(c.EMAIL_REGEX, member_email):
            raise ValueError('Invalid member email.')

        # Set the member_name and member_email
        self.member_name = member_name
        self.member_email = member_email

        if password is not None:
            self.validate_password(password)
            # Initialize password hash
            self.set_password(password)

        self.is_admin = is_admin

    def get_id(self) -> int:
        """Overrides UserMixin get_id, so you can use member_id instead of id.

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

        if not re.fullmatch(c.PASSWORD_REGEX, password):
            raise ValueError('Invalid password.')

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
            'is_admin': self.is_admin,
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
    course_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    course_desc: Mapped[Optional[str]] = mapped_column(String(256))

    # Courses can have the same name or code, but not both
    __table_args__ = (UniqueConstraint('course_name', 'course_code', name='uq_course_name_code'),)

    associations: Mapped[List['Association']] = relationship(
        'Association', back_populates='course', cascade=CASCADE_ARG
    )

    # pylint: disable-next=[too-many-arguments, too-many-positional-arguments]
    def __init__(
        self,
        course_name: str,
        course_code: str,
        course_group: Union[str, None] = None,
        course_key: Union[str, None] = None,
        course_desc: Union[str, None] = None,
    ) -> None:
        """Initialization with validation to ensure valid types and values.

        :param str course_name: The long name of the course
        :param str course_code: The short name or code of the course (SDEV 101)
        :param str course_group: The group the course belongs to (SDEV, etc.)
        :param str course_key: A password for the course in plain text, defaults to None
        :param str course_desc: A description of the course
        """
        # Validate inputs
        validate_input('course_name', course_name, str)
        validate_input('course_code', course_code, str)
        validate_input('course_group', course_group, Union[str, None], allow_empty=True)
        validate_input('course_key', course_key, Union[str, None], allow_empty=True)
        validate_input('course_desc', course_desc, Union[str, None], allow_empty=True)

        if not re.fullmatch(c.TEXT_REGEX, course_name):
            raise ValueError('Invalid course name.')

        if not re.fullmatch(c.TEXT_REGEX, course_code):
            raise ValueError('Invalid course code.')

        # Set the member_name and member_email
        self.course_name = course_name
        self.course_code = course_code

        if course_group is not None and course_group.strip() != '':
            if not re.fullmatch(c.TEXT_REGEX, course_group):
                raise ValueError('Invalid course group.')
            self.course_group = course_group

        if course_desc is not None and course_desc.strip() != '':
            self.course_desc = course_desc

        if course_key is not None and course_key.strip() != '':
            self.validate_password(course_key)
            # Initialize password hash
            self.set_key(course_key)

    def set_key(self, plain_text_key: str) -> None:
        """Encrypt a key using AES-GCM.

        :param str plain_text_key: The text to encrypt

        :returns: None
        :rtype: None
        """
        validate_input('plain_text', plain_text_key, str)

        # Get the 256-bit key (32 bytes) from the environment and convert it to a byte string
        # The environment variable KEY_32 should contain a 32-byte (256-bit) key.
        _env_key_32 = os.environ.get('KEY_32', 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEF')
        _key = str.encode(_env_key_32, encoding='utf-8')
        assert len(_key) == 32, "Key must be 32 bytes to use AES-256 encryption."

        # Generate a random initialization vector (IV) / nonce
        # GCM standard is 96 bits (12 bytes);
        # longer IV's do not improve security and may hurt performance
        _iv = os.urandom(12)

        # Instantiate a cipher object that defines how encryption will be performed
        _cipher = Cipher(algorithms.AES(_key), modes.GCM(_iv), backend=default_backend())

        # Convert the plain text to a byte string and encrypt
        _byte_str = str.encode(plain_text_key, encoding='utf-8')
        _encryptor = _cipher.encryptor()
        _ciphertext = _encryptor.update(_byte_str) + _encryptor.finalize()

        # Combine the IV, cyphertext, and tag into an encrypted package
        _encrypted_data = _iv + _ciphertext + _encryptor.tag

        self.course_key = _encrypted_data

    @staticmethod
    def decrypt_text(encrypted_data: bytes) -> str:
        """Decrypt AES-GCM encrypted data.

        :param bytes encrypted_data: The initialization vector (IV) / nonce, ciphertext, \
            and tag to decrypt

        :returns: The decrypted text
        :rtype: str
        """
        validate_input('encrypted_data', encrypted_data, bytes)

        # Get the 256-bit key (32 bytes) from the environment and convert it to a byte string
        # The environment variable KEY_32 should contain a 32-byte (256-bit) key.
        _env_key_32 = os.environ.get('KEY_32', 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEF')
        _key = str.encode(_env_key_32, encoding='utf-8')
        assert len(_key) == 32, "Key must be 32 bytes to use AES-256 encryption."

        # Extract the IV, tag, and ciphertext from the encrypted data
        # The first 12 bytes are the IV
        _iv = encrypted_data[:12]

        # The last 16 bytes are the tag
        _tag = encrypted_data[-16:]

        # The remainder is the ciphertext
        _ciphertext = encrypted_data[12:-16]

        # Instantiate a cipher object that defines how decryption will be performed
        _cipher = Cipher(algorithms.AES(_key), modes.GCM(_iv, _tag), backend=default_backend())

        # Decrypt the ciphertext in the encrypted data
        _decryptor = _cipher.decryptor()
        _decrypted_text = (_decryptor.update(_ciphertext) + _decryptor.finalize()).decode(
            encoding='utf-8'
        )

        return _decrypted_text

    def to_dict(self):
        """Return the object as a dictionary for conversion to JSON

        :return: The keys and values of the object
        :rtype: dict
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'course_group': self.course_group,
            'course_key': self.course_key,
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

    @validates('role_id')
    def validate_role_id(self, _, value: str) -> str:
        """Prevent members from assigning role_id 1.

        Students in the 'Unassigned' role will be deleted from the Associations table to save space

        :param str _: The key, i.e., role_id. Not used
        :param str value: The role id value to check

        :raises ValueError: If the role name is not 'Unassigned'

        :return: The value if no exception was raised
        :rtype: str
        """
        if int(value) == 1 and str(self.role_name).lower() != 'unassigned':
            raise ValueError('Role ID 1 is reserved for unassigned members and cannot be used')
        return value

    @validates('role_privilege')
    def validate_role_privilege(self, _, value: str) -> str:
        """Ensure that role privilege is between 1 and 99 if the role is not 'Unassigned'.

        :param str _: The key, i.e., role_privilege. Not used
        :param str value: The role privilege value to check

        :raises ValueError: If the value is not between 1 and 99

        :return: The value if no exception was raised
        :rtype: str
        """
        if str(self.role_name).lower() != 'unassigned':
            if int(value) < 1 or int(value) > 99:
                raise ValueError(
                    'role_privilege must be between 1 and 99.'
                    'Higher privileges are reserved for future use.'
                )
        return value

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

    # Members may only be assigned to a course once,
    # so they cannot have multiple roles in the course
    __table_args__ = (UniqueConstraint('course_id', 'member_id', name='uq_course_member'),)

    course: Mapped['Course'] = relationship(back_populates='associations')
    role: Mapped['Role'] = relationship(back_populates='associations')
    member: Mapped['Member'] = relationship(back_populates='associations')

    def to_dict(self):
        """Return the object as a dictionary for conversion to JSON

        :return: The keys and values of the object
        :rtype: dict
        """
        return {'course_id': self.course_id, 'role_id': self.role_id, 'member_id': self.member_id}
