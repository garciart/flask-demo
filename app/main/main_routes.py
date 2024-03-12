"""Main content routing manager.

TODO: Replace role_id with a privilege level system!

Test: http://127.0.0.1:5000
"""
# Flake8 F401: imports are used for type hints
from flask import (flash, redirect, render_template,
                   request, url_for)
from flask_login import (current_user, login_required)
from app import db
from app.main import bp
from app.models import (User, Course, Role, Association)

_DUMMY_DATA = [
    {'course_id': 1, 'course_name': 'Python 101', 'course_code': 'CS100',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Python.',
     'role_name': 'Teacher'},
    {'course_id': 2, 'course_name': 'Flask 101', 'course_code': 'CS101',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Flask.',
     'role_name': 'Student'}
]

INDEX_PAGE = 'main.index'
NOT_AUTH_MSG1 = 'You must be an administrator to perform that action.'
NOT_AUTH_MSG2 = (
    'You must be an administrator or chair to perform that action.')


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # type: () -> str
    """The landing page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Flask Demo'

    if current_user.is_admin:
        _courses = Course.query.all()
    else:
        _user_id = int(current_user.get_id())

        _courses = db.session.query(
            Course.course_id, Course.course_name, Course.course_code,
            Course.course_group, Course.course_desc,
            Role.role_id, Role.role_name).join(
                Association,
                Course.course_id == Association.course_id).join(
                    Role, Role.role_id == Association.role_id).filter(
                        Association.user_id == _user_id).all()

    # Convert to list if there is only one result
    _courses = [_courses] if not isinstance(_courses, list) else _courses

    # Send the list to the page
    _html = render_template('main/index.html', page_title=_page_title,
                            courses=_courses)
    return _html


@bp.route('/about')
def about():
    # type: () -> str
    """The about page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'About'
    _html = render_template('main/about.html', page_title=_page_title)
    return _html


@bp.route('/courses')
@login_required
def courses():
    # type: () -> str
    """The course list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'List of Courses'

    _courses = Course.query.all()

    # Convert to list if there is only one result
    _courses = [_courses] if not isinstance(_courses, list) else _courses

    _html = render_template('main/courses.html', page_title=_page_title,
                            courses=_courses)
    return _html


@bp.route('/roles')
@login_required
def roles():
    # type: () -> str
    """The role list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'List of Roles'
    
    _roles = Role.query.all()

    # Convert to list if there is only one result
    _roles = [_roles] if not isinstance(_roles, list) else _roles

    _html = render_template('main/roles.html', page_title=_page_title,
                            roles=_roles)
    return _html


@bp.route('/users')
@login_required
def users():
    # type: () -> str
    """The user list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        flash(NOT_AUTH_MSG1)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'List of Users'

    _users = User.query.all()

    # Convert to list if there is only one result
    _users = [_users] if not isinstance(_users, list) else _users

    _html = render_template('main/users.html', page_title=_page_title,
                            users=_users)
    return _html


@bp.route('/test')
@login_required
def test():
    # type: () -> str
    """Test page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Flask Demo'

    _courses = _DUMMY_DATA

    _html = render_template('main/index.html', page_title=_page_title,
                            courses=_courses)
    return _html
