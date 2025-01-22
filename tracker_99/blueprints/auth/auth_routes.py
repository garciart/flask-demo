"""Authentication and authorization routing manager.

Test: http://127.0.0.1:5000/login
"""

from typing import Union
from urllib.parse import urlsplit

from flask import Response, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from markupsafe import escape
from sqlalchemy import select

from tracker_99 import db, constants as c
from tracker_99.blueprints.auth import auth_bp
from tracker_99.blueprints.auth.auth_forms import LoginForm
from tracker_99.models.models import Member


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> Union[str, Response]:
    """The login page.

    :returns: The HTML code to display with {{ placeholders }} populated, \
        or a redirection if the user is logged in, \
        or a redirection if the user came from another site
    :rtype: str/Response
    """
    if current_user.is_authenticated:
        return redirect(url_for(c.INDEX_PAGE))

    _page_title = 'Log In'
    _page_description = 'Log In'

    _form = LoginForm()

    # Always redirect to the index page to avoid URL injections
    _next_page = url_for(c.INDEX_PAGE)

    if request.method == 'POST' and _form.validate_on_submit():
        _member = db.session.scalar(
            select(Member).where(Member.member_name.ilike(_form.member_name.data))
        )

        if _member is None or not _member.verify_password(_form.password.data):
            flash('Invalid member name or password')
            return redirect(url_for(c.LOGIN_PAGE))

        login_user(_member, remember=_form.remember_me.data)

        return redirect(_next_page)

    return render_template(
        'login.html', page_title=_page_title, page_description=_page_description,
        form=_form, next_page=_next_page
    )


@auth_bp.route('/logout')
def logout() -> Response:
    """The logout page.

    :returns: A response object
    :rtype: Response
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for(c.INDEX_PAGE))
