"""Initializes the blueprint object and other components related to the blueprint.

This file also turns the directory into a package whose scripts can be imported as modules.
"""

from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

# Import the other modules in the package after instantiating
# the Blueprint to avoid known circular import problems with Flask
from tracker_99.blueprints.auth import auth_routes  # noqa: E402
