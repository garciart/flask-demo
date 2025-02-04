"""Role Administration Routing Manager.
"""

from typing import Union

from flask import Response, abort, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from tracker_99 import db, constants as c
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.admin import admin_bp
from tracker_99.blueprints.admin.role_forms import (
    AddRoleForm,
    EditRoleForm,
    DeleteRoleForm,
)
from tracker_99.models.models import Role, Association


# Allow `except Exception as e` so issues can percolate up, like ValueErrors from the model
# pylint: disable=broad-except

# Temporarily disabled here, in base.html, and roles.html
ROLES_DISABLED = True
ROLES_DISABLED_MSG = 'Adding, editing, or deleting roles is disabled at this time.'


@admin_bp.route('/admin/add_role', methods=['GET', 'POST'])
@login_required
def add_role() -> Union[str, Response]:
    """Use form input to add a role in the database.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    if ROLES_DISABLED:
        flash(ROLES_DISABLED_MSG)
        return redirect(url_for(c.INDEX_PAGE), code=306)

    # Only administrators can add roles
    if not current_user.is_admin:
        abort(403, c.NOT_AUTH_MSG)

    _page_title = 'Add Role'
    _page_description = 'Add Role'

    _form = AddRoleForm()

    if _form.validate_on_submit():
        try:
            # Instantiate a Role object
            _role = Role(
                role_name=_form.role_name.data,
                role_privilege=_form.role_privilege.data,
            )
            """
            INSERT INTO roles (role_name, role_privilege)
            VALUES ("Super", "99");
            """
            db.session.add(_role)
            db.session.commit()
            flash('Addition successful.')
            return redirect(url_for(c.ROLES_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Addition failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'add_role.html',
        page_title=_page_title,
        page_description=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/view_role/<int:role_id>', methods=['GET'])
@login_required
def view_role(role_id: int) -> Union[str, Response]:
    """View a role in the database.

    :param int role_id: The role to retrieve by ID

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('role_id', role_id, int)

    # Only administrators can view roles
    if not current_user.is_admin:
        abort(403, c.NOT_AUTH_MSG)

    _page_title = 'View Role'
    _page_description = 'View Role'

    # Verify role exists
    """
    SELECT * FROM roles WHERE role_id = 4;
    """
    _role = Role.query.get_or_404(role_id)

    return render_template(
        'view_role.html',
        page_title=_page_title,
        page_description=_page_description,
        role=_role,
    )


@admin_bp.route('/admin/edit_role/<int:role_id>', methods=['GET', 'POST'])
@login_required
def edit_role(role_id: int) -> Union[str, Response]:
    """Use form input to update a role in the database.

    :param int role_id: The role to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    if ROLES_DISABLED:
        flash(ROLES_DISABLED_MSG)
        return redirect(url_for(c.INDEX_PAGE), code=306)

    # Validate inputs
    validate_input('role_id', role_id, int)

    # Only administrators can edit roles
    if not current_user.is_admin:
        abort(403, c.NOT_AUTH_MSG)

    _page_title = 'Edit Role'
    _page_description = 'Edit Role'

    # Verify role exists
    """
    SELECT * FROM roles WHERE role_id = 4;
    """
    _role = Role.query.get_or_404(role_id)
    _form = EditRoleForm(_role.role_name, _role.role_privilege)

    # Pre-populate form with current role details
    if request.method == 'GET':
        _form.role_name.data = _role.role_name
        _form.role_privilege.data = _role.role_privilege

    if _form.validate_on_submit():
        try:
            _role.role_name = _form.role_name.data
            _role.role_privilege = _form.role_privilege.data
            """
            UPDATE roles
            SET role_name = "Superman",
                role_privilege = "999"
            WHERE role_id = 4;
            """
            # db.session.add(_role)
            db.session.commit()
            flash('Update successful.')
            return redirect(url_for(c.ROLES_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Update failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'edit_role.html',
        page_title=_page_title,
        page_description=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/delete_role/<int:role_id>', methods=['GET', 'POST'])
@login_required
def delete_role(role_id: int) -> Union[str, Response]:
    """Use form input to delete a role from the database.

    :param int role_id: The role to delete by ID

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    if ROLES_DISABLED:
        flash(ROLES_DISABLED_MSG)
        return redirect(url_for(c.INDEX_PAGE), code=306)

    # Validate inputs
    validate_input('role_id', role_id, int)

    # Only administrators can delete roles
    if not current_user.is_admin:
        abort(403, c.NOT_AUTH_MSG)

    _page_title = 'Delete Role'
    _page_description = 'Delete Role'

    # Verify role exists
    """
    SELECT * FROM ROLES WHERE role_id = 4;
    """
    _role = Role.query.get_or_404(role_id)

    _form = DeleteRoleForm()

    if _form.validate_on_submit():
        try:
            # Delete association data first
            """
            DELETE FROM associations WHERE role_id = 4;
            """
            Association.query.filter(Association.role_id == _role.role_id).delete()
            """
            DELETE FROM roles WHERE role_id = 4;
            """
            db.session.delete(_role)
            db.session.commit()
            flash('Delete successful.')
            return redirect(url_for(c.ROLES_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Deletion failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # And re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'delete_role.html',
        page_title=_page_title,
        page_description=_page_description,
        role=_role,
        form=_form,
    )
