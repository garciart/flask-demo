"""Authentication and authorization routing manager.

NOTE - Imports within functions are to prevent a known
circular import problem in Flask.

Test: http://127.0.0.1:5000/login
"""
from urllib.parse import urlsplit
# Flake8 F401: imports are used for type hints
from flask import (Response,  # noqa: F401
                   flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select
from app.auth import auth_bp
from app.auth.auth_forms import LoginForm
from app import db
from app.models import User


INDEX_PAGE = 'main.index'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # type: () -> str
    """The login page.

    :returns: The HTML code to display with {{ placeholders }} populated,
    or a redirection if the user is logged in,
    or a redirection if the user came from another site
    :rtype: str
    """
    if current_user.is_authenticated:
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Log In'
    _form = LoginForm()

    if _form.validate_on_submit():
        _user = db.session.scalar(
            select(User).where(
                User.username.ilike(_form.username.data)))

        if _user is None or not _user.check_password(_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(_user, remember=_form.remember_me.data)

        _next_page = request.args.get('next')

        if not _next_page or urlsplit(_next_page).netloc != '':
            _next_page = url_for(INDEX_PAGE)

        return redirect(_next_page)

    _html = render_template('auth/login.html',
                            page_title=_page_title, form=_form)
    return _html


@auth_bp.route('/logout')
def logout():
    # type: () -> Response
    """The logout page.

    :returns: A response object
    :rtype: Response
    """
    logout_user()
    return redirect(url_for(INDEX_PAGE))
