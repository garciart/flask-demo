"""Initialize package and share code with other modules.

Usage:
- python3 -m flask --app cm run
- python3 -m flask --app cm run --debug # Allow hot reload
"""
import logging
import os
import sys
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

__author__ = 'Rob Garcia'

# Create the Flask instance first, then import the app modules,
# to prevent circular import issues
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# Import app modules after configuring app to prevent circular import issues
from app import routes, models  # noqa E402 pylint:disable=wrong-import-position
from app import cm_logger  # noqa: E402 pylint:disable=wrong-import-position


# Attempt to read LOGGING_LEVEL environment variable
# Leave at logging.DEBUG (10) if variable does not exist
LOGGING_LEVEL = 10
try:
    LOGGING_LEVEL = getattr(logging, app.config['LOGGING_LEVEL'])
except AttributeError:
    pass
# Create logger for CM user
logger = cm_logger.create_logger('cm_logger', LOGGING_LEVEL)
# Capture root logger messages if LOG_ROOT is true
LOG_ROOT = os.environ.get('LOG_ROOT') == 'True'
if LOG_ROOT:
    # File handler for root logger messages
    logging.basicConfig(
        filename='cm.log', level=logging.DEBUG,
        format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    # Console handler for logger root messages
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


# Get Python version and convert to float (e.g., 3.9 -> 3.09)
PYTHON_VERSION = float(
    f'{sys.version_info.major}.{sys.version_info.minor:02d}')
if PYTHON_VERSION < 3.08:
    # Use lazy % formatting in logging functions
    logger.warning(
        'Python version is %f. Flask 3 supports Python 3.8 and newer.',
        PYTHON_VERSION)
