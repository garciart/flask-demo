"""API content routing manager.

Test: http://127.0.0.1:5000/api/test
"""

import os
from functools import wraps
from typing import Any, Callable, Union

from flask import Response, jsonify, send_from_directory, request
from sqlalchemy import func
from werkzeug.security import check_password_hash

from tracker_99 import db
from tracker_99.app_utils import validate_input, encode_auth_token, decode_auth_token
from tracker_99.blueprints.api import api_bp
from tracker_99.models.models import Member

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

NOT_AUTH_MSG = 'You do not have permission to perform that action.'


def token_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that protects a route by requiring a valid JWT token.

    This decorator checks if a valid JWT token is included in the request's
    `Authorization` header. If the token is missing or invalid, an error response
    is returned. If the token is valid, the wrapped function is executed with
    additional user data (e.g., `user_id`, `user_is_admin`).

    :param f: The original view function to be wrapped.
    :type f: function
    :return: A wrapped version of the original function with JWT token validation.
    :rtype: Callable[..., Any]
    """

    @wraps(f)
    def wrapped_function(*args, **kwargs) -> Union[tuple, str]:
        """Checks for authorization and then runs the wrapped function.

        This function checks for a valid JWT token in the `Authorization` header.
        If the token is valid, it decodes the token to extract user information
        and passes that data to the wrapped function. If the token is invalid or
        missing, an error response is returned.

        :returns: Either the HTTP response from the wrapped function (with user info)
                  or an error message and status code.
        :rtype: Union[tuple, str]
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing authorization token.'}), 401

        # Token is expected to be in the format "Bearer <token>"
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({'error': 'Invalid token format.'}), 400

        # Decode the token to get the user's info
        user_id = decode_auth_token(auth_token)
        if not user_id:
            return jsonify({'error': 'Invalid or expired token.'}), 401

        # Fetch the member associated with the user_id
        member = Member.query.filter_by(member_id=user_id).first()
        if member:
            # If token is valid, pass user information to the protected route
            return f(*args, **kwargs, user_id=user_id, user_is_admin=member.is_admin)
        else:
            return jsonify({'error': 'User not found.'}), 404

    return wrapped_function


@api_bp.route('/api/test', methods=['GET'])
def api_get_test_data() -> tuple:
    """Get the list of test data when a REST call is made.

    Example:

    Linux:
    curl http://127.0.0.1:5000/api/test

    Windows:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/test"

    :returns: The data in JSON format (Response) and the HTTP status code (int)
    :rtype: tuple
    """
    return jsonify(test_data=_DUMMY_DATA, status=200, mimetype='application/json'), 200


