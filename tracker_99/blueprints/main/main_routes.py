"""Main content routing manager.
"""

import flask
from flask_login import current_user, login_required

from tracker_99.blueprints.main import main_bp
from tracker_99.models.models import Member

INDEX_PAGE = 'main_bp.index'
MEMBERS_PAGE = 'main_bp.index'
NOT_AUTH_MSG = 'You do not have permission to perform that action.'


@main_bp.route('/')
@main_bp.route('/index')
def index() -> str:
    """The landing page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Welcome!'
    _page_description = 'Landing Page'

    members = Member.query.all()

    return flask.render_template(
        'index.html',
        page_title=_page_title,
        page_description_text=_page_description,
        config_name_text=main_bp.config_name,
        logging_level_text=main_bp.logging_level,
        logging_level_name_text=main_bp.logging_level_name,
        members_data=members,
    )


@main_bp.route('/about')
def about() -> str:
    """The about page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'About...'
    _page_description = 'About Page'

    return flask.render_template(
        'about.html', page_title=_page_title, page_description_text=_page_description
    )


@main_bp.route('/members')
@login_required
def members():
    # type: () -> str
    """The member list page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    # Redirect if not an Administrator
    if not current_user.member_is_admin:
        flask.flash(NOT_AUTH_MSG)
        return flask.redirect(flask.url_for(INDEX_PAGE))

    _page_title = 'View Members'
    _page_description = 'List of Members'

    _members = Member.query.all()

    # Convert to list if there is only one result
    _members = [_members] if not isinstance(_members, list) else _members

    _html = flask.render_template('members.html', page_title=_page_title,
                                  page_description_text=_page_description, members=_members)
    return _html
