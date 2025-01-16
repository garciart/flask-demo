"""Member Administration Routing Manager.
"""

from typing import Union

from flask import Response, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from tracker_99 import db
from tracker_99.app_utils import validate_input
from tracker_99.blueprints.admin import admin_bp
from tracker_99.blueprints.admin.admin_forms import (
    AddMemberForm,
    EditMemberForm,
    DeleteMemberForm,
    UpdateProfileForm,
)
from tracker_99.models.models import Member, Association

INDEX_PAGE = 'main_bp.index'
MEMBERS_PAGE = 'main_bp.members'
NOT_AUTH_MSG = 'You do not have permission to perform that action.'

# Allow `except Exception as e` so issues can percolate up, like ValueErrors from the model
# pylint: disable=broad-except


@admin_bp.route('/admin/add_member', methods=['GET', 'POST'])
@login_required
def add_member() -> Union[str, Response]:
    """Use form input to add a member in the database.

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the current user is not an administrator
    :rtype: str/Response
    """
    # Only administrators can add members
    if not current_user.is_admin:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Add Member'
    _page_description = 'Add Member'

    _form = AddMemberForm()

    if _form.validate_on_submit():
        try:
            # Instantiate a Member object
            _member = Member(
                member_name=_form.member_name.data,
                member_email=_form.member_email.data,
                is_admin=_form.is_admin.data,
            )
            # Use the setter in the Member class to set Member.password_hash
            _member.set_password(_form.password.data)
            """
            INSERT INTO members (member_name, member_email, password_hash, is_admin)
            VALUES ("farok.tabr", "farok.tabr@fremen.com", "scrypt:32768:8:1$...", 0);
            """
            db.session.add(_member)
            db.session.commit()
            flash('Addition successful.')
            return redirect(url_for(MEMBERS_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Addition failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'add_member.html',
        page_title=_page_title,
        page_description=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/view_member/<int:member_id>', methods=['GET'])
@login_required
def view_member(member_id: int) -> Union[str, Response]:
    """View a member in the database.

    :param int member_id: The member to retrieve by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the current user is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Admins can view any profile, and members can view their own profile
    if not current_user.is_admin and current_user.member_id != member_id:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'View Member'
    _page_description = 'View Member'

    # Verify member exists
    """
    SELECT * FROM MEMBERS WHERE member_id = 17;
    """
    _member = Member.query.get_or_404(member_id)

    return render_template(
        'view_member.html',
        page_title=_page_title,
        page_description=_page_description,
        member=_member,
    )


@admin_bp.route('/admin/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id: int) -> Union[str, Response]:
    """Use form input to update a member in the database.

    :param int member_id: The member to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the current user is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Admins can edit any profile, and members can edit their own profile
    if not current_user.is_admin and current_user.member_id != member_id:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Edit Member'
    _page_description = 'Edit Member'

    # Verify member exists
    """
    SELECT * FROM MEMBERS WHERE member_id = 17;
    """
    _member = Member.query.get_or_404(member_id)
    _form = EditMemberForm(_member.member_name, _member.member_email)

    # Pre-populate form with current member details
    if request.method == 'GET':
        _form.member_name.data = _member.member_name
        _form.member_email.data = _member.member_email
        _form.is_admin.data = _member.is_admin

    if _form.validate_on_submit():
        try:
            _member.member_name = _form.member_name.data
            _member.member_email = _form.member_email.data
            _member.is_admin = _form.is_admin.data
            # Only update the password if data was entered in the password fields
            if _form.password.data.strip() != '':
                # Use the setter in the Member class to set Member.password_hash
                _member.set_password(_form.password.data)
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
            flash('Update successful.')
            return redirect(url_for(MEMBERS_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Update failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'edit_member.html',
        page_title=_page_title,
        page_description=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/delete_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def delete_member(member_id: int) -> Union[str, Response]:
    """Use form input to delete a member from the database.

    :param int member_id: The member to delete by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the current user is not an administrator
    :rtype: str/Response
    """

    # Validate inputs
    validate_input('member_id', member_id, int)

    # Only administrators can delete members
    if not current_user.is_admin:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    # Do not let members delete themselves!
    if current_user.get_id() == member_id:
        flash('You cannot delete yourself!')
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Delete Member'
    _page_description = 'Delete Member'

    # Verify member exists
    """
    SELECT * FROM MEMBERS WHERE member_id = 17;
    """
    _member = Member.query.get_or_404(member_id)

    _form = DeleteMemberForm()

    if _form.validate_on_submit():
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
            flash('Delete successful.')
            return redirect(url_for(MEMBERS_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Delete failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # And re-displays page with flash messages (e.g., errors, etc.)
    _member_name = _member.member_name
    return render_template(
        'delete_member.html',
        page_title=_page_title,
        page_description=_page_description,
        member_name=_member_name,
        form=_form,
    )


@admin_bp.route('/admin/update_profile/<int:member_id>', methods=['GET', 'POST'])
@login_required
def update_profile(member_id: int) -> Union[str, Response]:
    """Use form input to update your profile.

    :param int member_id: The member to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the current user is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Only you can update your profile
    if current_user.get_id() != member_id:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Update Profile'
    _page_description = 'Update Profile'

    # Verify member exists
    """
    SELECT * FROM MEMBERS WHERE member_id = 17;
    """
    _member = Member.query.get_or_404(member_id)
    _form = UpdateProfileForm(_member.member_email)

    # Pre-populate form with current member details
    if request.method == 'GET':
        _form.member_email.data = _member.member_email

    if _form.validate_on_submit():
        try:
            _member.member_email = _form.member_email.data

            # Only update the password if data was entered in the password fields
            if _form.password.data.strip() != '':
                # Use the setter in the Member class to set Member.password_hash
                _member.set_password(_form.password.data)
            """
            UPDATE members
            SET member_email = "farok.tabr@fremen.com",
                password_hash = "scrypt:32768:8:1$...",
            WHERE member_id = 17;
            """
            # db.session.add(_member)
            db.session.commit()
            flash('Update successful.')
            return redirect(url_for(INDEX_PAGE))
        except Exception as e:
            db.session.rollback()
            flash(f'Update failed: {str(e)}', 'error')

    # Default behavior if not sending data to the server (POST, etc.)
    # And re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'update_profile.html',
        page_title=_page_title,
        page_description=_page_description,
        form=_form,
        member=_member,
    )
