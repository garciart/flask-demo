#!/usr/bin/env python
from flask import Flask, render_template

import dynamodb_link as db

app = Flask(__name__)


@app.route('/')
def index() -> object:
    """Displays the landing page and data from the database

    :return: The page and content
    :rtype: object
    """
    items = db.get_items()
    return render_template('index.html', items=items)


@app.route('/details/<string:generic_name>', methods=['GET'])
def details(generic_name):
    response = db.read_item(generic_name=generic_name)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if 'Item' in response:
            return render_template('details.html', item=response['Item'])
        return {'msg': 'Item not found!'}
    return {
        'msg': 'Some error occurred',
        'response': response
    }


if __name__ == '__main__':
    app.run()
