"""Flask Demo

Usage: python3 -m flask --app app run
"""
from flask import Flask, render_template

__author__ = 'Rob Garcia'

app = Flask(__name__)


@app.route('/')
def index():
    # type: () -> str
    """The landing page.

    :return: A string of HTML code
    :rtype: str
    """
    _page_title = 'Flask Demo'
    _html = render_template('index.html', page_title=_page_title)
    return _html


@app.route('/test')
def test():
    # type: () -> str
    """A test page.

    :return: A string of HTML code
    :rtype: str
    """
    _page_title = 'Flask Demo'
    _html = render_template('test.html', page_title=_page_title)
    return _html


if __name__ == '__main__':
    # Default setting
    app.run(host='0.0.0.0', port=5000)
