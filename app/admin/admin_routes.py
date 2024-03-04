"""Administration routing manager.

NOTE - Imports within functions are to prevent a known
circular import problem in Flask.

Test: http://127.0.0.1:5000/add_user
"""
# Flake8 F401: imports are used for type hints
from flask import (flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required
from app.admin import admin_bp
from app.admin.admin_forms import (
    AddUserForm, AddRoleForm, EditUserForm, DeleteUserForm)
from app import db
from app.models import User, Role

INDEX_PAGE = 'main.index'


@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
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
    return render_template('admin/add_user.html', title='Add User', form=form)


@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # Only administrators can edit users
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


@admin_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
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


@admin_bp.route('/add_role', methods=['GET', 'POST'])
@login_required
def add_role():
    # Only administrators can add roles
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))
    form = AddRoleForm()
    if form.validate_on_submit():
        _role = Role(role_name=form.role_name.data)
        db.session.add(_role)
        db.session.commit()
        flash('Role added.')
        return redirect(url_for('main.roles'))
    return render_template('admin/add_role.html', title='Add Role', form=form)
