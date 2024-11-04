"""Main content routing manager.
"""

import flask

main_bp = flask.Blueprint('main_bp', __name__, template_folder='templates')


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
        _config_name_text=flask.current_app.config['CONFIG_NAME'],
        _logging_level_text=flask.current_app.config['LOGGING_LEVEL'],
        _logging_level_name_text=flask.current_app.config['LOGGING_LEVEL_NAME'],
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
