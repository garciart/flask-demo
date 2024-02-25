"""Routing manager for Class Manager.
"""

from flask import render_template, flash, redirect, url_for
from werkzeug import exceptions  # noqa F401
from app import app
from app.cm_utils import validate_inputs
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    # type: () -> str
    """The landing page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Class Manager'
    _html = render_template('index.html', page_title=_page_title)
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

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Login'
    _form = LoginForm()

    if _form.validate_on_submit():
        flash(f'Login requested for user {_form.username.data}, '
              f'remember_me={_form.remember_me.data}')
        return redirect(url_for('index'))

    _html = render_template('login.html', page_title=_page_title, form=_form)
    return _html


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
    validate_inputs('e', e, exceptions.NotFound)

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
    validate_inputs('e', e, exceptions.InternalServerError)

    _err_desc = e.get_description()
    _page_title = '404 Error'
    _additional_info = "We've logged the error and we'll get to it right away."
    _html = render_template('error.html', page_title=_page_title,
                            err_desc=_err_desc,
                            additional_info=_additional_info), 500
    return _html
