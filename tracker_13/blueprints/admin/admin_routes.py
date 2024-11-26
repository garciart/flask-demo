"""admin content routing manager.
"""
from typing import Union

from flask import Response, render_template

from tracker_13.app_utils import validate_input
from tracker_13.blueprints.admin import admin_bp
from tracker_13.models.member import Member

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
