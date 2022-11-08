#!/usr/bin/env python
from flask import Flask, render_template
import dynamodb_link as db

app = Flask(__name__)


@app.route('/')
def index() -> object:
    """Displays the landing page and data from the database

    :returns: The page and content
    :rtype: object
    """
    items = db.get_items()
    return render_template('index.html', items=items)


if __name__ == '__main__':
    app.run()
