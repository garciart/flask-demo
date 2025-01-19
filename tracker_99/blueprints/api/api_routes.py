"""API content routing manager.

Test: http://127.0.0.1:5000/api/test
"""

import os

from flask import Response, send_from_directory
from flask import jsonify, request
from sqlalchemy import Row, func
from werkzeug.security import check_password_hash

from tracker_99 import db, constants as c
from tracker_99.app_utils import encode_auth_token, validate_input
from tracker_99.blueprints.api import api_bp, token_required
from tracker_99.models.models import Association, Course, Member, Role


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


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/courses/get/details/<int:course_id>', methods=['GET'],
              endpoint='get_details')
@token_required
def api_get_details(course_id: int, **kwargs) -> tuple:
    """Respond to an API request to:

        - Admins: Get everyone assigned to a course and their roles.
        - Members: Get course information and their role in the course.

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" \
        http://127.0.0.1:5000/api/courses/get/assignment/2

    PS:
    Invoke-WebRequest -Method GET \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/courses/get/assignment/2"

    :param int course_id: The ID of the course to retrieve

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    # Get kwargs from the @token_required decorator
    _requester_id = kwargs.get('requester_id', 0)
    _is_admin = kwargs.get('requester_is_admin', False)

    """
    SELECT associations.member_id, members.member_name, courses.*, roles.*
    FROM associations, courses, members, roles
    WHERE associations.course_id = 12 AND
        associations.course_id = courses.course_id AND
        associations.member_id = members.member_id AND
        associations.role_id = roles.role_id;
    """
    _result = (db.session.query(Association.member_id, Member.member_name, Course, Role)
               .join(Course, Association.course_id == Course.course_id)
               .join(Member, Association.member_id == Member.member_id)
               .join(Role, Association.role_id == Role.role_id)
               .filter(Association.course_id == course_id)
               .all())
    if not _result:
        return jsonify({'error': c.NOT_FOUND_MSG}), 404

    def dict_builder(r: Row) -> dict:
        """Create a dictionary from a row in the results of a query.

        :param Row r: A SQLAlchemy row from the results of a query

        :returns: A dictionary containing keys and row values
        :rtype: dict
        """
        # Unpack the member_id and the course and role objects
        _member_id, _member_name, _course, _role = r
        return {
            'member_id': _member_id,
            'member_name': _member_name,
            'course_id': _course.course_id,
            'course_name': _course.course_name,
            'course_code': _course.course_code,
            'course_group': _course.course_group,
            'course_desc': _course.course_desc,
            'role_id': _role.role_id,
            'role_name': _role.role_name,
            'role_privilege': _role.role_privilege
        }

    if _is_admin:
        # For admin, return a list of all assigned courses
        _assigned_courses = [dict_builder(r) for r in _result]
        return jsonify(_assigned_courses), 200
    else:
        # For member, check if the requester is assigned to the course
        for r in _result:
            _info = dict_builder(r)
            if _requester_id == _info['member_id']:
                return jsonify(_info), 200

        # If no match is found, return an error
        return jsonify({'error': c.NOT_FOUND_MSG}), 404


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/courses/assign', methods=['POST', 'PUT', 'DELETE'], endpoint='assign_course')
@token_required
def api_assign_course(**kwargs) -> tuple:
    """Respond to an API request to assign a member to a course.

    Bash:
    curl -X POST -H "Authorization: Bearer json.web.token" \
        -H "Content-Type: application/json" \
        -d '{"course_id": 2, "member_id": 2, "role_id": 3}' \
        http://127.0.0.1:5000/api/courses/assign

    PS:
    Invoke-WebRequest -Method Post \
        -Headers "Authorization: Bearer json.web.token" \
        -ContentType "application/json" \
        -Body "{`"course_id`": 2, `"member_id`": 2, `"role_id`": 3"}" \
        -Uri "http://127.0.0.1:5000/api/courses/assign"

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Get the JSON data from the request
    _data = request.get_json()

    _course_id = _data.get('course_id', 0)
    _member_id = _data.get('member_id', 0)
    _role_id = _data.get('role_id', 0)

    # While you need all three values to add or update an association,
    # you only need _course_id and _member_id to delete an association
    # Therefore, verify those two values were provided
    if _course_id == 0 or _member_id == 0:
        return jsonify({'error': c.NOT_FOUND_MSG}), 404

    # Validate inputs
    validate_input('_course_id', _course_id, int)
    validate_input('_member_id', _member_id, int)
    validate_input('_role_id', _role_id, int)

    # Get kwargs from the @token_required decorator
    _requester_id = kwargs.get('requester_id', 2)
    _is_admin = kwargs.get('requester_is_admin', False)

    # Check if the requester is assigned to the course and has the required privilege level
    if not _is_admin:
        # You cannot reassign yourself unless you are an admin
        if _requester_id == _member_id:
            return jsonify({'error': c.NOT_AUTH_MSG}), 403

        """
        SELECT roles.role_privilege
        FROM associations
        JOIN roles ON associations.role_id = roles.role_id
        WHERE associations.course_id = 12
        AND associations.member_id = 2;
        """
        _result = (db.session.query(Role.role_privilege)
                   .select_from(Association)
                   .join(Role, Association.role_id == Role.role_id)
                   .filter(Association.course_id == _course_id)
                   .filter(Association.member_id == _requester_id)
                   .first())
        if not _result:
            return jsonify({'error': c.NOT_FOUND_MSG}), 404

        # Unpack the query row (i.e., convert tuple (2,) to int (2))
        _requestor_role_privilege = _result[0]

        # Get the requested role ID
        """
        SELECT roles.role_privilege FROM roles WHERE roles.role_id = 3;
        """
        _result = (db.session.query(Role.role_privilege)
                   .filter(Role.role_id == _role_id)
                   .first())

        # Unpack the query row (i.e., convert tuple (2,) to int (2))
        # Default to 0 for deletions
        _assignee_role_privilege = 0 if not _result else _result[0]

        # Compare the requestor's privilege to the _assignee_role_privilege
        # Remember, non-admins cannot assign at or above their privilege level
        if (_requestor_role_privilege < c.CUTOFF_PRIVILEGE_EDITOR or
                _requestor_role_privilege <= _assignee_role_privilege):
            return jsonify({'error': c.NOT_AUTH_MSG}), 403

    if request.method == 'POST':
        try:
            """
            INSERT INTO associations (course_id, member_id, role_id) VALUES (1, 6, 3);
            """
            _assoc = Association(course_id=_course_id,
                                 member_id=_member_id,
                                 role_id=_role_id)

            db.session.add(_assoc)
            db.session.commit()

            return jsonify(
                {'message':
                     f'POST: Successfully added Member #{_assoc.member_id} '
                     f'to Course #{_assoc.course_id}.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Addition failed: {str(e)}'}), 500

    if request.method == 'PUT':
        try:
            # Get association object
            _assoc = Association.query.filter(
                Association.course_id == _course_id, Association.member_id == _member_id
            ).first()

            if not _assoc:
                return jsonify({'error': c.NOT_FOUND_MSG}), 404

            # Update association object fields and commit
            # Must update all due to composite primary key
            # _assoc.course_id=_course_id
            # _assoc.member_id=_member_id
            _assoc.role_id = _role_id
            print(_assoc.role_id)
            """
            UPDATE association SET role_id = 2 WHERE course_id = 1 AND member_id == 6;
            """
            db.session.commit()

            return jsonify({'message':
                                f'POST: Successfully updated Member #{_assoc.member_id} '
                                f'for Course #{_assoc.course_id}.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Update failed: {str(e)}'}), 500

    if request.method == 'DELETE':
        try:
            # Get association object
            _assoc = Association.query.filter(
                Association.course_id == _course_id, Association.member_id == _member_id
            ).first()

            if not _assoc:
                return jsonify({'error': c.NOT_FOUND_MSG}), 404

            """
            DELETE FROM associations WHERE course_id = 1 AND member_id == 6;
            """
            db.session.delete(_assoc)
            # Ensure changes are pushed before commit
            db.session.flush()
            db.session.commit()
            return jsonify({'message':
                                f'DELETE: Successfully deleted #{_member_id} '
                                f'for Course #{_course_id}.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Deletion failed: {str(e)}'}), 500

    return jsonify('No action taken'), 204


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
