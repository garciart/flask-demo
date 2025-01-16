"""Main content routing manager.
"""
from typing import Union

from flask import Response
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import current_user, login_required

from tracker_99.blueprints.main import main_bp
from tracker_99.models import db
from tracker_99.models.models import Course, Member, Role, Association

INDEX_PAGE = 'main_bp.index'
MEMBERS_PAGE = 'main_bp.index'
NOT_AUTH_MSG = 'You do not have permission to perform that action.'


@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index() -> Union[str, Response]:
    """The landing page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    _page_title = 'Welcome!'
    _page_description = 'Landing Page'

    if current_user.is_admin:
        _courses = Course.query.all()
    else:
        _member_id = int(current_user.get_id())

        """
        SELECT courses.course_id, courses.course_name, courses.course_code,
            courses.course_group, courses.course_desc, roles.role_id, roles.role_name
        FROM courses
        JOIN associations ON courses.course_id = associations.course_id
        JOIN roles ON roles.role_id = associations.role_id
        WHERE associations.member_id = 2;
        """

        _courses = (
            db.session.query(
                Course.course_id,
                Course.course_name,
                Course.course_code,
                Course.course_group,
                Course.course_desc,
                Role.role_id,
                Role.role_name,
            )
            .join(Association, Course.course_id == Association.course_id)
            .join(Role, Role.role_id == Association.role_id)
            .filter(Association.member_id == _member_id)
            .all()
        )

    # Convert to list if there is only one result
    _courses = [_courses] if not isinstance(_courses, list) else _courses

    return render_template(
        'index.html',
        page_title=_page_title,
        page_description=_page_description,
        courses=_courses,
    )


@main_bp.route('/about')
def about() -> Union[str, Response]:
    """The about page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    _page_title = 'About...'
    _page_description = 'About Page'

    return render_template(
        'about.html', page_title=_page_title, page_description=_page_description
    )


@main_bp.route('/courses')
@login_required
def courses() -> Union[str, Response]:
    """The course list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    return redirect(url_for(INDEX_PAGE))


@main_bp.route('/members')
@login_required
def members() -> Union[str, Response]:
    """The member list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'View Members'
    _page_description = 'List of Members'

    _members = Member.query.all()

    # Convert to list if there is only one result
    _members = [_members] if not isinstance(_members, list) else _members

    _html = render_template(
        'members.html',
        page_title=_page_title,
        page_description=_page_description,
        members=_members,
    )
    return _html


@main_bp.route('/roles')
@login_required
def roles() -> Union[str, Response]:
    """The role list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str/Response
    """
    # Redirect if not an Administrator
    if not current_user.is_admin:
        flash(NOT_AUTH_MSG)
        return redirect(url_for(INDEX_PAGE))

    _page_title = 'View Roles'
    _page_description = 'List of Roles'

    _roles = Role.query.all()

    # Convert to list if there is only one result
    _roles = [_roles] if not isinstance(_roles, list) else _roles

    _html = render_template(
        'roles.html',
        page_title=_page_title,
        page_description=_page_description,
        roles=_roles
    )
    return _html
