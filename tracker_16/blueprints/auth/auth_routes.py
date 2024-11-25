"""Authentication and authorization routing manager.

Test: http://127.0.0.1:5000/login
"""
from urllib.parse import urlsplit

from flask import (Response,
                   flash, redirect, render_template,
                   request, url_for)
from flask_login import (current_user, login_user, logout_user)
from sqlalchemy import select

from tracker_16 import db
from tracker_16.blueprints.auth import auth_bp
from tracker_16.blueprints.auth.auth_forms import (LoginForm)
from tracker_16.models.member import Member

INDEX_PAGE = 'main_bp.index'
LOGIN_PAGE = 'auth_bp.login'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """The login page.

    :returns: The HTML code to display with {{ placeholders }} populated, \
        or a redirection if the user is logged in, \
        or a redirection if the user came from another site
    :rtype: str/Response
    """
    if current_user.is_authenticated:
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Log In'
    _form = LoginForm()

    if _form.validate_on_submit():

        _member = db.session.scalar(
            select(Member).where(
                Member.member_name.ilike(_form.member_name.data)))

        print(_form.password.data)

        if _member is None or not _member.verify_password(_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for(LOGIN_PAGE))

        login_user(_member, remember=_form.remember_me.data)

        _next_page = request.args.get('next')

        if not _next_page or urlsplit(_next_page).netloc != '':
            _next_page = url_for(INDEX_PAGE)

        flash(f'Welcome, {_member.member_name}!')

        return redirect(_next_page)

    return render_template('login.html',
                           page_title=_page_title, form=_form)


@auth_bp.route('/logout')
def logout() -> Response:
    """The logout page.

    :returns: A response object
    :rtype: Response
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for(INDEX_PAGE))
