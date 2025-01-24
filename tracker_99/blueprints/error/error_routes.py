"""Error content routing manager.
"""

from flask import render_template, jsonify, request

from tracker_99.blueprints.error import error_bp


# Blueprint's equivalent of Flask errorhandler is app_errorhandler
@error_bp.app_errorhandler(404)
def page_not_found(e) -> tuple:
    """Render an error page if the requested page or resource was not found on the server.

    Sends a JSON response instead if caused by an ReST call.

    :returns: The HTML code to render or JSON message and the response code
    :rtype: tuple
    """
    if '/api/' in request.url:
        return jsonify({'error': f'{str(e)}'}), 404
    else:
        _page_title = 'We must be cautious...'
        _page_description = 'Not Found'

        return (
            render_template(
                '404.html',
                page_title=_page_title,
                page_description=_page_description,
                e=e,
            ),
            404,
        )


# Blueprint's equivalent of Flask errorhandler is app_errorhandler
@error_bp.app_errorhandler(403)
def forbidden(e) -> tuple:
    """Render an error page if an unauthorized user requests for a page or resource.

    Sends a JSON response instead if caused by an ReST call.

    :returns: The HTML code to render or JSON message and the response code
    :rtype: tuple
    """
    if '/api/' in request.url:
        return jsonify({'error': f'{str(e)}'}), 403
    else:
        _page_title = 'We must be cautious...'
        _page_description = 'Not Found'

        return (
            render_template(
                '403.html',
                page_title=_page_title,
                page_description=_page_description,
                e=e,
            ),
            403,
        )


# Blueprint's equivalent of Flask errorhandler is app_errorhandler
@error_bp.app_errorhandler(500)
def server_error(e) -> tuple:
    """Render an error page if there is a server error.

    Sends a JSON response instead if caused by an ReST call.

    :returns: The HTML code to render or JSON message and the response code
    :rtype: tuple
    """
    if '/api/' in request.url:
        return jsonify({'error': f'{str(e)}'}), 500
    else:
        _page_title = 'Chewie!!!'
        _page_description = 'Internal Server Error'

        return (
            render_template(
                '500.html',
                page_title=_page_title,
                page_description=_page_description,
                e=e,
            ),
            500,
        )
