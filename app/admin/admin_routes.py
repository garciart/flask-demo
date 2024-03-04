"""Administration routing manager.

NOTE - Imports within functions are to prevent a known
circular import problem in Flask.

Test: http://127.0.0.1:5000/add_user
"""
# Flake8 F401: imports are used for type hints
from flask import (Response,  # noqa: F401 pylint:disable=unused-import
                   abort, flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required
from app import db
from app.admin import admin_bp
from app.admin.admin_forms import (
    AddUserForm, DeleteUserForm, EditUserForm,
    AddRoleForm, DeleteRoleForm, EditRoleForm,)
from app.models import User, Role

INDEX_PAGE = 'main.index'


@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    # type: () -> str | Response
    """Use form input to add a user to the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can add users
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    form = AddUserForm()

    if form.validate_on_submit():
        _user = User(username=form.username.data,
                     user_email=form.user_email.data,
                     is_admin=form.is_admin.data)
        _user.set_password(form.password.data)
        db.session.add(_user)
        db.session.commit()
        flash('User added.')
        return redirect(url_for(INDEX_PAGE))
    else:
        return render_template('admin/add_user.html', title='Add User',
                               form=form)


@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # type: (int) -> str | Response
    """Use form input to update a user in the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can update users
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _user = User.query.get_or_404(user_id)
    form = EditUserForm(_user.username)

    if form.validate_on_submit():
        _user.username = form.username.data
        _user.user_email = form.user_email.data
        _user.is_admin = form.is_admin.data
        if form.password.data.strip() != '':
            _user.set_password(form.password.data)
        db.session.commit()
        flash('User updated.')
        return redirect(url_for('main.users'))
    elif request.method == 'GET':
        form.username.data = _user.username
        form.user_email.data = _user.user_email
        form.is_admin.data = _user.is_admin
        return render_template('admin/edit_user.html', title='Edit User',
                               form=form)
    else:
        abort(500)


@admin_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    # type: (int) -> str | Response
    """Use form input to delete a user from the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can delete users
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _user = User.query.get_or_404(user_id)
    form = DeleteUserForm()

    if form.validate_on_submit():
        if form.submit.data:
            db.session.delete(_user)
            db.session.commit()
            flash('User deleted.')
        return redirect(url_for('main.users'))
    elif request.method == 'GET':
        _username = _user.username
        return render_template('admin/delete_user.html', title='Delete User',
                               username=_username, form=form)
    else:
        abort(500)


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
