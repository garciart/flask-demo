"""API content routing manager.

Test: http://127.0.0.1:5000/api/test
"""

from flask import Response, jsonify

from tracker.tracker_11.app_utils import validate_input
from tracker.tracker_11.blueprints.api import api_bp
from tracker.tracker_11.models.member import Member

_DUMMY_DATA = [
    {'course_id': 1, 'course_name': 'Python 101', 'course_code': 'CS100',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Python.'},
    {'course_id': 2, 'course_name': 'Flask 101', 'course_code': 'CS101',
     'course_group': 'SDEV', 'course_desc': 'Introduction to Flask.'}
]


@api_bp.route('/api/test', methods=['GET'])
def get_test_data() -> Response | tuple:
    """Get the list of test data when a REST call is made.

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    _response = jsonify(test_data=_DUMMY_DATA,
                        status=200,
                        mimetype='application/json'), 200
    return _response


@api_bp.route('/api/members/all', methods=['GET'])
def api_members() -> Response | tuple:
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
        {'member_id': m.member_id, 'member_name': m.member_name,
         'member_email': m.member_email}
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200


@api_bp.route('/api/members/<int:member_id>', methods=['GET'])
def api_member(member_id: int) -> Response | tuple:
    """Get a member from the database using their ID when a REST call is made.

    :param int member_id: The member to retrieve by ID

    :returns: A response with the data in JSON format
    :rtype: Response
    """
    validate_input('member_id', member_id, int)

    # Remember, when querying for a single result, like `Foo.query.first()`,
    # use the following code to return a list if the result was None:
    # _foo = Foo.query.first()
    # _foo = [_foo] if _foo is not None else []

    _member = Member.query.get(member_id)

    if _member is None:
        return jsonify({'error': 'Member not found'}), 404

    _members_list = [_member] if _member is not None else []

    # Exclude the 'member_email' field
    _filtered_members = [
        {'member_id': m.member_id, 'member_name': m.member_name,
         'member_email': m.member_email}
        for m in _members_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(members=_filtered_members), 200
