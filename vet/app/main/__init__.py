"""Make this directory a package to allow you to import its files as modules.
"""
from flask import Blueprint

bp = Blueprint('main', __name__)

# Import app modules after init to avoid known circular import problems
# Flake8 F401: imports are used for type hints
from app.main import main_routes
