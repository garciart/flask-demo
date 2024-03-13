"""Make this directory a package to allow you to import its files as modules.
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


__author__ = 'Rob Garcia'

# Variables accessible to other modules
# Initialized in create_app()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(alt_config=None):
    # type: (str) -> Flask
    """Application Factory.

    :param str alt_config: An alternate configuration file path for
    testing, etc. Use app/config.py if None

    :return: An application instance
    :rtype: Flask
    """
    # Create and configure the app
    app = Flask(__name__)

    # Import app modules after init to avoid known circular import problems
    from app.app_utils import validate_input  # noqa: E501 E402 pylint:disable=import-outside-toplevel
    from app.config import Config  # noqa: E501 E402 pylint:disable=import-outside-toplevel

    # Validate inputs
    if alt_config is not None:
        validate_input('alt_config', alt_config, str)

    # Load the default configuration file if an alternate does not exist
    if alt_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(alt_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    _setup_logging(app)

    _python_version = _get_python_version()

    if _python_version < 3.08:
        # Use lazy % formatting in logging functions
        app.logger.warning(
            'Python version is %0.2f. Flask 3 requires Python 3.8 or above.',
            _python_version)

    # _create_instance_folder(app)

    # _initialize_database(app)

    # Test page for http://127.0.0.1/hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Start routing
    # Import app modules after init to avoid known circular import problems
    from app.main import main_routes  # noqa: E501 E402 pylint:disable=import-outside-toplevel
    from app.auth import auth_routes  # noqa: E501 E402 pylint:disable=import-outside-toplevel
    from app.admin import admin_routes  # noqa: E501 E402 pylint:disable=import-outside-toplevel
    from app.error import error_routes  # noqa: E501 E402 pylint:disable=import-outside-toplevel
    from app.api import api_routes  # noqa: E501 E402 pylint:disable=import-outside-toplevel

    app.register_blueprint(main_routes.bp)
    app.register_blueprint(auth_routes.auth_bp)
    app.register_blueprint(admin_routes.admin_bp)
    app.register_blueprint(error_routes.error_bp)
    app.register_blueprint(api_routes.api_bp)

    # For debugging
    print('Information:')
    print('_python_version', _python_version, type(_python_version))

    return app


def _setup_logging(app):
    # type: (Flask) -> None
    """Setup logging.

    NOTE - Will not log if using flask --debug run

    :param Flask app: The application instance

    :return: None
    """
    # Do not log if using 'python3 flask --debug run'
    if not app.debug:
        # Attempt to read LOGGING_LEVEL environment variable
        # Leave at logging.DEBUG (10) if variable does not exist
        _logging_level = 10

        try:
            _logging_level = getattr(logging, app.config['LOGGING_LEVEL'])
        except (AttributeError, KeyError):
            pass

        _msg_format = ('%(asctime)s-%(name)s-%(levelname)s: %(message)s'
                       '[in %(pathname)s:%(lineno)d]')

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(_msg_format))
        file_handler.setLevel(_logging_level)

        app.logger.addHandler(file_handler)

        app.logger.setLevel(_logging_level)
        app.logger.info('Starting Flask application')


def _get_python_version():
    # type: () -> float
    """Get the Python version used by the server.

    :return: The Python version used by the server
    :rtype: float
    """
    # Get Python version and convert to float (e.g., 3.9 -> 3.09)
    _python_version = float(
        f'{sys.version_info.major}.{sys.version_info.minor:02d}')

    return _python_version


# IMPORTANT - This must be last to prevent circular import problems!
# Flake8 F401: Using model when running flask db init, migrate, and upgrade
from app import models  # noqa: F401 E402 pylint:disable=wrong-import-position
