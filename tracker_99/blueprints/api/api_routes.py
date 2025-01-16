"""API content routing manager.

Test: http://127.0.0.1:5000/api/test
"""

import os
from functools import wraps
from typing import Any, Callable, Union

from flask import Response, send_from_directory
from flask import jsonify, request
from sqlalchemy import func
from werkzeug.security import check_password_hash

from tracker_99.app_utils import decode_auth_token
from tracker_99.app_utils import encode_auth_token
from tracker_99.blueprints.api import api_bp
from tracker_99.models.models import Member


# Allow `except Exception as e` so issues can percolate up, like ValueErrors from the model
# pylint: disable=broad-except


@api_bp.route('/api/login', methods=['POST'])
def login() -> tuple:
    """Return a JWT token for API requests if the requester's credentials are valid.

    Bash:
    curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"username":"admin","password":"Change.Me.321"}' \
        http://127.0.0.1:5000/api/login

    PS:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/login" \
        -Method Post \
        -ContentType "application/json" \
        -Body "{`"username`":`"admin`",`"password`":`"Change.Me.321`"}"

    :returns: The JWT token or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Get the contents of the curl --data option and assign them to variables
    _data = request.get_json()
    _submitted_name = _data.get('username')
    _submitted_password = _data.get('password')

    # Find requester by name (case-insensitive comparison)
    _requester = Member.query.filter(
        func.lower(Member.member_name) == func.lower(_submitted_name)
    ).first()

    # Ensure the requester is a member with correct credentials
    if _requester and check_password_hash(_requester.password_hash, _submitted_password):
        # Generate a JWT token containing the member ID
        _auth_token = encode_auth_token(_requester.member_id)
        if 'error' in _auth_token.lower():
            return jsonify({'error': _auth_token}), 500
        return jsonify({'message': 'Login successful.', 'auth_token': _auth_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials.'}), 401


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
        # so I would not have to perform the additional query, but I left it here,
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


@api_bp.route('/favicon.ico')
def api_get_favicon() -> Response:
    """Loads application icon.
    Prevents 404 errors when making API calls with no HTML because of missing icon.

    :returns: The favicon.ico file
    :rtype: Response
    """
    favicon_path = os.path.join('static', 'img', 'favicon.ico')
    return send_from_directory(
        os.path.dirname(favicon_path), os.path.basename(favicon_path), mimetype='image/x-icon'
    )


_DUMMY_DATA = [
    {
        'course_id': 1,
        'course_name': 'Python 101',
        'course_code': 'CS100',
        'course_group': 'SDEV',
        'course_desc': 'Introduction to Python.',
    },
    {
        'course_id': 2,
        'course_name': 'Flask 101',
        'course_code': 'CS101',
        'course_group': 'SDEV',
        'course_desc': 'Introduction to Flask.',
    },
]


@api_bp.route('/api/test', methods=['GET'])
def api_get_test_data() -> tuple:
    """Respond to an API request for test data.

    Bash: curl http://127.0.0.1:5000/api/test

    PS: Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/test"

    :returns: The data in JSON format and the HTTP status code (Response, int)
    :rtype: tuple
    """
    return jsonify(test_data=_DUMMY_DATA, status=200, mimetype='application/json'), 200
