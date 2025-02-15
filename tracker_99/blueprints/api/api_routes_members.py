"""API content routing manager for members.

Test: http://127.0.0.1:5000/api/test
"""

from flask import jsonify, request

from tracker_99 import db, constants as c
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.api import api_bp, token_required
from tracker_99.models.models import Association, Member


# Allow `except Exception as e` so issues can percolate up, like ValueErrors from the model
# pylint: disable=broad-except


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/members/all', methods=['GET'], endpoint='members_all')
@token_required
def api_members_all(**kwargs) -> tuple:
    """Respond to an API request for a list of all members and their information.

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/all

    PS:
    Invoke-WebRequest -Method GET \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/members/all"

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Only administrators view all members
    # Get kwargs from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # query.all() always returns a list, even if it is empty
    """
    SELECT * FROM members;
    """
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
@api_bp.route('/api/members/add', methods=['POST'], endpoint='add_member')
@token_required
def api_add_member(**kwargs) -> tuple:
    """Respond to an API request to add a member.

    Bash:
    curl -X POST -H "Content-Type: application/json" \
        -H "Authorization: Bearer json.web.token" \
        -d '{"member_name": "Farok.Tabr", "member_email": "farok.tabr@fremen.com", "is_admin": false, "password": "Change.Me.123"}' \
        http://127.0.0.1:5000/api/members/add

    PS:
    Invoke-WebRequest -Method Post \
        -ContentType "application/json" \
        -Headers "Authorization: Bearer json.web.token" \
        -Body "{`"member_name`": `"Farok.Tabr`", `"member_email`": `"farok.tabr@fremen.com`", `"is_admin`": false, `"password`": `"Change.Me.123`"}" \
        -Uri "http://127.0.0.1:5000/api/members/add"

     :returns: A status message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Only administrators can add members
    # Get kwargs from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Get the JSON data from the request
    _data = request.get_json()

    # Add member if all attributes are provided and correct
    validate_input("_data['member_name']", _data['member_name'], str)
    validate_input("_data['member_email']", _data['member_email'], str)
    validate_input("_data['is_admin']", _data['is_admin'], bool)
    validate_input("_data['password']", _data['password'], str)

    try:
        # Instantiate a Member object
        _member = Member(
            member_name=_data['member_name'],
            member_email=_data['member_email'],
            is_admin=_data['is_admin'],
        )
        # Use the setter in the Member class to set Member.password_hash
        _member.set_password(_data['password'])
        """
        INSERT INTO members (member_name, member_email, password_hash, is_admin)
        VALUES ("farok.tabr", "farok.tabr@fremen.com", "scrypt:32768:8:1$...", 0);
        """
        db.session.add(_member)
        db.session.commit()

        _new_id = _member.get_id()

        return jsonify(
            {'message': f'POST: Successfully added {_member.member_name} ({_new_id}).'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Addition failed: {str(e)}'}), 500


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/members/get/<int:member_id>', methods=['GET'], endpoint='get_member')
@token_required
def api_get_member(member_id: int, **kwargs) -> tuple:
    """Respond to an API request for member information.

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/members/get/2

    PS:
    Invoke-WebRequest -Method GET \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/members/get/2"

    :param int member_id: The member to retrieve by ID

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Admins can view any profile, and members can view their own profile
    # Get kwargs from the @token_required decorator
    if (not kwargs.get('requester_is_admin', False)) and (
            int(kwargs.get('requester_id', 0)) != member_id):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Verify member exists
    """
    SELECT * FROM members WHERE member_id = 17;
    """
    _member = Member.query.get_or_404(member_id)

    _member_data = {
        'member_id': _member.member_id,
        'member_name': _member.member_name,
        'member_email': _member.member_email,
        'is_admin': _member.is_admin,
    }

    # Use jsonify to convert the _member_data to JSON
    return jsonify(member=_member_data), 200


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/members/edit/<int:member_id>', methods=['PUT'], endpoint='edit_member')
@token_required
def api_edit_member(member_id: int, **kwargs) -> tuple:
    """Respond to an API request to edit a member.

    Bash:
    curl -X PUT -H "Content-Type: application/json" \
        -H "Authorization: Bearer json.web.token" \
        -d '{"is_admin": true}' \
        http://127.0.0.1:5000/api/members/edit/2

    PS:
    Invoke-WebRequest -Method Put \
        -ContentType "application/json" \
        -Headers "Authorization: Bearer json.web.token" \
        -Body "{`"is_admin`": false}" \
        -Uri "http://127.0.0.1:5000/api/members/edit/2"

    :returns: A status message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Admins can edit any profile, and members can edit their own profile
    # Get kwargs from the @token_required decorator
    if (not kwargs.get('requester_is_admin', False)) and (
            int(kwargs.get('requester_id', 0)) != member_id):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Verify member exists
    """
    SELECT * FROM members WHERE member_id = 17;
    """
    _member = Member.query.get_or_404(member_id)

    try:
        # Get the JSON data from the request
        _data = request.get_json()

        # Validate and update member attributes if provided in the request
        if 'member_name' in _data:
            validate_input("_data['member_name']", _data['member_name'], str)
            _member.member_name = _data['member_name']
        if 'member_email' in _data:
            validate_input("_data['member_email']", _data['member_email'], str)
            _member.member_email = _data['member_email']
        if 'is_admin' in _data:
            validate_input("_data['is_admin']", _data['is_admin'], bool)
            _member.is_admin = bool(_data['is_admin'])
        if 'password' in _data:
            validate_input("_data['password']", _data['password'], str)
            _member.set_password(_data['password'])
        """
        UPDATE members
        SET member_name = "Farok.Tabr",
            member_email = "farok.tabr@fremen.com",
            password_hash = "scrypt:32768:8:1$...",
            is_admin = 0
        WHERE member_id = 17;
        """
        # db.session.add(_member)
        db.session.commit()
        return jsonify({'message': f'PUT: Successfully updated {_member.member_name}.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Update failed: {str(e)}'}), 500


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/members/delete/<int:member_id>', methods=['DELETE'], endpoint='delete_member')
@token_required
def api_delete_member(member_id: int, **kwargs) -> tuple:
    """Respond to an API request to delete a member.

    Bash:
    curl -X DELETE -H "Authorization: Bearer json.web.token" \
        http://127.0.0.1:5000/api/members/delete/2

    PS:
    Invoke-WebRequest -Method DELETE \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/members/delete/2"

    :returns: A status message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Only administrators can delete members
    # Get kwargs from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Do not let members delete themselves!
    if int(kwargs.get('requester_id', 0)) == member_id:
        return jsonify({'error': 'You cannot delete yourself!'}), 400

    # Verify member exists
    """
    SELECT * FROM members WHERE member_id = 17;
    """
    _member = Member.query.get_or_404(member_id)

    # Save name for message after deletion
    _member_name = _member.member_name

    try:
        # Delete association data first
        """
        DELETE FROM associations WHERE member_id = 17;
        """
        Association.query.filter(Association.member_id == _member.member_id).delete()
        """
        DELETE FROM members WHERE member_id = 17;
        """
        db.session.delete(_member)
        # Ensure changes are pushed before commit
        db.session.flush()
        db.session.commit()
        return jsonify({'message': f'DELETE: Successfully deleted {_member_name}.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Deletion failed: {str(e)}'}), 500
