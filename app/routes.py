"""Routes for Class Manager

Usage:
- python3 -m flask --app cm run
- python3 -m flask --app cm run --debug # Allow hot reload
"""
import os
import sys
import inspect
from types import FrameType
import logging
from flask import render_template
from werkzeug import exceptions  # noqa F401
from app import app, cm_logger
from app.forms import LoginForm

__author__ = 'Rob Garcia'

# Set up logging
try:
    logging_level = getattr(logging, app.config['LOGGING_LEVEL'])
except AttributeError:
    # Set to logging.DEBUG
    logging_level = 10
logger = cm_logger.create_logger('cm_logger', logging_level)
LOG_ROOT = os.environ.get('LOG_ROOT') == 'True'
if LOG_ROOT:
    logging.basicConfig(
        filename='cm.log', level=logging.DEBUG,
        format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Get Python version and convert to float (e.g., 3.9 -> 3.09)
PYTHON_VERSION = float(
    f'{sys.version_info.major}.{sys.version_info.minor:02d}')


@app.route('/')
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
    _html = render_template('About.html', page_title=_page_title)
    return _html


@app.route('/login')
def login():
    # type: () -> str
    """The login page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Login'
    _form = LoginForm()
    _html = render_template('login.html', page_title=_page_title, form=_form)
    return _html


@app.errorhandler(404)
def page_not_found(e):
    # type: (exceptions.NotFound) -> (str, int)
    """Display the error page if page not found.

    :param exceptions.NotFound e: An instance of the
    werkzeug.exceptions.NotFound class

    :return: A string of HTML code with the response code
    :rtype: tuple
    """
    # Validate inputs

    _err_desc = e.get_description()
    _page_title = '404 Error'
    _html = render_template('error.html', page_title=_page_title,
                            err_desc=_err_desc), 404
    return _html


@app.errorhandler(500)
def internal_server_error(e):
    # type: (exceptions.InternalServerError) -> (str, int)
    """Display the error page if there is an internal server error.

    :param exceptions.InternalServerError e: An instance of the
    werkzeug.exceptions.InternalServerError class

    :return: A string of HTML code with the response code
    :rtype: tuple
    """
    _err_desc = e.get_description()
    _page_title = '404 Error'
    _additional_info = "We've logged the error and we'll get to it right away."
    _html = render_template('error.html', page_title=_page_title,
                            err_desc=_err_desc,
                            additional_info=_additional_info), 500
    return _html


def __validate_inputs(obj_name, obj_to_check, expected_type):
    # type: (str, object, type) -> None
    """Validate an input's type and ensure it is not empty. Use this
    function to reduce code complexity in calling functions and methods.

    :param str obj_name: The name of the input to validate
    :param object obj_to_check: The input to validate
    :param type expected_type: The expected type for the input

    :returns: None
    """
    # Validate inputs
    if not isinstance(obj_name, str):
        raise TypeError('obj_name must be type <str>.')

    if not isinstance(expected_type, type):
        raise TypeError('expected_type must be type <type>.')

    _calling_method = inspect.currentframe().f_back

    if not isinstance(obj_to_check, expected_type):
        _error_msg = "'{0}' is not type {1}.".format(obj_name, expected_type)
        _log_error_and_exit(_error_msg, _calling_method)

    if isinstance(obj_to_check, str) and obj_to_check == '':
        _error_msg = "'{0}' is empty.".format(obj_name)
        _log_error_and_exit(_error_msg, _calling_method)

    if isinstance(obj_to_check, (str, list, dict)) and len(obj_to_check) == 0:
        _error_msg = "'{0}' is empty.".format(obj_name)
        _log_error_and_exit(_error_msg, _calling_method)


def _log_error_and_exit(error_msg, calling_method=None):
    # type: (str, FrameType) -> None
    """Provide the location of the error and a message

    :param str error_msg: A custom error message
    :param types.FrameType calling_method: An object containing stack
        information (e.g., where the error occurred), defaults to None. If not
        provided, this function will use the stack of the previous function
    :returns: None
    """
    # Validate inputs
    if not isinstance(error_msg, str):
        raise TypeError('obj_name must be type <str>.')

    if calling_method is not None and not isinstance(calling_method,
                                                     FrameType):
        raise TypeError('expected_type must be type <types.FrameType>.')

    if calling_method is None:
        calling_method = inspect.currentframe().f_back

    _msg = '>>> Error: {0} (see {1}(), line {2}).'.format(
        error_msg,
        calling_method.f_code.co_name,
        calling_method.f_lineno)
    logger.critical(_msg)
    print(_msg)
    print('Exiting now...')
    sys.exit(1)


if __name__ == '__main__':
    # Default setting
    app.run(host='0.0.0.0', port=5000)
