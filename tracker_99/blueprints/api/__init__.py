"""Initializes the blueprint object and other components related to the blueprint.

This file also turns the directory into a package whose scripts can be imported as modules.
"""

from functools import wraps
from typing import Any, Callable, Union

from flask import Blueprint
from flask import jsonify, request

from tracker_99.app_utils import decode_auth_token
from tracker_99.models.models import Member

api_bp = Blueprint('api_bp', __name__, template_folder='templates')


def token_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that protects a route by requiring a valid JWT token.

    This decorator checks if a valid JWT token is included in the request's
    `Authorization` header. If the token is missing or invalid, an error response
    is returned. If the token is valid, the wrapped function is executed with
    additional requester data (e.g., `requester_id`, `requester_is_admin`).

    :param Callable[..., Any] f: The function to wrap.

    :return: The original function wrapped with JWT token validation code.
    :rtype: Callable[..., Any]
    """

    @wraps(f)
    def wrapper(*args, **kwargs) -> Union[tuple, str]:
        """Checks for authorization and then runs the wrapped function.

        This function checks for a valid JWT token in the `Authorization` header.
        If the token is valid, it decodes the token to extract requester information
        and passes that data to the wrapped function. If the token is invalid or
        missing, an error response is returned.

        :returns: The HTTP response from the wrapped function (with requester info) \
            or an error message with the HTTP status code (Response, int)
        :rtype: Union[tuple, str]
        """
        _auth_header = request.headers.get('Authorization')
        if not _auth_header:
            return jsonify({'error': 'Missing authorization token.'}), 401

        # Token is expected to be in the format "Bearer <token>"
        try:
            _auth_token = _auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Invalid token format.'}), 400

        # Decode the token to get the requester's info
        _requester_id = decode_auth_token(_auth_token)
        if not _requester_id:
            return jsonify({'error': 'Invalid or expired token.'}), 401

        # Fetch the member associated with the _member_id
        # I considered adding is_admin to the token in app_utils.py
        # to avoid perform additional queries, but I left it here,
        # in case I wanted to add other attributes, like member_name, etc.
        """
        SELECT * FROM members WHERE member_id = 1 LIMIT 1;
        """
        _requester = Member.query.filter_by(member_id=_requester_id).first()
        if _requester:
            # If token is valid, pass requester information to the protected route
            # IMPORTANT - Do not add a response code to the return value;
            # the wrapped function will return the HTTP response code
            return f(*args, **kwargs, requester_id=_requester_id,
                     requester_is_admin=_requester.is_admin)
        else:
            return jsonify({'error': 'Requester not found.'}), 404

    return wrapper


# Import the other modules in the package after instantiating
# the Blueprint to avoid known circular import problems with Flask
from tracker_99.blueprints.api import (api_routes, api_routes_members, api_routes_courses,
                                       api_routes_roles)  # nopep8