@api_bp.route('/api/login', methods=['POST'])
def login() -> tuple:
    """Login and return a JWT token.

    Examples:

    Bash:
    curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"username":"admin","password":"Change.Me.321"}' \
        http://127.0.0.1:5000/api/login

    PowerShell:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/login" `
        -Method Post `
        -ContentType "application/json" `
        -Body "{`"username`":`"admin`",`"password`":`"Change.Me.321`"}"

    :returns: The JWT token or an error message (Response) and the HTTP status code (int)
    :rtype: tuple
    """
    data = request.get_json()
    submitted_name = data.get('username')
    submitted_password = data.get('password')

    # Find member by name (case-insensitive comparison)
    member = Member.query.filter(
        func.lower(Member.member_name) == func.lower(submitted_name)
    ).first()

    if member and check_password_hash(member.password_hash, submitted_password):
        # Generate JWT token
        auth_token = encode_auth_token(member.member_id)
        if 'error' in auth_token.lower():
            return jsonify({'error': auth_token}), 500
        return jsonify({'message': 'Login successful.', 'auth_token': auth_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials.'}), 401


@api_bp.route('/api/members/all', methods=['GET'], endpoint='get_all_members')
@token_required
def api_get_all_members(**kwargs) -> tuple:
    """Get the list of members in the database when a REST call is made.

    Examples:

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/all

    PowerShell:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/all" `
        -Method GET `
        -Headers @{ "Authorization" = "Bearer json.web.token" }

    :returns: The data in JSON format (Response) and the HTTP status code (int)
    :rtype: tuple
    """
    # Check if admin
    if not kwargs.get('user_is_admin', False):
        return jsonify({'error': NOT_AUTH_MSG}), 403

    # query.all() always returns a list, even if it is empty
    _members_list = Member.query.all()

    if not _members_list:
        return jsonify({'error': 'No members found.'}), 404

    # Exclude the 'password_hash' field
    _filtered_members = [
        {
            'member_id': m.member_id,
            'member_name': m.member_name,
            'member_email': m.member_email,
            'is_admin': m.is_admin,
        }
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/members/<int:member_id>', methods=['GET'], endpoint='get_member')
@token_required
def api_get_member(member_id: int, **kwargs) -> tuple:
    """Get a member from the database using their ID when a REST call is made.

    Examples:

    Linux:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/2

    Windows:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/2" `
        -Method GET `
        -Headers @{ "Authorization" = "Bearer json.web.token" }

    :param int member_id: The member to retrieve by ID

    :returns: The data in JSON format (Response) and the HTTP status code (int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    print("kwargs.get('user_id')", kwargs.get('user_id'), type(kwargs.get('user_id')))

    # Check if admin
    if not kwargs.get('user_is_admin', False) and int(kwargs.get('user_id')) != member_id:
        return jsonify({'error': NOT_AUTH_MSG}), 403

    # Remember, when querying for a single result, like `Foo.query.first()`,
    # use the following code to return a list if the result was None:
    # _foo = Foo.query.first()
    # _foo = [_foo] if _foo is not None else []

    _member = Member.query.get(member_id)

    if not _member:
        return jsonify({'error': 'Member not found.'}), 404

    _members_list = [_member] if _member is not None else []

    # Exclude the 'password_hash' field
    _filtered_members = [
        {
            'member_id': m.member_id,
            'member_name': m.member_name,
            'member_email': m.member_email,
            'is_admin': m.is_admin,
        }
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200


@api_bp.route('/api/members/<int:member_id>', methods=['PUT'], endpoint='update_member')
@token_required
def api_update_member(member_id: int, **kwargs) -> tuple:
    """Update a member through an API ReST call using their ID.

    Examples:

    Linux:
    curl -X PUT -H "Content-Type: application/json" \
        -H "Authorization: Bearer json.web.token" \
        -d '{"member_name": "Leto.Atreides", "member_email": "leto.atreides@atreides.com", "is_admin": true}' \
        http://localhost:5000/api/members/2

    Windows:
    Invoke-WebRequest -Uri "http://localhost:5000/api/members/2" `
        -Method Put `
        -ContentType "application/json" `
        -Headers @{ "Authorization" = "Bearer json.web.token" } `
        -Body "{`"member_name`": `"Leto.Atreides`", `"member_email`": `
        `"leto.atreides@atreides.com`", `"is_admin`": true }"

    :param int member_id: The member to update by ID

    :returns: The data in JSON format (Response) and the HTTP status code (int)
    :rtype: tuple
    """
    # External method that throws an exception if member_id is not an int, or it is empty
    validate_input('member_id', member_id, int)

    # Check if admin
    if not kwargs.get('user_is_admin', False):
        return jsonify({'error': NOT_AUTH_MSG}), 403

    # Query the member by ID
    _member = Member.query.get(member_id)

    # If member is not found, return 404
    if not _member:
        return jsonify({'error': 'Member not found.'}), 404

    # Get the JSON data from the request
    data = request.get_json()

    # Update member attributes if provided in the request
    if 'member_name' in data:
        validate_input("data['member_name']", data['member_name'], str)
        _member.member_name = data['member_name']
    if 'member_email' in data:
        validate_input("data['member_email']", data['member_email'], str)
        _member.member_email = data['member_email']
    if 'is_admin' in data:
        validate_input("data['is_admin']", data['is_admin'], bool)
        _member.is_admin = bool(data['is_admin'])

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': f'Successfully updated {_member.member_name}.'}), 200


@api_bp.route('/favicon.ico')
def api_get_favicon() -> Response:
    """Loads application icon when making API calls with no HTML.

    :returns: The favicon.ico file
    :rtype: Response
    """
    favicon_path = os.path.join('static', 'img', 'favicon.ico')
    return send_from_directory(
        os.path.dirname(favicon_path), os.path.basename(favicon_path), mimetype='image/x-icon'
    )
