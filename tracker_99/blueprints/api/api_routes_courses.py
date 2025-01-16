"""API content routing manager for courses.

Test: http://127.0.0.1:5000/api/test
"""

from functools import wraps
from typing import Any, Callable, Union

from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from tracker_99 import db
from tracker_99.app_utils import validate_input, decode_auth_token
from tracker_99.blueprints.api import api_bp
from tracker_99.models.models import Association, Course, Member

NOT_AUTH_MSG = 'You do not have permission to perform that action.'


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


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/courses/all', methods=['GET'], endpoint='courses_all')
@token_required
def api_courses_all(**kwargs) -> tuple:
    """Respond to an API request for a list of all courses and their information.

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/courses/all

    PS:
    Invoke-WebRequest -Method GET \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/courses/all"

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Only administrators view all courses
    # is_admin is a kwarg from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': NOT_AUTH_MSG}), 403

    # query.all() always returns a list, even if it is empty
    """
    SELECT * FROM courses;
    """
    _courses_list = Course.query.all()

    if not _courses_list:
        return jsonify({'error': 'No courses found.'}), 404

    # Exclude the 'password_hash' field
    _filtered_courses = [
        {
            'course_id': c.course_id,
            'course_name': c.course_name,
            'course_code': c.course_code,
            'course_group': c.course_group,
            'course_desc': c.course_desc,
        }
        for c in _courses_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(courses=_filtered_courses), 200


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/courses/add', methods=['POST'], endpoint='add_course')
@token_required
def api_add_course(**kwargs) -> tuple:
    """Respond to an API request to add a course.

    Bash:
    curl -X POST -H "Content-Type: application/json" \
        -H "Authorization: Bearer json.web.token" \
        -d '{"course_name": "Building Bad Python Applications", "course_code": "SDEV 301", "course_group": "SDEV", "course_desc": "Not recommended!"}' \
        http://127.0.0.1:5000/api/courses/add

    curl -X POST -H "Content-Type: application/json" \
        -d '{"course_name": "Building Bad Python Applications", "course_code": "SDEV 301", "course_group": "SDEV", "course_desc": "Not recommended!"}' \
        http://127.0.0.1:5000/api/courses/add

    curl -X POST -H "Content-Type: application/json" \
        -d '{"course_name": "Building Bad Python Applications", "course_code": "SDEV 301"}' \
        http://127.0.0.1:5000/api/courses/add

    PS:
    Invoke-WebRequest -Method Post \
        -ContentType "application/json" \
        -Headers "Authorization: Bearer json.web.token" \
        -Body "{`"course_name`": `"Building Bad Python Applications`", `"course_code`": `"farok.tabr@fremen.com`", `"course_group`": `"SDEV`", `"course_desc`": `"Not recommended!`"}" \
        -Uri "http://127.0.0.1:5000/api/courses/add"

    :returns: A status message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    _member_id = kwargs.get('requester_id', 0)

    # Get the JSON data from the request
    _data = request.get_json()

    print("_data['course_name']", _data['course_name'], type(_data['course_name']))
    print(_data.get('course_name', ''))

    _course_name = _data.get('course_name', '')
    _course_code = _data.get('course_code', '')
    _course_group = _data.get('course_group', '')
    _course_desc = _data.get('course_desc', '')

    # Add course if all attributes are provided and correct
    validate_input("_course_name", _course_name, str)
    validate_input("_course_code", _course_code, str)
    validate_input("_course_group", _course_group, str, allow_empty=True)
    validate_input("_course_desc", _course_desc, str, allow_empty=True)

    try:
        # Instantiate a Course object
        _course = Course(
            course_name=_course_name,
            course_code=_course_code,
            course_group=_course_group,
            course_desc=_course_desc,
        )
        """
        INSERT INTO courses (course_name, course_code, course_group, course_desc)
        VALUES ("Building Bad Python Applications", "SDEV 301", "SDEV", "Not recommended!");
        """
        db.session.add(_course)
        db.session.commit()

        # Get row_id of the new course
        _new_id = _course.course_id

        # Add the course and chair to the association table
        _assoc = Association(course_id=_new_id, role_id=4, member_id=_member_id)

        db.session.add(_assoc)
        db.session.commit()
        return jsonify(
            {'message': f'POST: Successfully added {_course.course_name} ({_new_id}).'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': f'Addition failed: {str(e)}'}), 200


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/courses/get/<int:course_id>', methods=['GET'], endpoint='get_course')
@token_required
def api_get_course(course_id: int, **kwargs) -> tuple:
    """Respond to an API request for course information.

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/courses/get/2

    PS:
    Invoke-WebRequest -Method GET \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/courses/get/2"

    :param int course_id: The course to retrieve by ID

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    _member_id = kwargs.get('requester_id', 0)

    # Admins can view any course, and members can view assigned courses
    # kwargs are from the @token_required decorator
    if (not kwargs.get('requester_is_admin', False)):
        """
        SELECT * FROM associations WHERE course_id = 2 AND member_id = 6;
        """
        _assoc = Association.query.filter(
            Association.course_id == course_id,
            Association.member_id == _member_id,
        ).first()

        if not _assoc:
            return jsonify({'error': NOT_AUTH_MSG}), 403

    # Verify course exists
    """
    SELECT * FROM courses WHERE course_id = 2;
    """
    _course = Course.query.get_or_404(course_id)

    _course_data = {
        'course_id': _course.course_id,
        'course_name': _course.course_name,
        'course_code': _course.course_code,
        'course_group': _course.course_group,
        'course_desc': _course.course_desc,
    }

    # Use jsonify to convert the _course_data to JSON
    return jsonify(course=_course_data), 200


# # Do not forget to add an endpoint, or you will get an AssertionError!
# @api_bp.route('/api/members/edit/<int:member_id>', methods=['PUT'], endpoint='edit_member')
# @token_required
# def api_edit_member(member_id: int, **kwargs) -> tuple:
#     """Respond to an API request to edit a member.

#     Bash:
#     curl -X PUT -H "Content-Type: application/json" \
#         -H "Authorization: Bearer json.web.token" \
#         -d '{"is_admin": true}' \
#         http://127.0.0.1:5000/api/members/edit/2

#     PS:
#     Invoke-WebRequest -Method Put \
#         -ContentType "application/json" \
#         -Headers "Authorization: Bearer json.web.token" \
#         -Body "{`"is_admin`": false}" \
#         -Uri "http://127.0.0.1:5000/api/members/edit/2"

#     :returns: A status message with the HTTP status code (Response, int)
#     :rtype: tuple
#     """
#     # Validate inputs
#     validate_input('member_id', member_id, int)

#     # Admins can edit any profile, and members can edit their own profile
#     # kwargs are from the @token_required decorator
#     if (not kwargs.get('requester_is_admin', False)) and (
#             int(kwargs.get('requester_id', 0)) != member_id):
#         return jsonify({'error': NOT_AUTH_MSG}), 403

#     # Verify member exists
#     """
#     SELECT * FROM members WHERE member_id = 17;
#     """
#     _member = Member.query.get_or_404(member_id)

#     try:
#         # Get the JSON data from the request
#         _data = request.get_json()

#         # Validate and update member attributes if provided in the request
#         if 'member_name' in _data:
#             validate_input("_data['member_name']", _data['member_name'], str)
#             _member.member_name = _data['member_name']
#         if 'member_email' in _data:
#             validate_input("_data['member_email']", _data['member_email'], str)
#             _member.member_email = _data['member_email']
#         if 'is_admin' in _data:
#             validate_input("_data['is_admin']", _data['is_admin'], bool)
#             _member.is_admin = bool(_data['is_admin'])
#         if 'password' in _data:
#             validate_input("_data['password']", _data['password'], str)
#             _member.set_password(_data['password'])
#         """
#         UPDATE members
#         SET member_name = "Farok.Tabr",
#             member_email = "farok.tabr@fremen.com",
#             password_hash = "scrypt:32768:8:1$...",
#             is_admin = 0
#         WHERE member_id = 17;
#         """
#         # db.session.add(_member)
#         db.session.commit()
#         return jsonify({'message': f'PUT: Successfully updated {_member.member_name} .'}), 200
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({'message': f'Update failed: {str(e)}'}), 200


# # Do not forget to add an endpoint, or you will get an AssertionError!
# @api_bp.route('/api/members/delete/<int:member_id>', methods=['DELETE'], endpoint='delete_member')
# @token_required
# def api_delete_member(member_id: int, **kwargs) -> tuple:
#     """Respond to an API request to delete a member.

#     Bash:
#     curl -X DELETE -H "Authorization: Bearer json.web.token" \
#         http://127.0.0.1:5000/api/members/delete/2

#     PS:
#     Invoke-WebRequest -Method DELETE \
#         -Headers @{ "Authorization" = "Bearer json.web.token" } \
#         -Uri "http://127.0.0.1:5000/api/members/delete/2"

#     :returns: A status message with the HTTP status code (Response, int)
#     :rtype: tuple
#     """
#     # Validate inputs
#     validate_input('member_id', member_id, int)

#     # Only administrators can delete members
#     # is_admin is a kwarg from the @token_required decorator
#     if not kwargs.get('requester_is_admin', False):
#         return jsonify({'error': NOT_AUTH_MSG}), 403

#     # Do not let members delete themselves!
#     if int(kwargs.get('requester_id', 0)) == member_id:
#         return jsonify({'error': 'You cannot delete yourself!'}), 400

#     # Verify member exists
#     """
#     SELECT * FROM members WHERE member_id = 17;
#     """
#     _member = Member.query.get_or_404(member_id)

#     # Save name for message after deletion
#     _member_name = _member.member_name

#     try:
#         # Delete association data first
#         """
#         DELETE FROM associations WHERE member_id = 17;
#         """
#         Association.query.filter(Association.member_id == _member.member_id).delete()
#         """
#         DELETE FROM members WHERE member_id = 17;
#         """
#         db.session.delete(_member)
#         # Ensure changes are pushed before commit
#         db.session.flush()
#         db.session.commit()
#         return jsonify({'message': f'PUT: Successfully deleted {_member_name} .'}), 200
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({'message': f'Delete failed: {str(e)}'}), 200
