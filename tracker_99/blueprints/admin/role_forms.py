"""Role forms manager
"""

from flask_wtf import FlaskForm
from sqlalchemy import func, select
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Length,
    NumberRange,
    Regexp,
)

from tracker_99 import db, constants as c
from tracker_99.models.models import Role


class AddRoleForm(FlaskForm):
    """Parameters for the Add Role form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    role_name = StringField(
        'Role',
        validators=[
            DataRequired(),
            Length(max=64),
            Regexp(c.TEXT_REGEX, message=c.INVALID_TEXT_MSG),
        ],
    )
    role_privilege = IntegerField(
        'Privilege Level', validators=[DataRequired(), NumberRange(min=1, max=3)]
    )
    submit = SubmitField('Add Role')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_role_name(self, role_name: StringField) -> None:
        """Check if a role name already exists in the database.

        :param StringField role_name: The role name to check

        :raises ValidationError: If the submitted role name already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM roles WHERE LOWER(roles.role_name) = LOWER("ChAiR");
        _role = db.session.scalar(
            select(Role).where(func.lower(Role.role_name) == func.lower(role_name.data))
        )
        if _role is not None:
            raise ValidationError('Role name already exists.')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_role_privilege(self, role_privilege: IntegerField) -> None:
        """Check if a privilege level already exists in the database.

        :param IntegerField role_privilege: The privilege level to check

        :raises ValidationError: If the submitted privilege level already exists

        :returns: None
        :rtype: None
        """
        # SELECT * FROM roles WHERE roles.role_privilege = 10;
        _role = db.session.scalar(select(Role).where(Role.role_privilege == role_privilege.data))
        if _role is not None:
            raise ValidationError('Privilege level already assigned.')


class EditRoleForm(FlaskForm):
    """Parameters for the Edit Role form template.

    :param FlaskForm FlaskForm: Base class for creating WTForms
    """

    role_name = StringField(
        'Role name', validators=[DataRequired(), Regexp(c.TEXT_REGEX, message=c.INVALID_TEXT_MSG)]
    )
    role_privilege = IntegerField(
        'Privilege Level', validators=[DataRequired(), NumberRange(min=1, max=99)]
    )
    submit = SubmitField('Update Role')

    def __init__(
            self, original_role_name: str, original_role_privilege: str, *args: any, **kwargs: any
    ) -> None:
        """Get the name and privilege of the role being edited.

        :param str original_role_name: The edited role's name
        :param int original_role_privilege: The edited role's privilege level

        :returns: None
        :rtype: None
        """
        super().__init__(*args, **kwargs)
        self.original_role_name = original_role_name
        self.original_role_privilege = original_role_privilege

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_role_name(self, role_name: StringField) -> None:
        """Check if a role name or already exists in the database.

        :param StringField role_name: The role name to check

        :raises ValidationError: If the submitted role name already exists

        :returns: None
        :rtype: None
        """
        if role_name.data != self.original_role_name:
            # SELECT * FROM roles WHERE LOWER(roles.role_name) = LOWER("ChAiR");
            _role = db.session.scalar(
                select(Role).where(func.lower(Role.role_name) == func.lower(role_name.data))
            )
            if _role is not None:
                raise ValidationError('Role name already exists.')

    # FIELD NAME VALIDATORS MUST USE validate_{field_name} PATTERN!
    def validate_role_privilege(self, role_privilege: IntegerField) -> None:
        """Check if a privilege level already exists in the database.

        :param IntegerField role_privilege: The privilege level to check

        :raises ValidationError: If the submitted privilege level already exists

        :returns: None
        :rtype: None
        """
        if role_privilege.data != self.original_role_privilege:
            # SELECT * FROM roles WHERE roles.role_privilege = 10;
            _role = db.session.scalar(
                select(Role).where(Role.role_privilege == role_privilege.data)
            )
            if _role is not None:
                raise ValidationError('Privilege level already assigned.')


class DeleteRoleForm(FlaskForm):
    """Parameters for the Delete Role form template.

    :param flask_wtf.FlaskForm: Base class for creating WTForms
    """

    submit = SubmitField('Delete Role')
