"""Main content routing manager.
"""

import flask

from tracker_18.blueprints.main import main_bp
from tracker_18.models.member import Member


@main_bp.route('/')
@main_bp.route('/index')
def index() -> str:
    """The landing page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Welcome to Tracker!'
    _page_description = 'Landing Page'

    members = Member.query.all()

    return flask.render_template(
        'index.html',
        page_title_text=_page_title,
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
    _page_title = 'About Tracker...'
    _page_description = 'About Page'

    return flask.render_template(
        'about.html', page_title_text=_page_title, page_description_text=_page_description
    )
