"""Error routing manager.

Test 404: http://127.0.0.1:5000/bad/bad_route
"""
# Flake8 F401: imports are used for type hints
from flask import (render_template, request, current_app)  # noqa: F401
from werkzeug import exceptions
from app.app_utils import validate_input
from app.error import error_bp


@error_bp.app_errorhandler(404)
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

    _page_title = '404 Error'
    _requested_url = f'{request.path}'
    _err_desc = f"'{_requested_url}': {str(e)}"
    current_app.logger.error(_err_desc)
    _html = render_template('error/error.html', page_title=_page_title,
                            err_desc=_err_desc), 404
    return _html


@error_bp.app_errorhandler(500)
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

    _page_title = '500 Error'
    _err_desc = f'{str(e)}'
    current_app.logger.error(_err_desc)
    _additional_info = "We've logged the error and we'll get to it right away."
    _html = render_template('error/error.html', page_title=_page_title,
                            err_desc=_err_desc,
                            additional_info=_additional_info), 500
    return _html
