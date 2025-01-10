"""admin content routing manager.
"""

from typing import Union

from flask import Response, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

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
MEMBERS_PAGE = 'main_bp.index'
NOT_AUTH_MSG = 'You do not have permission to perform that action.'


@admin_bp.route('/admin/add_member', methods=['GET', 'POST'])
@login_required
def add_member() -> Union[str, Response]:
    """Use form input to add a member in the database.

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the member is not an administrator
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
        _member = Member(
            member_name=_form.member_name.data,
            member_email=_form.member_email.data,
            is_admin=_form.is_admin.data,
        )
        _member.set_password(_form.password.data)
        # Ensure the object is updated in the session
        # before committing it to the database
        db.session.add(_member)
        db.session.commit()
        flash('Member added.')
        return redirect(url_for(MEMBERS_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    return render_template(
        'add_member.html',
        page_title=_page_title,
        page_description_text=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/view_member/<int:member_id>', methods=['GET'])
@login_required
def view_member(member_id: int) -> Union[str, Response]:
    """Use form input to view a member in the database.

    :param int member_id: The member to retrieve by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the member is not an administrator
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

    _member = Member.query.get_or_404(member_id)

    return render_template(
        'view_member.html',
        page_title=_page_title,
        page_description_text=_page_description,
        member_id=_member.member_id,
        member_name=_member.member_name,
        member_email=_member.member_email,
    )


@admin_bp.route('/admin/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id: int) -> Union[str, Response]:
    """Use form input to update a member in the database.

    :param int member_id: The member to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the member is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    # Admins can view any profile, and members can view their own profile
    if not current_user.is_admin and current_user.member_id != member_id:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'Edit Member'
    _page_description = 'Edit Member'

    _member = Member.query.get_or_404(member_id)
    _form = EditMemberForm(_member.member_name, _member.member_email)

    if _form.validate_on_submit():
        _member.member_name = _form.member_name.data
        _member.member_email = _form.member_email.data
        _member.is_admin = _form.is_admin.data
        if _form.password.data.strip() != '':
            _member.set_password(_form.password.data)
        # Ensure the object is updated in the session
        # before committing it to the database
        db.session.add(_member)
        db.session.commit()
        flash('Member updated.')
        return redirect(url_for(MEMBERS_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    _form.member_name.data = _member.member_name
    _form.member_email.data = _member.member_email
    _form.is_admin.data = _member.is_admin
    return render_template(
        'edit_member.html',
        page_title=_page_title,
        page_description_text=_page_description,
        form=_form,
    )


@admin_bp.route('/admin/delete_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def delete_member(member_id: int) -> Union[str, Response]:
    """Use form input to delete a member from the database.

    :param int member_id: The member to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the member is not an administrator
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

    _member = Member.query.get_or_404(member_id)
    _assoc = Association.query.filter(Association.member_id == _member.member_id).all()

    _form = DeleteMemberForm()

    if _form.validate_on_submit():
        if _form.submit.data:
            for _a in _assoc:
                db.session.delete(_a)
            db.session.delete(_member)
            db.session.commit()
            flash('Member deleted.')
        return redirect(url_for(MEMBERS_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _member_name = _member.member_name
    return render_template(
        'delete_member.html',
        page_title=_page_title,
        page_description_text=_page_description,
        member_name=_member_name,
        form=_form,
    )


@admin_bp.route('/admin/update_profile/<int:member_id>', methods=['GET', 'POST'])
@login_required
def update_profile(member_id: int) -> Union[str, Response]:
    """Use form input to update your profile.

    :param int member_id: The member to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the member is not an administrator
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

    _member = Member.query.get_or_404(member_id)
    _form = UpdateProfileForm(_member.member_email)

    if _form.validate_on_submit():
        _member.member_email = _form.member_email.data
        if _form.password.data.strip() != '':
            _member.set_password(_form.password.data)
        db.session.commit()
        flash('Profile updated.')
        return redirect(url_for(INDEX_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Also re-displays page with flash messages (e.g., errors, etc.)
    _member_name = _member.member_name
    _form.member_email.data = _member.member_email
    return render_template(
        'update_profile.html',
        page_title=_page_title,
        page_description_text=_page_description,
        form=_form,
        member_name=_member_name,
    )


