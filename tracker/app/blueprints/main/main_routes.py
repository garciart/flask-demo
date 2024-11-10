"""Main content routing manager.
"""

import flask
from app import db, log_page_request
from app.blueprints.main import bp
from app.models import Course, CourseGroup


@bp.route('/')
@bp.route('/index')
def index() -> str:
    """The landing page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Welcome to Tracker!'
    _page_description = 'Landing Page'

    log_page_request(app_instance=flask.current_app, request=flask.request)

    _html = flask.render_template(
        'main/index.html', page_title=_page_title, page_description=_page_description
    )
    return _html


@bp.route('/about')
def about() -> str:
    """The about page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'About'
    _page_description = 'About Page'

    log_page_request(app_instance=flask.current_app, request=flask.request)

    _html = flask.render_template(
        'main/about.html',
        page_title=_page_title,
        page_description=_page_description,
        python_version=flask.current_app.config['PYTHON_VERSION'],
        logging_level=flask.current_app.config['LOGGING_LEVEL'],
    )
    return _html


@bp.route('/courses')
def courses() -> str:
    """The courses page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'List of Courses'
    _page_description = 'Courses Page'

    log_page_request(app_instance=flask.current_app, request=flask.request)

    # Query to get all courses along with the course_group_code
    _courses_with_group_code = (
        db.session.query(
            Course.course_id,
            Course.course_name,
            Course.course_code,
            Course.course_desc,
            CourseGroup.course_group_code.label('course_group_code'),
        )
        .join(CourseGroup, Course.course_group_id == CourseGroup.course_group_id)
        .all()
    )

    # Display a representation of the query
    print(repr(_courses_with_group_code))

    _html = flask.render_template(
        'main/courses.html',
        page_title=_page_title,
        page_description=_page_description,
        courses=_courses_with_group_code,
    )
    return _html


@bp.route('/test', methods=['GET', 'POST'])
def test() -> str:
    """Test page.

    :returns: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = 'Test Page'
    _page_description = 'Test Page'

    log_page_request(app_instance=flask.current_app, request=flask.request)

    _environments = {
        'sandbox': {
            'env_name': 'Sandbox',
            'env_background_color': 'Tan',
            'env_text_color': 'Black',
            'link_text_color': 'White',
        },
        'com': {
            'env_name': 'COM',
            'env_background_color': 'SteelBlue',
            'env_text_color': 'Black',
            'link_text_color': 'White',
        },
        'mil': {
            'env_name': 'MIL',
            'env_background_color': 'Olive',
            'env_text_color': 'Black',
            'link_text_color': 'White',
        },
    }

    _selected_env = _environments['sandbox']

    if flask.request.method == 'POST':
        _selected_env = flask.request.form['environment']

    _html = flask.render_template(
        'main/test.html',
        page_title=_page_title,
        page_description=_page_description,
        environments=_environments,
        selected_env=_selected_env,
    )
    return _html
