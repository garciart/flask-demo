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
    AddRoleForm, DeleteRoleForm, EditRoleForm,
    AddCourseForm, DeleteCourseForm, EditCourseForm)
from app.models import User, Role, Course, Association
from app.app_utils import validate_input

INDEX_PAGE = 'main.index'
USERS_PAGE = 'main.users'
ROLES_PAGE = 'main.roles'
NOT_AUTH_MSG1 = 'You must be an administrator to perform this action.'
NOT_AUTH_MSG2 = (
    'You must be an administrator or owner to perform this action.')
SUICIDE_MSG = 'You cannot delete yourself!'


@admin_bp.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    # type: () -> str | Response
    """Use form input to add a course to the database.

    Note - Anyone may add a course

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    _form = AddCourseForm()

    if _form.validate_on_submit():
        _course = Course(course_name=_form.course_name.data,
                         course_code=_form.course_code.data,
                         course_group=_form.course_group.data,
                         course_desc=_form.course_desc.data)
        db.session.add(_course)
        db.session.commit()

        # Get row_id of the new course
        _new_id = _course.course_id

        # Add the course and owner to the association table
        _user_id = int(current_user.get_id())
        _assoc = Association(course_id=_new_id, role_id=2, user_id=_user_id)

        db.session.add(_assoc)
        db.session.commit()
        flash('Course added.')
        return redirect(url_for(INDEX_PAGE))
    else:
        return render_template('admin/add_course.html', title='Add Course',
                               form=_form)


@admin_bp.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    # type: (int) -> str | Response
    """Use form input to update a course in the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    _course = Course.query.get_or_404(course_id)

    _assoc = Association.query.filter(
        Association.course_id == _course.course_id).all()

    print('_assoc', _assoc, type(_assoc))

    # Only owners and administrators can edit courses
    if not current_user.is_admin:
        _user_id = int(current_user.get_id())
        for _a in _assoc:
            if _a.user_id != _user_id and _a.role_id > 2:
                flash(NOT_AUTH_MSG2)
                return redirect(url_for(INDEX_PAGE))

    _form = EditCourseForm(_course.course_name)

    if _form.validate_on_submit():
        _course.course_name = _form.course_name.data
        _course.course_code = _form.course_code.data
        _course.course_group = _form.course_group.data
        _course.course_desc = _form.course_desc.data
        db.session.commit()
        flash('Course updated.')
        return redirect(url_for('main.courses'))
    elif request.method == 'GET':
        _form.course_name.data = _course.course_name
        _form.course_code.data = _course.course_code
        _form.course_group.data = _course.course_group
        _form.course_desc.data = _course.course_desc
        return render_template('admin/edit_course.html', title='Edit Course',
                               form=_form)
    else:
        abort(500)


@admin_bp.route('/delete_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def delete_course(course_id):
    # type: (int) -> str | Response
    """Use form input to delete a course from the database.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    _course = Course.query.get_or_404(course_id)

    _assoc = Association.query.filter(
        Association.course_id == _course.course_id).all()

    # Only owners and administrators can delete courses
    if not current_user.is_admin:
        _user_id = int(current_user.get_id())
        for _a in _assoc:
            if _a.user_id != _user_id and _a.role_id > 2:
                flash(NOT_AUTH_MSG2)
                return redirect(url_for(INDEX_PAGE))

    _form = DeleteCourseForm()

    if _form.validate_on_submit():
        if _form.submit.data:
            for _a in _assoc:
                db.session.delete(_a)
            db.session.delete(_course)
            db.session.commit()
            flash('Course deleted.')
        return redirect(url_for('main.courses'))
    elif request.method == 'GET':
        _course_name = _course.course_name
        return render_template('admin/delete_course.html',
                               title='Delete Course', course_name=_course_name,
                               form=_form)
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
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    _form = AddRoleForm()

    if _form.validate_on_submit():
        _role = Role(role_name=_form.role_name.data)
        db.session.add(_role)
        db.session.commit()
        flash('Role added.')
        return redirect(url_for(ROLES_PAGE))
    else:
        return render_template('admin/add_role.html', title='Add Role',
                               form=_form)


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
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    # Validate inputs
    validate_input('role_id', role_id, int)

    _role = Role.query.get_or_404(role_id)
    _form = EditRoleForm(_role.role_name)

    if _form.validate_on_submit():
        _role.role_name = _form.role_name.data
        db.session.commit()
        flash('Role updated.')
        return redirect(url_for(ROLES_PAGE))
    elif request.method == 'GET':
        _form.role_name.data = _role.role_name
        return render_template('admin/edit_role.html', title='Edit Role',
                               form=_form)
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
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    # Validate inputs
    validate_input('role_id', role_id, int)

    _role = Role.query.get_or_404(role_id)
    _form = DeleteRoleForm()

    if _form.validate_on_submit():
        if _form.submit.data:
            db.session.delete(_role)
            db.session.commit()
            flash('Role deleted.')
        return redirect(url_for(ROLES_PAGE))
    elif request.method == 'GET':
        _role_name = _role.role_name
        return render_template('admin/delete_role.html', title='Delete Role',
                               role_name=_role_name, form=_form)
    else:
        abort(500)


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
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    _form = AddUserForm()

    if _form.validate_on_submit():
        _user = User(username=_form.username.data,
                     user_email=_form.user_email.data,
                     is_admin=_form.is_admin.data)
        _user.set_password(_form.password.data)
        db.session.add(_user)
        db.session.commit()
        flash('User added.')
        return redirect(url_for(USERS_PAGE))
    else:
        return render_template('admin/add_user.html', title='Add User',
                               form=_form)


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
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    # Validate inputs
    validate_input('user_id', user_id, int)

    _user = User.query.get_or_404(user_id)
    _form = EditUserForm(_user.username)

    if _form.validate_on_submit():
        _user.username = _form.username.data
        _user.user_email = _form.user_email.data
        _user.is_admin = _form.is_admin.data
        if _form.password.data.strip() != '':
            _user.set_password(_form.password.data)
        db.session.commit()
        flash('User updated.')
        return redirect(url_for(USERS_PAGE))
    elif request.method == 'GET':
        _form.username.data = _user.username
        _form.user_email.data = _user.user_email
        _form.is_admin.data = _user.is_admin
        return render_template('admin/edit_user.html', title='Edit User',
                               form=_form)
    else:
        abort(500)


@admin_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # type: () -> str | Response
    """Allow users to change their emails and passwords.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    pass


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
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    if current_user.get_id() == user_id:
        flash(SUICIDE_MSG)
        return redirect(url_for(INDEX_PAGE))

    # Validate inputs
    validate_input('user_id', user_id, int)

    _user = User.query.get_or_404(user_id)
    _assoc = Association.query.filter(
        Association.user_id == _user.user_id).all()

    _form = DeleteUserForm()

    if _form.validate_on_submit():
        if _form.submit.data:
            for _a in _assoc:
                db.session.delete(_a)
            db.session.delete(_user)
            db.session.commit()
            flash('User deleted.')
        return redirect(url_for(USERS_PAGE))
    elif request.method == 'GET':
        _username = _user.username
        return render_template('admin/delete_user.html', title='Delete User',
                               username=_username, form=_form)
    else:
        abort(500)
