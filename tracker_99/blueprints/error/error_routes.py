"""Error content routing manager.
"""

import flask

from tracker_99.blueprints.error import error_bp


# Blueprint's equivalent of Flask errorhandler is app_errorhandler
@error_bp.app_errorhandler(404)
def page_not_found(e) -> tuple:
    """Render an error page if the requested page or resource was not found on the server.

    :returns: The HTML code to render and the response code
    :rtype: tuple
    """
    _page_title = 'We must be cautious...'
    _page_description = 'Not Found'

    return (
        flask.render_template(
            '404.html',
            page_title=_page_title,
            page_description_text=_page_description,
            e=e,
        ),
        404,
    )


# Blueprint's equivalent of Flask errorhandler is app_errorhandler
@error_bp.app_errorhandler(500)
def server_error(e) -> tuple:
    """Render an error page if there is a server error.

    :returns: The HTML code to render and the response code
    :rtype: tuple
    """
    _page_title = 'Chewie!!!'
    _page_description = 'Internal Server Error'

    return (
        flask.render_template(
            '500.html',
            page_title=_page_title,
            page_description_text=_page_description,
            e=e,
        ),
        500,
    )
