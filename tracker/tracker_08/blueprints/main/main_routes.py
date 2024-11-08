"""Main content routing manager.
"""

import flask
from . import main_bp


@main_bp.route('/')
@main_bp.route('/index')
def index() -> str:
    """The landing page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Welcome to Tracker!'
    _page_description = 'Landing Page'

    return flask.render_template(
        'index.html',
        page_title_text=_page_title,
        page_description_text=_page_description,
        _config_name_text=main_bp.config_name,
        _logging_level_text=main_bp.logging_level,
        _logging_level_name_text=main_bp.logging_level_name,
    )


@main_bp.route('/about')
def about() -> str:
    """The about page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'About Tracker...'
    _page_description = 'About Page'

    return flask.render_template(
        'about.html', page_title_text=_page_title, page_description_text=_page_description
    )
