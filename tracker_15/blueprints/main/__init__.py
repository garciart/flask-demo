"""Initializes the blueprint object and other components related to the blueprint.

This file also turns the directory into a package whose scripts can be imported as modules.
"""

import flask

main_bp = flask.Blueprint('main_bp', __name__, template_folder='templates')

# Import the other modules in the package after instantiating
# the Blueprint to avoid known circular import problems with Flask
from tracker_15.blueprints.main import main_routes


def get_vars_from_create_app(
        config_name: str = 'default', logging_level: int = 30, logging_level_name: str = 'WARNING'
):
    """Get application variables from create_app().

    :param str config_name: The name of the configuration to use, defaults to 'default'
    :param int logging_level: The level of messages to log, defaults to 30
    :param str logging_level_name: The name of the logging level, defaults to 'WARNING'
    """
    main_bp.config_name = config_name
    main_bp.logging_level = logging_level
    main_bp.logging_level_name = logging_level_name
