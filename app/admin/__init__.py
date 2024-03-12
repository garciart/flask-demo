"""Make this directory a package to allow you to import its files as modules.
"""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

# Import app modules after init to avoid known circular import problems
# Flake8 F401: imports are used for type hints
from app.admin import admin_routes  # noqa: E402 E501 F401 pylint:disable=wrong-import-position
