"""Role administration routing manager.

NOTE - Imports within functions are to prevent a known
circular import problem in Flask.

Test: http://127.0.0.1:5000/add_role
"""
# Flake8 F401: imports are used for type hints
from flask import (Response,  # noqa: F401 pylint:disable=unused-import
                   abort, flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required
from app import db
from app.admin import admin_bp
from app.admin.admin_forms import (
    AddRoleForm, DeleteRoleForm, EditRoleForm)
from app.models import Role

INDEX_PAGE = 'main.index'


@admin_bp.route('/add_role', methods=['GET', 'POST'])
@login_required
def add_role():
    # type: () -> str | Response
    """Use form input to add a role to the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can add roles
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    form = AddRoleForm()

    if form.validate_on_submit():
        _role = Role(role_name=form.role_name.data)
        db.session.add(_role)
        db.session.commit()
        flash('Role added.')
        return redirect(url_for(INDEX_PAGE))
    else:
        return render_template('admin/add_role.html', title='Add Role',
                               form=form)


@admin_bp.route('/edit_role/<int:role_id>', methods=['GET', 'POST'])
@login_required
def edit_role(role_id):
    # type: (int) -> str | Response
    """Use form input to update a role in the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can update roles
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _role = Role.query.get_or_404(role_id)
    form = EditRoleForm(_role.role_name)

    if form.validate_on_submit():
        _role.role_name = form.role_name.data
        db.session.commit()
        flash('Role updated.')
        return redirect(url_for('main.roles'))
    elif request.method == 'GET':
        form.role_name.data = _role.role_name
        return render_template('admin/edit_role.html', title='Edit Role',
                               form=form)
    else:
        abort(500)


@admin_bp.route('/delete_role/<int:role_id>', methods=['GET', 'POST'])
@login_required
def delete_role(role_id):
    # type: (int) -> str | Response
    """Use form input to delete a role from the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can delete roles
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _role = Role.query.get_or_404(role_id)
    form = DeleteRoleForm()

    if form.validate_on_submit():
        if form.submit.data:
            db.session.delete(_role)
            db.session.commit()
            flash('Role deleted.')
        return redirect(url_for('main.roles'))
    elif request.method == 'GET':
        _role_name = _role.role_name
        return render_template('admin/delete_role.html', title='Delete Role',
                               role_name=_role_name, form=form)
    else:
        abort(500)
