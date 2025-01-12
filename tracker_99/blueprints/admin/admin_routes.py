"""Administration Routing Manager.
"""

from typing import Union

from flask import Response, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from tracker_99 import db
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.admin import admin_bp
from tracker_99.blueprints.admin.admin_forms import SimpleForm
from tracker_99.models.models import Course, Member, Role, Association

INDEX_PAGE = 'main_bp.index'
COURSES_PAGE = 'main_bp.courses'
NOT_AUTH_MSG = 'You do not have permission to perform that action.'

@admin_bp.route('/admin/assign_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def assign_course(course_id:int) -> Union[str, Response]:
    """Assign members to a course.

    :param int course_id: The ID of the course to modify access

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Validate inputs
    validate_input('course_id', course_id, int)

    _page_title = 'Assign Course'
    _page_description = 'Assign Course'

    # Administrators have full access
    if current_user.is_admin:
        """
        SELECT * FROM associations WHERE course_id = 16
        """
        _assoc = Association.query.filter(Association.course_id == course_id).first()
    else:
        _member_id = int(current_user.get_id())
        # Get the member info from the Association table
        # Should look like [{'course_id': 16, 'role_id': 1, 'member_id': 2}]
        """
        SELECT * FROM associations WHERE course_id = 16 AND role_id IN (1, 2) AND member_id = 2 LIMIT 1;
        """
        _assoc = Association.query.filter(
            Association.course_id == course_id,
            Association.member_id == _member_id,
            Association.role_id.in_([1, 2])).first()

    # Only administrators, chairs, and teachers can edit courses
    if _assoc is None:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    # _assoc_list = [assoc.to_dict() for assoc in _assoc]
    _assoc = _assoc.to_dict()

    print(_assoc['role_id'], type(_assoc['role_id']))

    # Instantiate the form
    _form = SimpleForm()

    # Get the course data (e.g., course_id, course_name) from the database
    _course = Course.query.get_or_404(course_id)

    # Get a list of roles from the database
    # _roles = Role.query.all()
    _roles = Role.query.filter(Role.role_id >= _assoc['role_id'])

    # # Ensure the result is a list so you can iterate over it
    # # even if it only contains one Role object
    # _roles = [_roles] if not isinstance(_roles, list) else _roles

    # # Create a list to hold role information
    # # You will iterate through this list of dictionaries,
    # # instead of a list of Role objects, when you render the webpage,
    # # since you will temporarily add a 'Not Assigned' role to it
    # _roles_list = []

    # for _r in _roles:
    #     _role_dict = _r.__dict__
    #     _roles_list.append(_role_dict)

    _roles_list = [roles.to_dict() for roles in _roles]

    # Temporarily add a 'Not Assigned' role
    # Members in this role will be deleted from the Association table
    # or skipped if they are not in the table
    # You will not store 'Not Assigned' members, since that will increase
    # the size of the Association table and slow down queries
    _roles_list.append({"role_id": 4, "role_name": "Not Assigned"})

    # Get a list of members by name from the database
    _members = Member.query.order_by(Member.member_name).all()

    # Ensure the result is a list so you can iterate over it
    # even if it only contains one Member object
    _members = [_members] if not isinstance(_members, list) else _members

    # Create a list to hold member information
    # You will iterate through this list of dictionaries,
    # instead of a list of Member objects, when you render the webpage,
    # since you have to temporarily add a 'role_id' column
    _members_list = []

    for _u in _members:
        _member_dict = _u.__dict__

        # Temporarily add a 'role_id' column
        # and set the default value to 4 ('Not Assigned')
        # That will ensure at least one radio button is checked
        # when you render the webpage
        _member_dict['role_id'] = 4

        # Update the role_id if a value exists in the Association Table
        _a = Association.query.filter(
            Association.course_id == _course.course_id,
            Association.member_id == _member_dict['member_id']).first()

        if _a is not None:
            _member_dict['role_id'] = _a.role_id

        # Add the member with the 'role_id' column to the list
        _members_list.append(_member_dict)

    if request.method == 'POST':
        # Iterate through each member and check if their assignment has changed
        for _u in _members_list:
            _member_id = str(_u['member_id'])

            _a = Association.query.filter(
                Association.course_id == _course.course_id,
                Association.member_id == _member_id).first()

            _role_id = int(request.form.get(_member_id))

            # If the assignment does not exist in the Association table
            # but the course is now assigned
            if _a is None and _role_id < 4:
                print('Adding...')
                _new_assoc = Association(course_id=_course.course_id,
                                        role_id=_role_id,
                                        member_id=_member_id)
                db.session.add(_new_assoc)

            # If the assignment exist in the Association table
            # but the course is now unassigned
            elif _a is not None and _role_id == 4:
                print('Deleting...')
                db.session.delete(_a)

            # If the row exist in the Association table but the role changed
            elif _a is not None and _a.role_id != _role_id:
                print('Updating...')
                _a.role_id = _role_id

            else:
                print('Skipping...')

        db.session.commit()

        return redirect(url_for(INDEX_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'assign_course.html',
        page_title='Assign Members to Course',
        course_name=_course.course_name,
        form=_form,
        roles=_roles_list,
        members_list=_members_list)
