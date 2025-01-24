"""Administration Routing Manager.
"""

from typing import Union

from flask import Response, abort, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from tracker_99 import db, constants as c
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.admin import admin_bp
from tracker_99.blueprints.admin.admin_forms import SimpleForm
from tracker_99.models.models import Course, Member, Role, Association


@admin_bp.route('/admin/assign_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def assign_course(course_id: int) -> Union[str, Response]:  # NOSONAR
    """Assign members to a course.

    NOTE - (NOSONAR) This method updates information in a three-way association table,
    and I am accepting the code complexity above 15.

    :param int course_id: The ID of the course to modify access

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    _page_title = 'Assign Course'
    _page_description = 'Assign Course'

    # Get the course data (e.g., course_id, course_name) from the database
    _course = Course.query.get_or_404(course_id)

    # Get the members assigned to the course
    # The query will generate a list of tuples
    # Each tuple in the list will have the role_id, member_id, member_name, is_admin,
    # and role_privilege of member assigned to the course in that order, like
    # [(1, 16, 0, 'Stilgar.Tabr', 20), (2, 2, 0, 'Leto.Atreides', 10), ...]
    """
    SELECT associations.role_id,
        members.member_id,
        members.member_name,
        members.is_admin,
        roles.role_privilege
    FROM associations,
        members,
        roles
    WHERE associations.member_id = members.member_id AND
        associations.role_id = roles.role_id AND
        associations.course_id = 12;
    """
    _assigned_members = (
        db.session.query(
            Association.role_id,
            Member.member_id,
            Member.member_name,
            Member.is_admin,
            Role.role_privilege,
        )
        .join(Member, Association.member_id == Member.member_id)
        .join(Role, Association.role_id == Role.role_id)
        .filter(Association.course_id == course_id)
        .all()
    )

    # Convert _assigned_members to a list of dictionaries
    # Make sure the keys correspond to the values
    _keys = ['role_id', 'member_id', 'member_name', 'is_admin', 'role_privilege']
    _assigned_members = [dict(zip(_keys, row)) for row in _assigned_members]

    # Get the ID of the current user
    _member_id = int(current_user.get_id())

    # Only members with role_privileges greater than or equal to 10,
    # like chairs and teachers of the course and admins,
    # can assign other members to a course
    if not current_user.is_admin and not any(
        a['member_id'] == _member_id and a['role_privilege'] >= c.PRIVILEGE_LVL_ASSIGNER
        for a in _assigned_members
    ):
        abort(403, c.NOT_AUTH_MSG)

    # Get a list of ID for assigned members
    _assigned_member_ids = [a['member_id'] for a in _assigned_members]

    # Get a list of unassigned members
    """
    SELECT members.member_id,
           members.member_name,
           members.is_admin
    FROM members
    WHERE members.member_id NOT IN (2, 3, 4, 16);
    """
    _unassigned_members = (
        db.session.query(Member.member_id, Member.member_name, Member.is_admin)
        .filter(Member.member_id.notin_(_assigned_member_ids))
        .all()
    )

    # Convert _unassigned_members to a list of dictionaries
    # Make sure the keys correspond to their values
    _keys = ['member_id', 'member_name', 'is_admin']
    _unassigned_members = [dict(zip(_keys, row)) for row in _unassigned_members]

    # Members cannot elevate their privileges
    # (teachers cannot reassign themselves to chairs, etc.)
    # and they cannot reassign other members at or above their privilege level
    # (teachers cannot assign or reassign other teachers, etc.)
    # Therefore, set the cutoff to one less than the privilege level of the current user
    # This sets the default to assigning members as students only
    if not current_user.is_admin:
        _PRIVILEGE_LVL_level = (
            int(
                next(
                    (
                        a['role_privilege']
                        for a in _assigned_members
                        if _member_id == a['member_id']
                    ),
                    c.PRIVILEGE_LVL_EDITOR,
                )
            )
            - 1
        )
    else:
        _PRIVILEGE_LVL_level = 99

    # Get members with privilege less than the level of the current user
    _touchable_members = [
        a for a in _assigned_members if int(a['role_privilege']) <= _PRIVILEGE_LVL_level
    ]

    # Match the structure of _unassigned_members and _touchable_members
    # by adding required key-value pairs
    for u in _unassigned_members:
        u['role_id'] = 1
        u['role_privilege'] = 0

    # Combine the two lists of dictionaries
    _members_list = _touchable_members + _unassigned_members

    # Get info for roles less than the privilege level of the current user
    # Use ORDER BY for rendering in the template by privilege level
    """
    SELECT role_id, role_name FROM roles
    WHERE roles.role_privilege < 10 ORDER BY role_privilege DESC;
    """
    _roles_list = (
        db.session.query(Role.role_id, Role.role_name)
        .filter(Role.role_privilege <= _PRIVILEGE_LVL_level)
        .order_by(Role.role_privilege.desc())
        .all()
    )

    # Temporarily add a 'Unassigned' role
    # Members in this role will be deleted from the Association table
    # or skipped if they are not in the table
    # Do not store 'Unassigned' members, since that will increase
    # the size of the Association table and slow down queries
    _roles_list.append({"role_id": 1, "role_name": "Unassigned"})

    if request.method == 'POST':
        # Get all associations for the given course in advance
        _existing_associations = {
            a.member_id: a
            for a in Association.query.filter(Association.course_id == _course.course_id).all()
        }

        # Iterate through each member and check if their assignment has changed
        for _u in _members_list:
            # Get the current assignment in the Association table
            _member_id = str(_u['member_id'])

            # Get the value of the selected radio button in the template for the member
            # Using the member_id in the name keeps each group unique (name="2_role")
            _role_id = int(request.form.get(f'{_member_id}_role'))

            # Check if the member already has an association
            _a = _existing_associations.get(int(_member_id))

            # Add an association if the assignment does not exist in the Association table
            # but the course is now assigned
            if _a is None and _role_id != 1:
                print('Adding...')
                _new_assoc = Association(
                    course_id=_course.course_id, role_id=_role_id, member_id=_member_id
                )
                db.session.add(_new_assoc)

            # Delete the association if the assignment exists in the Association table
            # but the course is now unassigned
            elif _a is not None and _role_id == 1:
                print('Deleting...')
                db.session.delete(_a)

            # Update the association if the assignment exists in the Association table
            # but the role has changed
            elif _a is not None and _a.role_id != _role_id:
                print('Updating...')
                _a.role_id = _role_id

            else:
                print('Skipping...')

        db.session.commit()

        return redirect(url_for(c.INDEX_PAGE))

    # Instantiate the form
    _form = SimpleForm()

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'assign_course.html',
        page_title=_page_title,
        page_description=_page_description,
        course_name=_course.course_name,
        form=_form,
        roles_list=_roles_list,
        members_list=_members_list,
    )
