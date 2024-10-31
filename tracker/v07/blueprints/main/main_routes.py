"""Main content routing manager.
"""

import flask
from v07 import log_page_request
from v07.blueprints.main import bp
from v07.models import Course


@bp.route("/")
@bp.route("/index")
def index() -> str:
    """The landing page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = "Welcome to Tracker!"
    _page_description = "Landing Page"

    log_page_request(app_instance=flask.current_app, request=flask.request)

    _html = flask.render_template(
        "main/index.html", page_title=_page_title, page_description=_page_description
    )
    return _html


@bp.route("/about")
def about() -> str:
    """The about page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = "About"
    _page_description = "About Page"

    log_page_request(app_instance=flask.current_app, request=flask.request)

    _html = flask.render_template(
        "main/about.html",
        page_title=_page_title,
        page_description=_page_description,
        python_version=flask.current_app.config["PYTHON_VERSION"],
        logging_level=flask.current_app.config["LOGGING_LEVEL"],
    )
    return _html


@bp.route("/courses")
def courses() -> str:
    """The courses page.

    :return: The HTML code to display with {{ placeholders }} populated
    :rtype: str
    """
    _page_title = "List of Courses"
    _page_description = "Courses Page"

    log_page_request(app_instance=flask.current_app, request=flask.request)

    # Get a list of courses from the database
    _courses = Course.query.all()

    # Convert to list if there is only one result
    _courses = [_courses] if not isinstance(_courses, list) else _courses

    # Display a representation of the query
    print(repr(_courses[1]))

    _html = flask.render_template(
        "main/courses.html",
        page_title=_page_title,
        page_description=_page_description,
        courses=_courses,
    )
    return _html
