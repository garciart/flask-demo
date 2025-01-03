"""Make this directory a package to allow you to import its files as modules.
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

# Import modules after instantiating 'bp' to avoid known circular import problems with Flask
from app.blueprints.main import main_routes
