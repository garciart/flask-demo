"""API content routing manager.

Test: http://127.0.0.1:5000/api/test
"""

import os
from typing import Union

from flask import Response, jsonify, send_from_directory, request
from sqlalchemy import func
from werkzeug.security import check_password_hash

from tracker_17 import db
from tracker_17.app_utils import validate_input, encode_auth_token, decode_auth_token
from tracker_17.blueprints.api import api_bp
from tracker_17.models.member import Member

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


def token_required(f):
    """Decorator to require JWT authentication."""

    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization token is missing'}), 401

        # Token is expected to be in the format "Bearer <token>"
        auth_token = auth_header.split(" ")[1]

        # Decode the token
        member_id = decode_auth_token(auth_token)
        if not member_id:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # If token is valid, pass the member_id to the protected route
        # return f(member_id, *args, **kwargs)
        return f(*args, **kwargs)

    return decorator


@api_bp.route('/api/login', methods=['POST'])
def login() -> Response:
    """Login and return a JWT token.

    Examples:

    Linux:
    curl -X PUT -H "Content-Type: application/json" -d '{"username": "admin", \
        "password": "foobar"}' http://127.0.0.1:5000/api/login

    Windows:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/login" `
        -Method Post `
        -ContentType "application/json" `
        -Body "{`"username`": `"admin`", `"password`": `"Change.Me.321`"}"

    :returns: The JWT token
    :rtype: Response
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
        return jsonify({'message': 'Login successful', 'auth_token': auth_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


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


@api_bp.route('/api/test', methods=['GET'])
def api_get_test_data() -> Union[Response, tuple]:
    """Get the list of test data when a REST call is made.

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    _response = jsonify(test_data=_DUMMY_DATA, status=200, mimetype='application/json'), 200
    return _response


@api_bp.route('/api/members/all', methods=['GET'], endpoint='get_all_members')
@token_required
def api_get_all_members() -> Union[Response, tuple]:
    """Get the list of members in the database when a REST call is made.

    Examples:

    Linux:
    curl -X GET -H "Authorization: Bearer your.jwt.token.here"' \
        http://127.0.0.1:5000/api/members/all

    Windows:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/all" `
        -Method GET `
        -Headers @{ "Authorization" = "Bearer your.jwt.token.here" }

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    # query.all() always returns a list, even if it is empty
    _members_list = Member.query.all()

    if not _members_list:
        return jsonify({'error': 'No members found'}), 404

    # Exclude the 'password_hash' field
    _filtered_members = [
        {
            'member_id': m.member_id,
            'member_name': m.member_name,
            'member_email': m.member_email,
            'member_is_admin': m.member_is_admin,
        }
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200


# Do not forget to add an endpoint or you will get an AssertionError!
@api_bp.route('/api/members/<int:member_id>', methods=['GET'], endpoint='get_member')
@token_required
def api_get_member(member_id: int) -> Union[Response, tuple]:
    """Get a member from the database using their ID when a REST call is made.

    Examples:

    Linux:
    curl -X GET -H "Authorization: Bearer your.jwt.token.here"' \
        http://127.0.0.1:5000/api/members/2

    Windows:
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/members/2" `
        -Method GET `
        -Headers @{ "Authorization" = "Bearer your.jwt.token.here" }

    :param int member_id: The member to retrieve by ID

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Remember, when querying for a single result, like `Foo.query.first()`,
    # use the following code to return a list if the result was None:
    # _foo = Foo.query.first()
    # _foo = [_foo] if _foo is not None else []

    _member = Member.query.get(member_id)

    if not _member:
        return jsonify({'error': 'Member not found'}), 404

    _members_list = [_member] if _member is not None else []

    # Exclude the 'password_hash' field
    _filtered_members = [
        {
            'member_id': m.member_id,
            'member_name': m.member_name,
            'member_email': m.member_email,
            'member_is_admin': m.member_is_admin,
        }
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200


@api_bp.route('/api/members/<int:member_id>', methods=['PUT'], endpoint='update_member')
@token_required
def api_update_member(member_id: int) -> Union[Response, tuple]:
    """Update a member through an API ReST call using their ID.

    Examples:

    Linux:
    curl -X PUT -H "Content-Type: application/json" \
        -H "Authorization: Bearer your.jwt.token.here" \
        -d '{"member_name": "Leto.Atreides", \
        "member_email": "leto.atreides@atreides.com", "member_is_admin": true}' \
        http://localhost:5000/api/members/2

    Windows:
    Invoke-WebRequest -Uri "http://localhost:5000/api/members/2" `
        -Method Put `
        -ContentType "application/json" `
        -Headers @{ "Authorization" = "Bearer your.jwt.token.here" } `
        -Body "{`"member_name`": `"Leto.Atreides`", `"member_email`": `
        `"leto.atreides@atreides.com`", `"member_is_admin`": true}"

    :param int member_id: The member to update by ID

    :returns: A response with a message in JSON format
    :rtype: Response
    """
    # External method that throws an exception if member_id is not an int, or it is empty
    validate_input('member_id', member_id, int)

    # Query the member by ID
    _member = Member.query.get(member_id)

    # If member is not found, return 404
    if not _member:
        return jsonify({'error': 'Member not found'}), 404

    # Get the JSON data from the request
    data = request.get_json()

    # Update member attributes if provided in the request
    if 'member_name' in data:
        validate_input("data['member_name']", data['member_name'], str)
        _member.member_name = data['member_name']
    if 'member_email' in data:
        validate_input("data['member_email']", data['member_email'], str)
        _member.member_email = data['member_email']
    if 'member_is_admin' in data:
        validate_input("data['member_is_admin']", data['member_is_admin'], bool)
        _member.member_is_admin = bool(data['member_is_admin'])

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': f'Successfully updated {_member.member_name}.'}), 200
