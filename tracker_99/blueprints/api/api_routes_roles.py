"""API content routing manager for roles.

Test: http://127.0.0.1:5000/api/test
"""

from flask import jsonify, request

from tracker_99 import db, constants as c
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.api import api_bp, token_required
from tracker_99.models.models import Role


# Allow `except Exception as e` so issues can percolate up, like ValueErrors from the model
# pylint: disable=broad-except


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/roles/all', methods=['GET'], endpoint='roles_all')
@token_required
def api_roles_all(**kwargs) -> tuple:
    """Respond to an API request for a list of all roles and their information.

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/roles/all

    PS:
    Invoke-WebRequest -Method GET \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/roles/all"

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Get kwargs from the @token_required decorator
    _is_admin = kwargs.get('requester_is_admin', False)

    if not _is_admin:
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Administrators can view all roles
    # query.all() always returns a list, even if it is empty
    """
    SELECT * FROM roles;
    """
    _roles_list = Role.query.all()

    if not _roles_list:
        return jsonify({'error': c.NOT_FOUND_MSG}), 404

    # Exclude the 'password_hash' field
    _filtered_roles = [
        {
            'role_id': role.role_id,
            'role_name': role.role_name,
            'role_privilege': role.role_privilege,
        }
        for role in _roles_list
    ]

    # Use jsonify to convert the filtered list to JSON
    return jsonify(roles=_filtered_roles), 200


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/roles/add', methods=['POST'], endpoint='add_role')
@token_required
def api_add_role(**kwargs) -> tuple:
    """Respond to an API request to add a role.

    Bash:
    curl -X POST -H "Authorization: Bearer json.web.token" \
        -H "Content-Type: application/json" \
        -d '{"role_name": "Foo", "role_privilege": 15}' \
        http://127.0.0.1:5000/api/roles/add

    PS:
    Invoke-WebRequest -Method Post \
        -Headers "Authorization: Bearer json.web.token" \
        -ContentType "application/json" \
        -Body "{`"role_name`": `"Foo`", `"role_privilege`": 15"}" \
        -Uri "http://127.0.0.1:5000/api/roles/add"

    :returns: A status message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Only administrators can add roles
    # Get kwargs from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Get the JSON data from the request
    _data = request.get_json()

    _role_name = _data.get('role_name', '')
    _role_privilege = _data.get('role_privilege', '')

    # Add role if all attributes are provided and correct
    validate_input("_role_name", _role_name, str)
    validate_input("_role_privilege", _role_privilege, int)

    try:
        # Instantiate a Role object
        _role = Role(
            role_name=_role_name,
            role_privilege=_role_privilege,
        )
        """
        INSERT INTO roles (role_name, role_privilege)
        VALUES ("FOO", 15);
        """
        db.session.add(_role)
        db.session.commit()

        # Get row_id of the new role
        _new_id = _role.role_id

        return jsonify(
            {'message': f'POST: Successfully added {_role.role_name} ({_new_id}).'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Addition failed: {str(e)}'}), 500


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/roles/get/<int:role_id>', methods=['GET'], endpoint='get_role')
@token_required
def api_get_role(role_id: int, **kwargs) -> tuple:
    """Respond to an API request for role information.

    Bash:
    curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/roles/get/5

    PS:
    Invoke-WebRequest -Method GET \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/roles/get/5"

    :param int role_id: The role to retrieve by ID

    :returns: The data in JSON format or an error message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('role_id', role_id, int)

    # Only administrators can add roles
    # Get kwargs from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Verify role exists
    """
    SELECT * FROM roles WHERE role_id = 17;
    """
    _role = Role.query.get_or_404(role_id)

    _role_data = {
        'role_id': _role.role_id,
        'role_name': _role.role_name,
        'role_privilege': _role.role_privilege,
    }

    # Use jsonify to convert the _role_data to JSON
    return jsonify(role=_role_data), 200


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/roles/edit/<int:role_id>', methods=['PUT'], endpoint='edit_role')
@token_required
def api_edit_role(role_id: int, **kwargs) -> tuple:
    """Respond to an API request to edit a role.

    Bash:
    curl -X PUT -H "Authorization: Bearer json.web.token" \
        -H "Content-Type: application/json" \
        -d '{"role_privilege": 25}' \
        http://127.0.0.1:5000/api/roles/edit/5

    PS:
    Invoke-WebRequest -Method Put \
        -ContentType "application/json" \
        -Headers "Authorization: Bearer json.web.token" \
        -Body "{`"role_privilege`": 25"}' \
        -Uri "http://127.0.0.1:5000/api/roles/edit/5"

    :returns: A status message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('role_id', role_id, int)

    # Only administrators can add roles
    # Get kwargs from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Verify role exists
    """
    SELECT * FROM roles WHERE role_id = 5;
    """
    _role = Role.query.get_or_404(role_id)

    try:
        # Get the JSON data from the request
        _data = request.get_json()

        # Validate and update role attributes if provided in the request
        if 'role_name' in _data:
            validate_input("_data['role_name']", _data['role_name'], str)
            _role.role_name = _data['role_name']
        if 'role_privilege' in _data:
            validate_input("_data['role_privilege']", _data['role_privilege'], int)
            _role.role_privilege = _data['role_privilege']
        """
        UPDATE roles
        SET role_privilege = 25
        WHERE role_id = 5;
        """
        # db.session.add(_role)
        db.session.commit()
        return jsonify({'message': f'PUT: Successfully updated {_role.role_name}.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Update failed: {str(e)}'}), 500


# Do not forget to add an endpoint, or you will get an AssertionError!
@api_bp.route('/api/roles/delete/<int:role_id>', methods=['DELETE'], endpoint='delete_role')
@token_required
def api_delete_role(role_id: int, **kwargs) -> tuple:
    """Respond to an API request to delete a role.

    Bash:
    curl -X DELETE -H "Authorization: Bearer json.web.token" \
        http://127.0.0.1:5000/api/roles/delete/5

    PS:
    Invoke-WebRequest -Method DELETE \
        -Headers @{ "Authorization" = "Bearer json.web.token" } \
        -Uri "http://127.0.0.1:5000/api/roles/delete/5"

    :returns: A status message with the HTTP status code (Response, int)
    :rtype: tuple
    """
    # Validate inputs
    validate_input('role_id', role_id, int)

    # Only administrators can add roles
    # Get kwargs from the @token_required decorator
    if not kwargs.get('requester_is_admin', False):
        return jsonify({'error': c.NOT_AUTH_MSG}), 403

    # Verify role exists
    """
    SELECT * FROM roles WHERE role_id = 5;
    """
    _role = Role.query.get_or_404(role_id)

    # Save name for message after deletion
    _role_name = _role.role_name

    try:
        """
        DELETE FROM roles WHERE role_id = 5;
        """
        db.session.delete(_role)
        # Ensure changes are pushed before commit
        db.session.flush()
        db.session.commit()
        return jsonify({'message': f'DELETE: Successfully deleted {_role_name}.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Deletion failed: {str(e)}'}), 500
