"""admin content routing manager.
"""
from typing import Union

from flask import Response, flash, redirect, url_for, render_template

from tracker_15 import db
from tracker_15.app_utils import validate_input
from tracker_15.blueprints.admin import admin_bp
from tracker_15.blueprints.admin.admin_forms import EditMemberForm
from tracker_15.models.member import Member

MEMBERS_PAGE = 'main_bp.index'


@admin_bp.route('/admin/view_member/<int:member_id>', methods=['GET'])
def view_member(member_id: int) -> Union[str, Response]:
    """Use form input to view a member in the database.

    :param int member_id: The member to retrieve by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the member is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    _member = Member.query.get_or_404(member_id)

    return render_template(
        'view_member.html',
        page_title='View Member',
        member_id=_member.member_id,
        member_name=_member.member_name,
        member_email=_member.member_email,
    )


@admin_bp.route('/admin/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id: int) -> Union[str, Response]:
    """Use form input to update a member in the database.

    :param int member_id: The member to edit by ID

    :returns: The HTML code to display with {{ placeholders }} populated \
        or redirect if the member is not an administrator
    :rtype: str/Response
    """
    # Validate inputs
    validate_input('member_id', member_id, int)

    _member = Member.query.get_or_404(member_id)
    _form = EditMemberForm(_member.member_name, _member.member_email)

    if _form.validate_on_submit():
        _member.member_name = _form.member_name.data
        _member.member_email = _form.member_email.data
        _member.member_is_admin = _form.member_is_admin.data
        if _form.password.data.strip() != '':
            _member.set_password(_form.password.data)
        db.session.commit()
        flash('Member updated.')
        return redirect(url_for(MEMBERS_PAGE))

    # Default behavior if not sending data to the server (POST, etc.)
    # Re-displays page with flash messages (e.g., errors, etc.)
    _form.member_name.data = _member.member_name
    _form.member_email.data = _member.member_email
    _form.member_is_admin.data = _member.member_is_admin
    return render_template('edit_member.html', page_title='Edit Member', form=_form)
