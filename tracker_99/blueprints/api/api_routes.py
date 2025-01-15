"""API content routing manager.

Test: http://127.0.0.1:5000/api/test
"""

import os

from flask import Response, jsonify, send_from_directory, request
from sqlalchemy import func
from werkzeug.security import check_password_hash

from tracker_99.app_utils import encode_auth_token
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


@api_bp.route('/api/test', methods=['GET'])
def api_get_test_data() -> tuple:
    """Respond to an API request for test data.

    Bash: curl http://127.0.0.1:5000/api/test

    PS: Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/test"

    :returns: The data in JSON format and the HTTP status code (Response, int)
    :rtype: tuple
    """
    return jsonify(test_data=_DUMMY_DATA, status=200, mimetype='application/json'), 200


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
