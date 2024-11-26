"""API content routing manager.

Test: http://127.0.0.1:5000/api/test
"""
import os
from typing import Union

from flask import (Response, jsonify, send_from_directory, request)

from tracker_16 import db
from tracker_16.app_utils import validate_input
from tracker_16.blueprints.api import api_bp
from tracker_16.models.member import Member

_DUMMY_DATA = [
    {'course_id': 1, 'course_name': 'Python 101', 'course_code': 'CS100',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Python.'},
    {'course_id': 2, 'course_name': 'Flask 101', 'course_code': 'CS101',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Flask.'}
]


@api_bp.route('/favicon.ico')
def api_get_favicon() -> Response:
    """Loads application icon when making API calls with no HTML.

    :returns: The favicon.ico file
    :rtype: Response
    """
    favicon_path = os.path.join('static', 'img', 'favicon.ico')
    return send_from_directory(os.path.dirname(favicon_path), os.path.basename(favicon_path),
                               mimetype='image/x-icon')


@api_bp.route('/api/test', methods=['GET'])
def api_get_test_data() -> Union[Response, tuple]:
    """Get the list of test data when a REST call is made.

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    _response = jsonify(test_data=_DUMMY_DATA,
                        status=200,
                        mimetype='application/json'), 200
    return _response


@api_bp.route('/api/members/all', methods=['GET'])
def api_get_all_members() -> Union[Response, tuple]:
    """Get the list of members in the database when a REST call is made.

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    # query.all() always returns a list, even if it is empty
    _members_list = Member.query.all()

    if not _members_list:
        return jsonify({'error': 'No members found'}), 404

    # Exclude the 'password_hash' field
    _filtered_members = [
        {'member_id': m.member_id,
         'member_name': m.member_name,
         'member_email': m.member_email,
         'member_is_admin': m.member_is_admin}
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200


@api_bp.route('/api/members/<int:member_id>', methods=['GET'])
def api_get_member(member_id: int) -> Union[Response, tuple]:
    """Get a member from the database using their ID when a REST call is made.

    :param int member_id: The member to retrieve by ID

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    # External method that throws an exception if member_id is not an int, or it is empty
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
        {'member_id': m.member_id,
         'member_name': m.member_name,
         'member_email': m.member_email,
         'member_is_admin': m.member_is_admin}
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200


@api_bp.route('/api/members/<int:member_id>', methods=['PUT'])
def api_update_member(member_id: int) -> Union[Response, tuple]:
    """Update a member through an API ReST call using their ID.

    Examples:

    Linux:
    curl -X PUT -H "Content-Type: application/json" -d '{"member_name": "Leto.Atreides", \
        "member_email": "leto.atreides@atreides.com", "member_is_admin: true}' \
        http://localhost:5000/api/members/2

    Windows:
    Invoke-WebRequest -Uri "http://localhost:5000/api/members/2" `
        -Method Put `
        -ContentType "application/json" `
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
