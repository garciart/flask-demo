"""Routing manager for Class Manager.
"""
# noqa F401 for type hints Flake8 does not detect
from urllib.parse import urlsplit
from flask import (render_template, flash, redirect, Response,  # noqa F401
                   url_for, request)
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug import exceptions  # noqa F401
from app import app, db
from app.cm_utils import validate_input
from app.forms import LoginForm
from app.models import User, Course, Role, Association


@app.route('/')
@app.route('/index')
@login_required
def index():
    # type: () -> str
    """The landing page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Class Manager'

    _user_id = int(current_user.get_id())

    if _user_id == 1:
        # Get all courses if admin
        _courses = Course.query.all()
    else:
        # Your query
        _courses = db.session.query(
            Course.course_id, Course.course_name, Course.course_code,
            Course.course_desc,
            Role.role_name).join(
                Association,
                Course.course_id == Association.course_id).join(
                    Role, Role.role_id == Association.role_id).filter(
                        Association.user_id == _user_id).all()

    # Convert to list if there is only one result
    _courses = [_courses] if not isinstance(_courses, list) else _courses

    # Send the list to the page
    _html = render_template('index.html', page_title=_page_title,
                            courses=_courses)
    return _html


@app.route('/courses')
@login_required
def courses():
    # type: () -> str
    """The course list page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'List of Courses'

    _courses = Course.query.all()

    _html = render_template('courses.html', page_title=_page_title,
                            courses=_courses)
    return _html


@app.route('/roles')
@login_required
def roles():
    # type: () -> str
    """The role list page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'List of Roles'

    _roles = Role.query.all()

    _html = render_template('roles.html', page_title=_page_title,
                            roles=_roles)
    return _html


@app.route('/users')
@login_required
def users():
    # type: () -> str
    """The user list page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'List of Users'

    if int(current_user.get_id()) == 1:
        _users = User.query.all()
    else:
        _users = User.query.get_or_404(current_user.get_id(),
                                       'You must log in.')

    # Convert to list if there is only one result
    _users = [_users] if not isinstance(_users, list) else _users

    _html = render_template('users.html', page_title=_page_title,
                            users=_users)
    return _html


@app.route('/test_gridjs')
def test_gridjs():
    # type: () -> str
    """Test of Grid.js with base.html.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Grid.js Test'
    _users = User.query.all()
    _html = render_template('test_gridjs.html', page_title=_page_title,
                            users=_users)
    return _html


@app.route('/test_one_page')
def test_one_page():
    # type: () -> str
    """Test without template inheritance.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'One Page Test'
    _users = User.query.all()
    _html = render_template('test_one_page.html', page_title=_page_title,
                            users=_users)
    return _html


@app.route('/about')
def about():
    # type: () -> str
    """The about page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'About'
    _html = render_template('about.html', page_title=_page_title)
    return _html


@app.route('/login', methods=['GET', 'POST'])
def login():
    # type: () -> str
    """The login page.

    :return: The HTML code to display with {{ placeholders }} populated,
    or a redirection if the user is logged in,
    or a redirection if the user came from another site
    :rtype: str
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    _page_title = 'Login'
    _form = LoginForm()

    if _form.validate_on_submit():
        _user = db.session.scalar(
            sa.select(User).where(User.username.ilike(_form.username.data)))

        if _user is None or not _user.check_password(_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(_user, remember=_form.remember_me.data)
        _next_page = request.args.get('next')

        if not _next_page or urlsplit(_next_page).netloc != '':
            _next_page = url_for('index')

        return redirect(_next_page)

    _html = render_template('login.html', page_title=_page_title, form=_form)
    return _html


@app.route('/logout')
def logout():
    # type: () -> Response
    """The logout page.

    :return: A response object
    :rtype: flask.Response
    """
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    # type: (exceptions.NotFound) -> tuple[str, int]
    """Display the error page if page not found.

    :param exceptions.NotFound e: An instance of the
    werkzeug.exceptions.NotFound class

    :return: A string of HTML code with the response code
    :rtype: tuple
    """
    # Validate inputs
    validate_input('e', e, exceptions.NotFound)

    _err_desc = e.get_description()
    _page_title = '404 Error'
    _html = render_template('error.html', page_title=_page_title,
                            err_desc=_err_desc), 404
    return _html


@app.errorhandler(500)
def internal_server_error(e):
    # type: (exceptions.InternalServerError) -> tuple[str, int]
    """Display the error page if there is an internal server error.

    :param exceptions.InternalServerError e: An instance of the
    werkzeug.exceptions.InternalServerError class

    :return: A string of HTML code with the response code
    :rtype: tuple
    """
    # Validate inputs
    validate_input('e', e, exceptions.InternalServerError)

    _err_desc = e.get_description()
    _page_title = '404 Error'
    _additional_info = "We've logged the error and we'll get to it right away."
    _html = render_template('error.html', page_title=_page_title,
                            err_desc=_err_desc,
                            additional_info=_additional_info), 500
    return _html
