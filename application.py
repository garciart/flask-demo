#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Flask application module.
"""

from flask import Flask, render_template

import dynamodb_link as db
from validator import validate_regex_match

# Elastic Beanstalk looks for an 'application' callable by default, not 'app'.
application = Flask(__name__)


@application.route('/')
def index() -> object:
    """Display the landing page and a list of medications

    :return: The page and content
    :rtype: object
    """
    items = db.get_items()
    return render_template('index.html', items=items)


@application.route('/details/<string:generic_name>', methods=['GET'])
def details(generic_name):
    # Type: (str) -> object
    """Display details about a specific medication

    :return: The page and content
    :rtype: object
    """
    # Validate inputs
    validate_regex_match(generic_name, db.short_desc_regex, err_msg='Invalid generic name.')
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
    application.run()
