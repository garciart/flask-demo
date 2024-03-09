"""Main content routing manager.

Test: http://127.0.0.1:5000
"""
# Flake8 F401: imports are used for type hints
from flask import (abort, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.main_forms import AccessChoiceForm, UserAccessForm
from app.models import User, Course, Role, Association

_DUMMY_DATA = [
    {'course_id': 1, 'course_name': 'Python 101', 'course_code': 'CS100',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Python.',
     'role_name': 'Teacher'},
    {'course_id': 2, 'course_name': 'Flask 101', 'course_code': 'CS101',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Flask.',
     'role_name': 'Student'}
]

INDEX_PAGE = 'main.index'
LOGIN_REQ_MSG = 'You must log in.'


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
    # An alternate way of preventing non-admins from accessing page
    if not current_user.is_admin:
        _roles = Role.query.get_or_404(current_user.get_id(),
                                       LOGIN_REQ_MSG)
    else:
        _roles = Role.query.all()

    _page_title = 'List of Roles'

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


@bp.route('/scratch/<int:course_id>', methods=['GET', 'POST'])
@login_required
def scratch(course_id):
    # type: (int) -> str
    """Scratch page.

    :param int course_id: The ID of the course to modify access

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Assign Users to Course'

    _form = UserAccessForm()
    _course = Course.query.get_or_404(course_id)

    if _form.validate_on_submit():
        print('Submitted')
    elif request.method == 'GET':
        _users = User.query.order_by(User.username).all()

        for _u in _users:
            print(_u.user_id, _u.username)

        # Convert to list if there is only one result
        _users = [_users] if not isinstance(_users, list) else _users

        for _u in _users:
            _a = Association.query.filter(
                Association.course_id == course_id,
                Association.user_id == _u.user_id).first()

            _access_form = AccessChoiceForm()

            if _a is None:
                _access_form.access_code = 4
            else:
                _access_form.access_code = _a.role_id

            _form.access_fields.append_entry(_access_form)

        return render_template(
            'main/scratch.html',
            page_title=_page_title,
            form=_form,
            course_name=_course.course_name,
            users=_users,
            zip_object=zip(_form.access_fields, _user_fields)
        )
    else:
        abort(500)


@bp.route('/scratch/<int:course_id>', methods=['GET', 'POST'])
@login_required
def old_scratch(course_id):
    # type: (int) -> str
    """Scratch page.

    :param int course_id: The ID of the course to modify access

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Assign Users to Course'

    _form = UserAccessForm()
    _course = Course.query.get_or_404(course_id)
    _user_fields = []

    if _form.validate_on_submit():
        print('Submitted')
    elif request.method == 'GET':
        # _users = User.query.order_by(User.username).all()
        _users = User.query.all()
        for _u in _users:
            print(_u.user_id, _u.username)

        for _u in User.query.all():

            _user_fields.append(_u)

            _a = Association.query.filter(
                Association.course_id == course_id,
                Association.user_id == _u.user_id).first()

            _access_form = AccessChoiceForm()

            if _a is None:
                _access_form.access_code = 4
            else:
                _access_form.access_code = _a.role_id

            _form.access_fields.append_entry(_access_form)

        return render_template(
            'main/scratch.html',
            page_title=_page_title,
            form=_form,
            course_name=_course.course_name,
            zip_object=zip(_form.access_fields, _user_fields)
        )
    else:
        abort(500)
