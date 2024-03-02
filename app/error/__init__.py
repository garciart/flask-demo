"""Make this directory a package to allow you to import its files elsewhere
"""
from flask import Blueprint

error_bp = Blueprint('error', __name__)

# Import app modules after init app to prevent circular import problems
# Flake8 F401: imports are used for type hints
from app.error import error_routes  # noqa: E402 E501 F401 pylint:disable=wrong-import-position
