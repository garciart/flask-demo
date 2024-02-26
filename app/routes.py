"""Routing manager for Class Manager.
"""
# noqa F401 for type hints Flake8 does not detect
from flask import (render_template, flash, redirect, Response,  # noqa F401
                   url_for, request)
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug import exceptions  # noqa F401
from urllib.parse import urlsplit
from app import app, db
from app.cm_utils import validate_input
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    # type: () -> str
    """The landing page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Class Manager'
    _users = User.query.all()
    _html = render_template('index.html', page_title=_page_title,
                            users=_users)
    return _html


@app.route('/about')
@login_required
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

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    _page_title = 'Login'
    _form = LoginForm()

    if _form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == _form.username.data))
        if user is None or not user.check_password(_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

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
