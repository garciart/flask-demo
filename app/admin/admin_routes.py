"""Administration routing manager.

NOTE - Imports within functions prevent a known circular import problem
in Flask.

Test: http://127.0.0.1:5000/add_user
"""
# Flake8 F401: imports are used for type hints
from flask import (Response,  # noqa: F401 pylint:disable=unused-import
                   abort, flash, redirect, render_template, request, url_for)
from flask_login import (current_user, login_required)
from app import db
from app.admin import admin_bp
from app.admin.admin_forms import (SimpleForm,
    AddUserForm, DeleteUserForm, EditUserForm,
    AddRoleForm, DeleteRoleForm, EditRoleForm,
    AddCourseForm, DeleteCourseForm, EditCourseForm,
    UpdateProfileForm)
from app.models import (User, Role, Course, Association)
from app.app_utils import validate_input

INDEX_PAGE = 'main.index'
USERS_PAGE = 'main.users'
ROLES_PAGE = 'main.roles'
COURSES_PAGE = 'main.courses'
NOT_AUTH_MSG1 = 'You do not have permission to perform that action.'

SUICIDE_MSG = 'You cannot delete yourself!'


@admin_bp.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    # type: () -> str | Response
    """Use form input to add a course to the database.

    NOTE - Anyone may add a course

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

        # Add the course and chair to the association table
        _user_id = int(current_user.get_id())
        _assoc = Association(course_id=_new_id, role_id=1, user_id=_user_id)

        db.session.add(_assoc)
        db.session.commit()
        flash('Course added.')
        return redirect(url_for(INDEX_PAGE))
    
    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
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

    _user_id = int(current_user.get_id())

    _assoc = Association.query.filter(
        Association.course_id == _course.course_id,
        Association.user_id == _user_id,
        ((Association.role_id == '1') | (Association.role_id == '2'))).all()

    # Only administrators, chairs, and teachers can edit courses
    if not current_user.is_admin and len(_assoc) == 0:
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))
    
    _form = EditCourseForm(_course.course_name)

    if _form.validate_on_submit():
        _course.course_name = _form.course_name.data
        _course.course_code = _form.course_code.data
        _course.course_group = _form.course_group.data
        _course.course_desc = _form.course_desc.data
        db.session.commit()
        flash('Course updated.')
        return redirect(url_for(INDEX_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _form.course_name.data = _course.course_name
    _form.course_code.data = _course.course_code
    _form.course_group.data = _course.course_group
    _form.course_desc.data = _course.course_desc
    return render_template('admin/edit_course.html', title='Edit Course',
                        form=_form)


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

    _user_id = int(current_user.get_id())

    _assoc = Association.query.filter(
        Association.course_id == _course.course_id,
        Association.user_id == _user_id,
        Association.role_id == '1').all()

    # Only administrators and chairs can delete courses
    if not current_user.is_admin and len(_assoc) == 0:
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    _form = DeleteCourseForm()

    if _form.validate_on_submit():
        if _form.submit.data:
            for _a in _assoc:
                db.session.delete(_a)
            db.session.delete(_course)
            db.session.commit()
            flash('Course deleted.')
        return redirect(url_for(INDEX_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _course_name = _course.course_name
    return render_template('admin/delete_course.html',
                            title='Delete Course', course_name=_course_name,
                            form=_form)


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
        _role = Role(role_name=_form.role_name.data,
                     role_privilege=_form.role_privilege.data)
        db.session.add(_role)
        db.session.commit()
        flash('Role added.')
        return redirect(url_for(ROLES_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
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
    _form = EditRoleForm(_role.role_name, _role.role_privilege)

    if _form.validate_on_submit():
        _role.role_name = _form.role_name.data
        _role.role_privilege = _form.role_privilege.data
        db.session.commit()
        flash('Role updated.')
        return redirect(url_for(ROLES_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _form.role_name.data = _role.role_name
    _form.role_privilege.data = _role.role_privilege
    return render_template('admin/edit_role.html', title='Edit Role',
                            form=_form)


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

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _role_name = _role.role_name
    _role_privilege = _role.role_privilege
    return render_template('admin/delete_role.html', title='Delete Role',
                            role_name=_role_name,
                            role_privilege=_role_privilege, form=_form)
    

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

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
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
    _form = EditUserForm(_user.username, _user.user_email)

    if _form.validate_on_submit():
        _user.username = _form.username.data
        _user.user_email = _form.user_email.data
        _user.is_admin = _form.is_admin.data
        if _form.password.data.strip() != '':
            _user.set_password(_form.password.data)
        db.session.commit()
        flash('User updated.')
        return redirect(url_for(USERS_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _form.username.data = _user.username
    _form.user_email.data = _user.user_email
    _form.is_admin.data = _user.is_admin
    return render_template('admin/edit_user.html', title='Edit User',
                            form=_form)


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

    # Do not let users delete themselves!
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
    
    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _username = _user.username
    return render_template('admin/delete_user.html', title='Delete User',
                            username=_username, form=_form)


@admin_bp.route('/assign_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def assign_course(course_id):
    # type: (int) -> str
    """Assign users to a course.

    :param int course_id: The ID of the course to modify access

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Validate inputs
    validate_input('course_id', course_id, int)
    
    _user_id = int(current_user.get_id())

    _assoc = Association.query.filter(
        Association.course_id == course_id,
        Association.user_id == _user_id,
        ((Association.role_id == '1') | (Association.role_id == '2'))).all()

    # Only administrators, chairs, and teachers can edit courses
    if not current_user.is_admin and len(_assoc) == 0:
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    # Instantiate the form
    _form = SimpleForm()

    # Get the course data (e.g., course_id, course_name) from the database
    _course = Course.query.get_or_404(course_id)

    # Get a list of roles from the database
    _roles = Role.query.all()
    
    # Ensure the result is a list so you can iterate over it
    # even if it only contains one Role object
    _roles = [_roles] if not isinstance(_roles, list) else _roles

    # Create a list to hold role information
    # You will iterate through this list of dictionaries,
    # instead of a list of Role objects, when you render the webpage,
    # since you will temporarily add a 'Not Assigned' role to it
    _roles_list = []

    for _r in _roles:
        _role_dict = _r.__dict__
        _roles_list.append(_role_dict)
    
    # Temporarily add a 'Not Assigned' role
    # Users in this role will be deleted from the Association table
    # or skipped if they are not in the table
    # You will not store 'Not Assigned' users, since that will increase
    # the size of the Association table and slow down queries
    _roles_list.append({"role_id": 4, "role_name": "Not Assigned"})
    
    # Get a list of users by name from the database
    _users = User.query.order_by(User.username).all()
    
    # Ensure the result is a list so you can iterate over it
    # even if it only contains one User object
    _users = [_users] if not isinstance(_users, list) else _users
    
    # Create a list to hold user information
    # You will iterate through this list of dictionaries,
    # instead of a list of User objects, when you render the webpage,
    # since you have to temporarily add a 'role_id' column
    _users_list = []

    for _u in _users:
        _user_dict = _u.__dict__
        
        # Temporarily add a 'role_id' column
        # and set the default value to 4 ('Not Assigned')
        # That will ensure at least one radio button is checked
        # when you render the webpage 
        _user_dict['role_id'] = 4
        
        # Update the role_id if a value exists in the Association Table
        _a = Association.query.filter(
            Association.course_id == _course.course_id,
            Association.user_id == _user_dict['user_id']).first()

        if _a is not None:
            _user_dict['role_id'] = _a.role_id

        # Add the user with the 'role_id' column to the list
        _users_list.append(_user_dict)

    if request.method == 'POST':
        # Iterate through each user and check if their assignment has changed
        for _u in _users_list:
            _user_id = str(_u['user_id'])
            
            _a = Association.query.filter(
                Association.course_id == _course.course_id,
                Association.user_id == _user_id).first()

            _role_id = int(request.form.get(_user_id))
            
            # If the assignment does not exist in the Association table
            # but the course is now assigned
            if _a is None and _role_id < 4:
                print('Adding...')
                _new_assoc = Association(course_id=_course.course_id,
                                        role_id=_role_id,
                                        user_id=_user_id)
                db.session.add(_new_assoc)

            # If the assignment exist in the Association table
            # but the course is now unassigned
            elif _a is not None and _role_id == 4:
                print('Deleting...')
                db.session.delete(_a)

            # If the row exist in the Association table but the role changed
            elif _a is not None and _a.role_id != _role_id:
                print('Updating...')
                _a.role_id = _role_id
            
            else:
                print('Skipping...')

        db.session.commit()                

        return redirect(url_for(INDEX_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'admin/assign_course.html',
        title='Assign Users to Course',
        course_name=_course.course_name,
        form=_form,
        roles=_roles_list,
        users_list=_users_list)

@admin_bp.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    # type: (int) -> str | Response
    """Use form input to update your profile.

    :return: The HTML code to display with {{ placeholders }} populated
    or redirect if the user is not an administrator or access another profile
    :rtype: str/Response
    """
    # Only you and administrators can update your profile
    if not current_user.is_admin and current_user.get_id() != user_id:
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    # Validate inputs
    validate_input('user_id', user_id, int)

    _user = User.query.get_or_404(user_id)
    _form = UpdateProfileForm(_user.user_email)

    if _form.validate_on_submit():
        _user.user_email = _form.user_email.data
        if _form.password.data.strip() != '':
            _user.set_password(_form.password.data)
        db.session.commit()
        flash('Profile updated.')
        return redirect(url_for(INDEX_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _username = _user.username
    _form.user_email.data = _user.user_email
    return render_template('admin/update_profile.html',
                            title='Update Profile', form=_form,
                            username=_username)
