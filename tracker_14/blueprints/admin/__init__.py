"""Initializes the blueprint object and other components related to the blueprint.

This file also turns the directory into a package whose scripts can be imported as modules.
"""

import flask

admin_bp = flask.Blueprint('admin_bp', __name__, template_folder='templates')

# Import the other modules in the package after instantiating
# the Blueprint to avoid known circular import problems with Flask
from tracker_14.blueprints.admin import admin_routes
