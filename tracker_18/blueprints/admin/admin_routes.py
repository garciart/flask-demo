"""admin content routing manager.
"""

from typing import Union

from flask import Response, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from tracker_18 import db
from tracker_18.app_utils import validate_input
from tracker_18.blueprints.admin import admin_bp
from tracker_18.blueprints.admin.admin_forms import EditMemberForm
from tracker_18.models.member import Member

INDEX_PAGE = 'main_bp.index'
NOT_AUTH_MSG = 'You do not have permission to perform that action.'


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

    # Admins can view any profile, and users can view their own profile
    if not current_user.member_is_admin and current_user.member_id != member_id:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _member = Member.query.get_or_404(member_id)

    return render_template(
        'view_member.html',
        page_title='View Member',
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

    # Admins can view any profile, and users can view their own profile
    if not current_user.member_is_admin and current_user.member_id != member_id:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _member = Member.query.get_or_404(member_id)
    _form = EditMemberForm(_member.member_name, _member.member_email)

    if _form.validate_on_submit():
        _member.member_name = _form.member_name.data
        _member.member_email = _form.member_email.data
        _member.member_is_admin = _form.member_is_admin.data
        if _form.password.data.strip() != '':
            _member.set_password(_form.password.data)
        # Ensure the object is updated in the session
        # before committing it to the database
        db.session.add(_member)
        db.session.commit()
        flash('Member updated.')
        return redirect(url_for(INDEX_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    _form.member_name.data = _member.member_name
    _form.member_email.data = _member.member_email
    _form.member_is_admin.data = _member.member_is_admin
    return render_template('edit_member.html', page_title='Edit Member', form=_form)
